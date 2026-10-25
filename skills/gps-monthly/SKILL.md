---
name: gps-monthly
description: "4-week GPS checkpoint (weeks 4, 8, 12 of a cycle): trends per goal, milestone drift, anti-goal and time trends, route changes allowed, reset reminder at week 12."
metadata:
  hermes:
    tags: [checkpoint, review, goals]
    related_skills: [gps-core, gps-weekly, gps-reset]
---

# GPS Checkpoint — every 4 weeks (Hermes edition)

Runs every
`config.checkpoint_every_weeks` cycle weeks (default 4), right after that Sunday's
weekly prep. Load `gps-core` first. Read the period's weekly reviews, tracking files,
scorecard, goal files, `changes.md` for the period, and `aw/` summaries if present.

## Steps

1. **Write `reviews/checkpoint/<cycle>-W<nn>.md`**:
   - Per goal: trend over the 4 weekly %s, milestones hit vs planned, cumulative
     drift in days.
   - Anti-goal trends by week; apply any escalation rules defined in
     `goals/anti-goals.md`.
   - Time trends: deep hours per week, wake-time drift toward `wake_goal`, phone and
     desktop distraction per week.
   - Verdict per goal in the configured tone.
   - Parking-lot growth (a rising count mid-cycle is a signal, not a failure).
2. **Route review** (proposals, applied only after the owner agrees in chat): move
   milestone dates, change the operating procedure, change the daily structure
   (block count, times). Goals themselves do not change here — that is `gps-reset`
   or the guarded replace path in `gps-goal`.
3. **Reset reminder**: at week 12 state that `gps-reset` is due this week.
4. Append to the weekly summons (same delivered message), 2–4 extra lines, worst
   news first, prefixed `【四周检查】`.
