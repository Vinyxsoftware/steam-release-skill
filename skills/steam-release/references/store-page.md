# Store page

Official requirements and art sizes are in [steamworks-rules.md](steamworks-rules.md). This file is about impact. Everything here is experience from the indie scene, not a Valve rule.

## What people see first

1. **Capsule** (header and small): decides whether anyone clicks at all. The best place to spend money on an artist.
   - Title large and still readable at 184 × 69. One clear subject that shows genre and mood.
   - Successful simulation capsules usually show a person in the middle of the core activity, not an empty building.
   - Test: shrink the capsule and place it next to 10 competitor capsules. Does it stand out, and is the genre obvious?
2. **Trailer:** real gameplay in the first 5 seconds, no logo intro. 30 to 90 seconds. Ends with "Wishlist now" and the title.
3. **First 4 screenshots:** they show on hover in lists. Each one shows a different core mechanic. No menus, no loading screens.
4. **Short description** (around 300 characters): first sentence = genre plus hook. Then 2 or 3 concrete activities. No chains of adjectives.

## Short description pattern

> A [genre] where you [core fantasy]. [Activity 1], [activity 2] and [activity 3] until [goal or escalation].

Example (warehouse simulation):
> A first-person warehouse simulation: you run a robot warehouse. Unload trucks, store goods in the robot grid, pick orders and get every parcel onto the truck on time.

If the project already has store copy or a press kit, read it first and build on it.

## Long description

- Open with a GIF or image of the core mechanic, then 3 to 5 sections with headings, each with a GIF.
- Only features that ship at launch. Leave planned ones out, or the review rejects the page.
- No external links.
- A proper version for every store language, not just English.

## Tags and genre

- Steam allows up to 20 tags. The first tags carry the most weight for recommendations.
- Method: open 5 to 10 successful games in the same niche, compare their tags and take the shared ones.
- Example for a management sim: Simulation, Management, First-Person, Automation, Building, Singleplayer. Always check against comparable games before setting them.

## Languages

- List only languages that are fully in the game.
- Store copy and capsules with text can be set per language.

## Check before submitting

- [ ] `scripts/asset_check.py` passes without errors
- [ ] At least 5 screenshots, gameplay only, 4 marked as suitable for all ages
- [ ] Trailer opens with gameplay
- [ ] No real brands or third-party logos without rights
- [ ] Only features that work at launch (also in the Basic Info tab)
- [ ] Content survey filled in, including AI disclosure
- [ ] System requirements tested on a weaker PC, not just the dev machine
