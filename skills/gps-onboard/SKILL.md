---
name: gps-onboard
description: "Start a 12-week GPS cycle in conversation: discovery interview, owner profile, up to 3 goals with anti-goals, milestones, 80% checks, WOOP and if-thens; then files, scorecard and the coach schedule. Use for first-time setup, '帮我定目标', '开始新周期'."
metadata:
  hermes:
    tags: [goals, onboarding, coaching, planning]
    related_skills: [gps-core, gps-daily, chronoplanner, life-coach]
---

# GPS Onboard — start a 12-week cycle (Hermes edition)

Load `gps-core` first and follow it (language, tone, data layout, hard rules). Read
`gps-core/references/method.md` before step 3. This is an **interactive** ritual in a
chat session: ask in plain conversation, 2–4 related questions per message, wait for
the answer. Never invent the owner's goals, history or numbers.

It can span several messages or even days. Keep progress in `~/coach/onboarding.md`
(phase reached + notes) so a later turn can resume where it stopped; delete it at
the end.

## Phase 0 — Already onboarded?

If `~/coach/config.json` and an active cycle exist, ask whether this is a new cycle
(→ `gps-reset` first) or a change to one goal (→ `gps-goal`). Stop here unless the
owner confirms a fresh start.

## Phase 1 — Discovery interview (adapted from 2026-coach)

Purpose: understand the person before any goal is written. Four rounds; reflect
back what you heard in 2–3 sentences after each round before moving on.

1. **Current state** — what they do now, how a normal day actually goes (wake,
   sleep, fixed commitments such as the gym), money/time/energy constraints, what
   they spend most hours on (be specific: feeds, video, chat).
2. **Vision** — where they want to be in 1 year and in 3–5 years; what success
   looks like in their own words; the ONE thing that would make them proud looking
   back; what kind of person they want to be.
3. **Strategy** — biggest bet for the coming year; what worked before and should
   continue; what failed and should stop; what would make this year different.
4. **Process** — realistic daily hours for focused work (the honest number, not the
   hopeful one); which daily behaviours would move the needle; biggest time sinks
   and when they hit; best and worst hours of the day.

Then **synthesize**: name the patterns you see, the core tension (e.g. "lots of free
time, little protected time"), and propose a one-year direction in one sentence.
The owner confirms or corrects it. Write `~/coach/vision.md`:

```
# 方向 (confirmed YYYY-MM-DD)
一年后: ...
三到五年: ...
最想成为的人: ...
核心矛盾: ...
年度主线: ... (Q1..Q4 milestones, one line each)
```

## Phase 2 — Profile and config (first run only)

Write `~/coach/profile.md` from Phase 1 plus these questions:

- Follow-through history: when do they deliver (deadlines? bursts? after a push
  from someone?), how do plans usually die (drift week, shiny objects, overload,
  late nights, phone in bed).
- **Obstacle classes** — name 3–5 recurring ones in their words (e.g. 刷抖音/推特,
  熬夜, 起床后赖床刷手机, 没有截止日期就拖). Every goal's if-thens must cover these.
- Base rate: of the last few plans they made, roughly how many did they follow for
  two weeks? (Used by the second 80% check.)
- Daily structure: current wake/sleep, gym time and days, preferred hours for hard
  work. Store as observed facts, not targets.

Write `~/coach/config.json` from the `gps-core` schema, filling `day.*` from the
answers (keep defaults where they have no preference). Tone defaults to
`full-scorecard` for this owner unless they ask otherwise.

Seed `~/coach/goals/anti-goals.md` with standing guardrails from the answers, each
measurable, for example:

```
- 睡眠: 不为任何目标熬到 01:30 之后 (每晚检查)
- 健身: 每周至少 5 次，不因工作取消
- 信息流: 深度块期间不开抖音/推特 (ActivityWatch 可核对)
```

Initialize `~/coach/state.json`: `{"intensity": "steady", "streak_deep_days": 0,
"last": {}}`.

## Phase 3 — Goals (divergent → convergent)

1. Ask what would make the next 12 weeks a win, tied to the yearly direction in
   `vision.md`. Push vague answers toward a metric.
2. **Enforce the cap**: max 3 goals (suggested: 1 main work/skill/income goal, 1
   health or life goal, 1 optional — an empty third slot is a good choice).
   Everything else → `~/coach/parking-lot.md`, said explicitly.
3. For EACH goal, walk `gps-core/templates/goal-template.md`:
   - Specific measurable outcome; **learning-goal override** for novel work ("run N
     experiments and document results", not a performance number).
   - Identity why, one sentence ("我是一个……的人").
   - Milestones: 3–5, with dates inside the 12 weeks; the 4-week checkpoints should
     each have something checkable.
   - The two **80% checks** — the owner scores them; below 80% → shrink and re-score
     using the base rate in `profile.md`.
   - **WOOP**: pre-mortem ("第 12 周，这个目标失败了，原因是什么？"), then ≥3
     if-thens covering the obstacle classes.
   - **Process target**: the daily/weekly behaviour the owner fully controls (e.g.
     "每天一个 90 分钟深度块做 X"). This is what daily plans schedule.
   - **Operating procedure (machine test)**: if the goal is reached by repeating a
     unit of work whose steps the milestones don't spell out, write the ordered
     steps for ONE unit; otherwise delete the section.
4. Read every goal back in one compact summary; get an explicit "确认".

## Phase 4 — Write files

- Cycle id = `C<start date>` (start = the next Monday, or today if the owner wants
  to start now). Create `~/coach/goals/<cycle>/g<N>-<slug>.md` per goal, fully
  filled.
- `~/coach/tracking/scorecard.md`: goals × W1–W12 with real week dates + an anti row.
- `~/coach/tracking/YYYY-MM.md` with a header line explaining the format (see
  `gps-core`).
- Record `cycle_id`, `cycle_start` in `config.json`.

## Phase 5 — Turn on the rhythm

1. Tell the owner, in 5–6 short lines, how a day works: he says "起床了" → today's
   plan; reminders at block starts (Google Calendar once connected, otherwise
   Telegram); short check-ins after each deep block; evening review with tomorrow's
   plan; bedtime nudge; Sunday weekly review.
2. Create the coach's scheduled jobs with the cron tool — exactly the set defined in
   `gps-daily` → "Scheduled jobs". Replace existing coach jobs with the same names
   instead of duplicating them. Confirm the list back.
3. Make the first plan: load `chronoplanner` and plan the next day (or the rest of
   today if it is early enough), honouring `config.day` and the goals' process
   targets.
4. Delete `~/coach/onboarding.md`. Close with the single next action per goal.
