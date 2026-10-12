# Steamworks rules (official)

As of 2026-10-12, from the Steamworks documentation. Re-check the source before committing to a deadline.

## Account and fee

Source: https://partner.steamgames.com/doc/gettingstarted/onboarding, https://partner.steamgames.com/doc/gettingstarted/appfee

- **Steam Direct fee:** USD 100 per app, non-refundable. Paid back once the app reaches USD 1,000 in Adjusted Gross Revenue.
- **Waiting period:** 21 days between paying the fee and releasing that app (applies to an account's first titles).
- **Tax and identity check:** run by a third party, takes 10 to 15 business days, sometimes with follow-up requests. Tax details can't be changed while it runs.
- The app credit belongs to the account that paid, and only that person can redeem it.
- Non-US developers fill in a W-8BEN (individual) or W-8BEN-E (company) in the tax interview. Check the treaty rate for your country there and ask an accountant if unsure.

## Coming Soon page and reviews

Source: https://partner.steamgames.com/doc/store/coming_soon, https://partner.steamgames.com/doc/store/review_process

- The Coming Soon page must be public for **at least 2 weeks** before release.
- **Store review:** 3 to 5 business days. Submit at least 7 business days before the wanted live date.
- **Build review:** 3 to 5 business days, also plan 7 business days. After approval, updates need no new review.
- Steps: create the app, complete the "Your Store Presence" section of the release checklist, "Mark As Ready For Review", then "Post as Coming Soon" after approval.
- **Store page gets rejected** if it shows content missing at launch, if capsules lack a readable title, if screenshots show no gameplay, or if the description links to other websites.
- **Build gets rejected** if it doesn't start on a listed OS or a listed feature (for example controller, cloud saves, achievements) is missing.

## Demo

Source: https://partner.steamgames.com/doc/store/application/demos

- Own App ID linked to the base game, with its own checklist, depots and build review.
- A separate store page is optional. Without one, only a button shows on the base game page. With one: demo content only, a trailer and at least 5 demo screenshots, capsules must clearly say "Demo".
- After releasing the demo, republish the base game page, or the download button won't show.
- **Wishlist notification for the demo:** possible once, triggered on the demo page, within 2 weeks of the demo first becoming playable.
- Better to leave achievements out of the demo. Store progress in Steam Cloud and grant achievements in the full game later.

## Next Fest

Source: https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest

- Each game can join **only once**. It must be unreleased, have a public store page, and a public demo by the start of the fest.
- Register from the base game, not the demo. Then check for the green tick on the app landing page.
- Submit the demo for review **5 weeks** before for the press preview, otherwise **3 weeks** before at the latest.
- Timeline: developer preview 5 weeks before, press preview 11 days before, trailer 4 days before, then 7 days of fest.
- Editions run in February, June and October. Exact dates and registration deadlines are on each edition's page.

## Wishlist notifications

Source: https://partner.steamgames.com/doc/marketing/wishlist

- Email and push to wishlisters at release (once for Early Access, once for full release).
- For discounts only if the discount is at least 20 %, runs longer than 8 hours and covers the cheapest package.
- At most one email per app every 2 weeks. Space out demo email, launch and discounts.
- Wishlist numbers are in the Sales & Activation Reports, updated daily up to the previous day.

## Discounts and price

Source: https://partner.steamgames.com/doc/marketing/discounts

- **Launch discount:** 10 to 40 %, 7 to 14 days, must be set up before release.
- **Regular discounts:** 10 to 95 %, 1 to 14 days.
- **Blocks:** no discount for 30 days after release (except the launch discount). No discount for 30 days after a price increase. 30 days between two discounts.
- **Seasonal sales** (summer, winter and so on) are exempt from the 30-days-between-discounts rule, but not from the release and price-increase blocks.
- The base price can't be changed while a discount is active or scheduled.

## Art

Source: https://partner.steamgames.com/doc/store/assets/standard, https://partner.steamgames.com/doc/store/assets/libraryassets

| Asset | Size | Required | Rule |
|---|---|---|---|
| Header Capsule | 920 × 430 | yes | title is the only text |
| Small Capsule | 462 × 174 | yes | logo nearly fills the space |
| Main Capsule | 1232 × 706 | yes | title is the only text |
| Vertical Capsule | 748 × 896 | yes | title is the only text |
| Screenshots | min. 1920 × 1080, 16:9 | min. 5 | gameplay only, mark 4 as suitable for all ages |
| Page Background | 1438 × 810 | no | calm, not distracting |
| Library Capsule | 600 × 900 | yes | title is the only text |
| Library Header | 920 × 430 | no | falls back to the header capsule |
| Library Hero | 3840 × 1240 | yes | no text, keep key content in the centre (860 × 380) |
| Library Logo | 1280 wide and/or 720 tall | yes | transparent PNG, logo only |

No quotes, awards or marketing copy on capsules. Time-limited text (for example "Out now") goes into artwork overrides, which expire automatically.

## AI content disclosure

Source: the Content Survey in Steamworks (section on AI generated content). Valve reworked the rules in January 2026.

- Disclose what players see or hear: in the game, on the store page, in marketing. Split into pre-generated (made during development) and live-generated (made while playing).
- Pure development helpers (code assistants, unshipped concept sketches) need no disclosure.
- Example: AI-translated in-game text is visible, pre-generated content and belongs in the disclosure.
- Read the current wording in the survey before filling it in. The developer stays liable for copyright.
