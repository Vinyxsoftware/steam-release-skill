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

    rows = [
        (account_rec, "Steamworks account, tax interview, USD 100 fee", "recommended (check takes up to 15 business days)"),
        (store_review_rec, "Submit store page for review", "recommended"),
        (coming_soon_rec, "Coming Soon page public", "recommended (6 months before)"),
        (fee_latest, "Fee paid at the latest", "hard (21-day wait, before store review)"),
        (store_review_latest, "Submit store page at the latest", "hard (7 business days)"),
        (coming_soon_latest, "Coming Soon page public at the latest", "hard (2 weeks)"),
        (build_review_latest, "Submit release build and launch discount", "hard (7 business days)"),
        (release, "Release", ""),
    ]
    warnings = []

    if a.nextfest:
        nf = parse(a.nextfest)
        nf_end = nf + timedelta(days=NF_LENGTH_DAYS)
        rows += [
            (nf - timedelta(days=90), "Demo public (feedback before the fest)", "recommended"),
            (nf - timedelta(days=NF_PRESS_PREVIEW_DAYS), "Submit demo for review (press preview)", "hard if press preview wanted"),
            (nf - timedelta(days=NF_LATEST_DAYS), "Submit demo for review at the latest", "hard (3 weeks)"),
            (nf, "Next Fest starts", ""),
            (nf_end, "Next Fest ends", ""),
        ]
        nf_page = sub_business_days(nf - timedelta(days=NF_LATEST_DAYS), REVIEW_BUSINESS_DAYS)
        rows.append((nf_page, "Submit store page (must be public for the fest)", "hard for Next Fest"))
        if coming_soon_rec > nf:
            warnings.append("Recommended Coming Soon date falls after Next Fest. Publish the page earlier.")
        if nf_end >= release:
            warnings.append("Release is before Next Fest ends. Only unreleased games can take part.")
        gap = (release - nf_end).days
        if 0 < gap < 30:
            warnings.append(f"Only {gap} days between fest and release. Little time to act on feedback.")
        if gap > 150:
            warnings.append(f"{gap} days between fest and release. The wishlist boost tends to fade, rule of thumb is 1 to 4 months.")

    rows.sort(key=lambda r: r[0])
    print(f"Release {release.isoformat()} ({release.strftime('%A')}), reference date {today.isoformat()}\n")
    print(f"{'Date':<12} {'Step':<56} Type")
    print("-" * 110)
    for d, what, kind in rows:
        flag = "  <- MISSED" if d < today and kind.startswith("hard") else ("  <- past" if d < today else "")
        print(f"{d.isoformat():<12} {what:<56} {kind}{flag}")

    if release.weekday() >= 5:
        warnings.append("Release falls on a weekend. Indies usually launch Monday to Thursday.")
    if fee_latest < today or coming_soon_latest < today:
        warnings.append("At least one hard deadline has passed. Move the release date.")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")
    print("\nNote: re-check values in the Steamworks docs before committing to a plan.")
    return 1 if (fee_latest < today or coming_soon_latest < today) else 0


if __name__ == "__main__":
    sys.exit(main())
