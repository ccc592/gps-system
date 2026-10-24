---
name: gps-reset
description: 12-week GPS cycle reset, in chat. Scores the closing cycle, harvests lessons, triages the parking lot (promote max 1), re-asks the accountability-partner question, then hands off to /gps-onboard.
---

# GPS Reset — close a cycle, open the next

Interactive, in chat (Hermes edition) — run at week 12 (the week-12 checkpoint
reminds the owner). Load `gps-core` first; read `gps-core/references/method.md`,
`~/coach/config.json`, the cycle's reviews, scorecard, goal files, `vision.md`, and
`~/coach/parking-lot.md`.

## Steps

1. **Score the cycle**: per goal — final metric vs target, milestones hit, honest
   done/missed/partial call (owner's call, your evidence). Anti-goal totals vs the
   baselines in `~/coach/goals/anti-goals.md`.
2. **Harvest lessons** (in conversation): which if-thens fired and worked? Where did
   drift start? Was the plan structure right for this person? Update
   `~/coach/profile.md` if a pattern repeated across goals, and re-check `vision.md`
   (does the yearly direction still hold?).
3. **Triage the parking lot**: list every parked idea; promote **max 1** into the
   next cycle's candidates; move the rest to Archived with a one-line reason.
   Archiving is success, not failure.
4. **Partner check**: if a partner is set, ask whether the weekly WeChat report
   actually happened and helped; if none is set, offer `gps-partner` once — solo
   mode is the documented weaker configuration.
5. **Write `~/coach/reviews/cycle/<cycle>-reset.md`**.
6. **Close out**: set closing goals' `status`; then run `gps-onboard` for the new
   cycle, skipping its discovery and profile phases unless the owner wants them (a
   continuing goal still counts against the cap of 3).
