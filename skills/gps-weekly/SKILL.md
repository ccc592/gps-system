---
name: gps-weekly
description: "Sunday GPS review: scheduled prep run computes the scorecard and sends a summons; the owner closes it in chat. Includes the wake-time ramp, next week's if-then, and a WeChat-ready report for the accountability partner."
metadata:
  hermes:
    tags: [weekly-review, scorecard, accountability]
    related_skills: [gps-core, gps-monthly, gps-daily, life-coach, activitywatch]
---

# GPS Weekly — scorecard + review (Hermes edition)

Load `gps-core` first (tone, layout, intensity). Read `config.json`, active goal
files, `goals/anti-goals.md`, this and last month's `tracking/` files, the week's
`plans/*.json`, `aw/*.json` for the week (if any), and last week's review.

Week = Monday–Sunday. Cycle week N = weeks since `config.cycle_start` (+1).

## Mode A — scheduled prep run (non-interactive, Sunday evening)

1. **Compute the week** per goal: % of planned deep blocks done (plan JSON statuses
   + tracking marks), milestone status vs dates, days untouched. Deep hours total vs
   last week. Anti-goal violations, dated. Desktop: average `totals.productive_pct`,
   total `distracting_min`, and the top 2 distracting sites with weekly hours (only if `aw/` files exist). Phone:
   weekly average from the evening reports (if reported). Wake: average actual wake
   time vs target.
   - **Machine check**: a goal reached by repeating a unit of work without a filled
     `## Operating procedure` is an open question, not progress.
2. **Update `tracking/scorecard.md`** (this week's column).
3. **Write the draft** `reviews/weekly/YYYY-Wnn.md`:
   - Scorecard + one-line verdict per goal: `ON TRACK` / `SLIPPING: <fact>` /
     `STALLED: untouched Nd`.
   - Anti-goal violations, dated. Time: deep hours, phone, desktop distraction.
   - Open questions (unreconciled `?` days, milestone re-dates).
   - Next week's WOOP re-check: the most likely obstacle THIS week + its if-then.
   - Wake ramp proposal (see below).
   - **Partner report draft** (if `config.partner.name` is set), marked
     `PENDING OWNER APPROVAL`.
4. **Reply with the summons** (this is the delivered message, ≤6 lines):
   `【周复盘】W<nn>: g1 71% · g2 40% SLIPPING · 深度 9.0h(上周 6.0h) · 手机日均 3.1h · anti: 2 次晚睡。回我开始复盘，10 分钟。`
5. Nothing goes to the partner in Mode A, ever.

## Mode B — completion in chat (the owner answers the summons)

1. Walk the draft in 3–5 short exchanges: reconcile `?` days, confirm/contest
   verdicts, log scope changes in the goal file (shrinking is allowed, silent drift
   is not), set next week's if-then.
2. Goal stalled 2+ weeks → force a decision: recommit (with what change?), shrink,
   or park (park frees a slot only at reset). Use `life-coach` → "Review after
   noncompletion" before deciding.
3. **Wake ramp**: if an active goal file has a week-by-week sleep/wake table (for
   example a sleep goal), that table sets next week's `wake_target` and
   `sleep_target`; the ramp below is only the fallback. Otherwise: if last week's
   average wake was within 30 min of
   `config.day.wake_target` and `wake_target` is later than `wake_goal`, propose
   moving it earlier by `wake_ramp_minutes_per_week` (shift `sleep_target` the same
   amount only if he agrees). If he missed the target by more than 30 min, keep it
   and look at why (bedtime, phone in bed). Apply only on his OK; update
   `config.json` and say the new times.
4. **Intensity**: restate the current level and what it means for next week.
5. **Partner report**: show the draft as one plain-text block he can copy into
   WeChat (no markdown, ≤10 lines, Chinese, facts only — goals, %, verdicts, one
   line of next-week focus; no diary details, no phone data unless he wants it).
   He may edit it. Record in the review whether he said he forwarded it.
6. Mark the review completed and save files. Next week's first plan is made by
   tonight's evening review as usual.
