#!/usr/bin/env python3
"""Works out Steam deadlines backwards from a release date.

Example:
  python3 release_timeline.py --release 2027-09-14
  python3 release_timeline.py --release 2027-09-14 --nextfest 2027-06-14 --today 2026-10-12

Values from the Steamworks docs as of 2026-10-12 (see references/steamworks-rules.md).
Business days count Monday to Friday only, US holidays are ignored.
"""
import argparse
import sys
from datetime import date, timedelta

FEE_WAIT_DAYS = 21           # fee paid -> earliest release
COMING_SOON_MIN_DAYS = 14    # Coming Soon page public before release
REVIEW_BUSINESS_DAYS = 7     # store and build review: submit this early
TAX_CHECK_BUSINESS_DAYS = 15 # tax and identity check, upper bound
NF_PRESS_PREVIEW_DAYS = 35   # demo review for press preview
NF_LATEST_DAYS = 21          # demo review at the latest
NF_LENGTH_DAYS = 7
RECOMMENDED_PAGE_MONTHS = 6  # rule of thumb, not a Valve rule


def sub_business_days(d: date, n: int) -> date:
    while n > 0:
        d -= timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def fmt(d: date) -> str:
    return d.strftime("%a %d %b %Y")


def parse(s: str) -> date:
    try:
        return date.fromisoformat(s)
    except ValueError:
        sys.exit(f"Invalid date: {s} (format YYYY-MM-DD)")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--release", required=True, help="planned release, YYYY-MM-DD")
    p.add_argument("--nextfest", help="start of the chosen Next Fest edition, YYYY-MM-DD")
    p.add_argument("--today", help="reference date for warnings, default: today")
    a = p.parse_args()

    release = parse(a.release)
    today = parse(a.today) if a.today else date.today()

    coming_soon_latest = release - timedelta(days=COMING_SOON_MIN_DAYS)
    coming_soon_rec = release - timedelta(days=RECOMMENDED_PAGE_MONTHS * 30)
    store_review_latest = sub_business_days(coming_soon_latest, REVIEW_BUSINESS_DAYS)
    store_review_rec = sub_business_days(coming_soon_rec, REVIEW_BUSINESS_DAYS)
    # no paid fee, no app, no store page
    fee_latest = min(release - timedelta(days=FEE_WAIT_DAYS), store_review_latest)
    # fee and tax check must be done before submitting the store page
    account_rec = sub_business_days(min(store_review_rec, fee_latest), TAX_CHECK_BUSINESS_DAYS)
    build_review_latest = sub_business_days(release, REVIEW_BUSINESS_DAYS)

    store_why = "review takes up to 7 business days"
    live_why = "must be live 2 weeks before release"
    warnings = []
    fest = ""
    fest_best = []

    if a.nextfest:
        nf = parse(a.nextfest)
        nf_end = nf + timedelta(days=NF_LENGTH_DAYS)
        fest = f"Next Fest {fmt(nf)} to {fmt(nf_end)}"
        # Next Fest needs a public store page, so the page deadlines move earlier
        nf_live = nf - timedelta(days=NF_LATEST_DAYS)
        nf_page = sub_business_days(nf_live, REVIEW_BUSINESS_DAYS)
        if nf_page < store_review_latest:
            store_review_latest, store_why = nf_page, "Next Fest needs a live store page"
        if nf_live < coming_soon_latest:
            coming_soon_latest, live_why = nf_live, "Next Fest needs a live store page"
        fee_latest = min(fee_latest, store_review_latest)
        fest_must = [(nf - timedelta(days=NF_LATEST_DAYS), "Send demo for review", "Next Fest rule: 3 weeks before")]
        fest_best = [
            (max(nf - timedelta(days=60), coming_soon_rec + timedelta(days=7)), "Demo is live", "time for feedback before Next Fest"),
            (nf - timedelta(days=NF_PRESS_PREVIEW_DAYS), "Send demo for review", "to be in the Next Fest press preview"),
        ]
        if coming_soon_rec > nf:
            warnings.append("The recommended Coming Soon date is after Next Fest. Put the page up earlier.")
        if nf_end >= release:
            warnings.append("Release is before Next Fest ends. Only unreleased games can take part.")
        gap = (release - nf_end).days
        if 0 < gap < 30:
            warnings.append(f"Only {gap} days between Next Fest and release. Little time to act on feedback.")
        if gap > 150:
            warnings.append(f"{gap} days between Next Fest and release. The wishlist boost fades, aim for 1 to 4 months.")
    else:
        fest_must = []

    # (date, what to do, why)
    must = [
        (fee_latest, "Pay the USD 100 app fee", "needed before the store page, 21-day wait before release"),
        (store_review_latest, "Send store page to Valve for review", store_why),
        (coming_soon_latest, "Coming Soon page is live", live_why),
        (build_review_latest, "Send final build and launch discount for review", "review takes up to 7 business days"),
    ] + fest_must
    best = [
        (account_rec, "Open Steamworks account, do the tax interview", "tax check takes up to 15 business days"),
        (store_review_rec, "Send store page to Valve for review", ""),
        (coming_soon_rec, "Coming Soon page is live", "6 months to collect wishlists"),
    ] + fest_best

    print(f"Release: {fmt(release)}" + (f"   |   {fest}" if fest else ""))

    def block(title, subtitle, items, missed_word):
        print(f"\n{title}")
        print(f"{subtitle}\n")
        for d, what, why in sorted(items, key=lambda r: r[0]):
            flag = f"   <- {missed_word}" if d < today else ""
            reason = f"  ({why})" if why else ""
            print(f"  {fmt(d)}   {what}{reason}{flag}")

    must_note = "Steam rules. Miss one and you lose Next Fest or must move the release." if a.nextfest else "Steam rules. Miss one and the release date moves."
    block("MUST DO BY", must_note, must, "MISSED")
    block("BEST TO DO BY", "Recommended, so enough people wishlist the game.", best, "late")

    if release.weekday() >= 5:
        warnings.append("Release falls on a weekend. Indies usually launch Monday to Thursday.")
    hard_missed = any(d < today for d, _, _ in must)
    if hard_missed:
        warnings.append("At least one MUST date has passed. Move the release date.")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")
    print("\nValues from the Steamworks docs. Re-check them before you commit to a date.")
    return 1 if hard_missed else 0


if __name__ == "__main__":
    sys.exit(main())
