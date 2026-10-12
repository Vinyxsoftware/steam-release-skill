---
name: steam-release
description: Plans and checks an indie game release on Steam, from the Coming Soon page to post-launch sales. Covers Steamworks deadlines, store page and capsule art, wishlists, demos, Next Fest, pricing and discounts, AI content disclosure, and Godot export with GodotSteam and SteamPipe. Use when the user mentions Steam, Steamworks, a Steam release or launch date, store page, capsule art, wishlists, Next Fest, a demo, Steam Deck, game pricing, or wants to publish a PC game.
---

# Steam Release

For solo and small indie developers bringing a PC game to Steam. Steam rewards lead time: without a store page and wishlists months before launch, even a good game rarely sells.

## Quick start

1. Read the project context first: the repo's `CLAUDE.md` or README, any release milestones, existing store texts and press kit.
2. Find the phase (table below) and load only the matching reference.
3. Work out deadlines and check the art (scripts use the Python standard library only):

```bash
python3 scripts/release_timeline.py --release 2027-09-14 --nextfest 2027-06-14
python3 scripts/asset_check.py marketing/steam   # header.png, main.png, screenshot_01.png ...
```

## Phases

| Phase | Typical question | Reference |
|---|---|---|
| 0 Account | Steamworks account, fee, tax, bank | [steamworks-rules.md](references/steamworks-rules.md) |
| 1 Store page | Capsules, screenshots, trailer, copy, tags | [store-page.md](references/store-page.md) |
| 2 Wishlists | Channels, festivals, devlogs, press | [marketing.md](references/marketing.md) |
| 3 Demo and Next Fest | When, how long, registration | [steamworks-rules.md](references/steamworks-rules.md), [marketing.md](references/marketing.md) |
| 4 Tech | Export, Steamworks API, SteamPipe, Steam Deck | [godot-steam.md](references/godot-steam.md) (Godot; upload and Deck parts apply to any engine) |
| 5 Launch and after | Date, price, launch discount, updates, sales | [marketing.md](references/marketing.md), [steamworks-rules.md](references/steamworks-rules.md) |

## Workflow for a release plan

- [ ] Pick a target launch month, not a day. Fix the day after Next Fest.
- [ ] Run `release_timeline.py` and copy the hard deadlines into the plan.
- [ ] Put the Coming Soon page up as early as possible, rule of thumb 6 to 12 months before launch.
- [ ] Choose a Next Fest: each game can join only once. It helps most 1 to 4 months before launch.
- [ ] Set a wishlist target and compare it monthly with the Steamworks report.
- [ ] Before every review: the page shows only what ships at launch, and the build starts on every listed OS.
- [ ] After launch: plan for the 30-day discount block, then use the seasonal sales.

## Rules for answers

- **Separate official rules from rules of thumb.** Name the source for Valve rules. Always mark community numbers (wishlist targets, conversion) as estimates.
- **Rules change.** Numbers in the references carry an "as of" date. Before committing to a deadline, re-check the linked Steamworks page with a web fetch and tell the user if it changed.
- **No real brands** on capsules, screenshots or in copy unless the project has the rights. Respect the project's own naming rules if it has any.
- **Disclose AI content** that players see or hear, for example AI-translated text. Details in steamworks-rules.md.
- **Recommend concretely:** a date, a size, a sentence of copy or the next step. No list of options without a pick.
- Tax and legal questions (company setup, VAT, trademarks): give orientation only and point to an accountant or lawyer.

## Examples

- "When do I have to pay the fee if I launch in March?" → run the script, show deadlines as a table, mention the 10 to 15 business days tax check.
- "Write my store copy" → load store-page.md, short description around 300 characters, hook in the first sentence, in every store language.
- "Is a demo worth it?" → marketing.md, section Demo and Next Fest.
