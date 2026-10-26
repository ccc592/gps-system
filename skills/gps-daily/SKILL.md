---
name: gps-daily
description: "The coach's daily rhythm: wake-up plan ('起床了'), block reminders, post-block check-ins, '我偏了' re-plans, evening review that plans tomorrow, bedtime nudge, and the scheduled jobs that drive them."
metadata:
  hermes:
    tags: [daily, coaching, check-in, review, planning]
    related_skills: [gps-core, chronoplanner, life-coach, activitywatch]
---

# GPS Daily — the day loop (Hermes edition)

Load `gps-core` first. Every mode reads: `~/coach/config.json`, `state.json`, the
active goal files, `goals/anti-goals.md`, today's `plans/<day>.json` + `.md`, and
the last 7 lines of `tracking/YYYY-MM.md`.

**Coach day**: a day runs until 04:00 the next morning. Anything before 04:00
belongs to the previous date (a 00:40 bedtime is part of yesterday).

**Clock times**: never state a time you have not just computed with
`TZ=Asia/Shanghai date '+%F %T %a'`. Bare `date` on this host returns UTC — 8 hours
behind him — and a scheduled delivery carries the time it was *generated*, not the
time it is read. See the `coach-clock` skill.

## Hard rule — write it down the moment he says it

The scheduler and the check-ins read **only** the files. A fact that lives in the
conversation does not exist to them, and the message that follows from the gap is
usually a wrong one sent to his phone.

- **Any** statement that he is up — "起床了", "醒了", "早", "我已经起来了",
  "我9点就起来了", said anywhere in the conversation, in any wording — is a wake
  record. Immediately set `wake_actual` in `plans/<coach_day>.json` **and**
  `state.json → wake[<coach_day>]`, before writing anything back to him.
  Otherwise `wake-fallback` fires at `wake_planned + 60` and tells a man who has
  been up for two hours that he is an hour late.
- Same for block progress mentioned in passing ("我先做饭", "这一块做完了", "现在
  开始第一个块"): update that block's `status` / start-end in the plan JSON in the
  same turn, never deferred to the evening review. When a block's times move, edit the
  matching line in `plans/<coach_day>.md` too and re-sync that one calendar event
  (`chronoplanner` → Calendar & Output Integrations).
- Recording costs one small atomic write. Do it first, talk second.

## Plan files (written by `chronoplanner`)

`plans/YYYY-MM-DD.md` is the readable plan. `plans/YYYY-MM-DD.json` is what the
scheduler and the check-ins read:

```json
{
  "date": "2026-10-26",
  "wake_planned": "12:00",
  "wake_actual": null,
  "sleep_target": "00:00",
  "evening_review": "22:30",
  "bedtime_nudge": "23:30",
  "blocks": [
    {"id": "b1", "start": "13:30", "end": "15:00", "kind": "deep", "title": "…", "goal": "g1", "status": "planned"},
    {"id": "gym", "start": "15:30", "end": "18:30", "kind": "anchor", "title": "健身"},
    {"id": "b2", "start": "19:30", "end": "21:00", "kind": "deep", "title": "…", "goal": "g2", "status": "planned"}
  ],
  "calendar_event_ids": []
}
```

`kind` is `deep`, `shallow`, `anchor` (gym, meals, fixed), or `break`. `status` is
`planned` → `done` / `partial` / `missed` / `moved`. Times after midnight (`00:30`)
belong to the same coach day.

## Mode: wake — owner says he is up ("起床了", "醒了", "早")

1. Record `wake_actual` (now) in today's plan JSON and in `state.json`. Read last
   night from the Apple Watch (`gps-core` → Apple Watch data): asleep time, wake
   time, total sleep, split sleep yes/no. If the watch says he woke much earlier
   than now, record the watch wake time and mention the gap in one line.
2. No plan for today (evening review was skipped)? Load `chronoplanner` and make one
   now — short, using `config.day` defaults and the goals' process targets.
3. Woke later than `wake_planned`? Shift the not-yet-started blocks by the delay
   (keep the gym anchor where it is unless the owner says otherwise); if the day no
   longer fits, drop the lowest-priority shallow block first, never the first deep
   block. Update the calendar events if calendar is enabled (chronoplanner →
   Calendar sync).
4. Reply `【今日计划】` in ≤8 lines: last night's sleep in one line (watch), wake time
   vs plan (one fact, no lecture), the
   blocks with times, the single lead action per goal, one anti-goal reminder for
   today (e.g. "深度块前 60 分钟不碰短视频"). End with nothing else.

## Mode: wake-fallback (scheduled, owner has not checked in)

One line, `【起床】`: ask if he is up and remind of the first block time. Do not
repeat it the same day.

## Mode: block-start (scheduled; only when calendar is not enabled)

One line, `【开始】`: block title, end time, "手机放远一点". Nothing else.

## Mode: check-in (scheduled, a deep block just ended)

1. Read the latest `~/coach/aw/<day>.json` (see `activitywatch`, remote coach mode;
   `<day>` is the coach day, 04:00–04:00). If fresh, sum the `summary.slots[]` inside
   the block window: minutes at the computer, productive vs distracting minutes,
   minutes away from the computer, and the `top_distracting` sites. Away is not a
   verdict — state it and ask. If stale or missing, say "没有电脑数据".
2. Send `【打卡】` in ≤4 lines: the block, what the desktop data suggests (one line,
   facts), and one question: done / partial / not started?
3. Do not diagnose yet; a short answer is enough. When he answers (chat turn), mark
   the block `status` in the plan JSON. Not done → one question about what got in
   the way, then either re-slot the work (Mode: deviation) or note it for the
   evening review.

## Mode: deviation — "我偏了", "刚才在刷…", "计划乱了", "来不及了"

No judgment. Load `chronoplanner` → Plan Adjustment Protocol: keep the most
important remaining deep block, re-slot or drop the rest, update calendar events,
send only the changed part of the day. Log one `note:` for the evening review.

## Mode: evening review (scheduled `【晚间复盘】`, finished in chat)

Phase A — the scheduled message (≤6 lines):
- Today in facts: blocks planned vs done (from the plan JSON + replies), desktop
  summary for the day (productive hours, top distracting site + minutes).
- Today's workout from the watch if there was one (type, minutes), one line.
- Ask for: (1) any block he hasn't reported, (2) phone screen time — a screenshot or
  two numbers (total, top app), (3) one line: what got in the way / what worked,
  (4) anything fixed tomorrow (appointments).

Phase B — when he answers (chat turn):
1. **Phone data**: if he sends a screenshot, read the totals from it; if you cannot
   read images, ask for the two numbers instead. Never guess.
2. **Diagnose misses** with `life-coach` → "Review after noncompletion" order
   (still his goal? task too big/vague? capability? opportunity? did the plan
   itself create resistance?). One or two questions, not an interrogation. If the
   desktop data shows feeds during a block, say it plainly once.
3. **Write the tracking line** for today (format in `gps-core`), updating in place.
   `wake` and the previous line's `sleep` come from the watch when it has the night.
4. **Recompute intensity** (`gps-core` → Intensity levels) and update `state.json`.
   If the level changed, say what changes tomorrow in one sentence.
5. **Plan tomorrow**: load `chronoplanner`, plan the next coach day from
   `config.day` (current `wake_target`), the goals' process targets, tomorrow's
   fixed items, intensity level and today's lessons. Write `plans/<tomorrow>.md`
   and `.json`; sync calendar if enabled.
6. Reply `【明日计划】`: the blocks with times + lead action per goal, ≤8 lines, and
   one line of honest assessment of today (fact-based, no shaming, no inflated
   praise).

If he never answers, the next morning's wake mode uses yesterday's defaults and the
next evening review reconciles `?` marks.

## Mode: bedtime (scheduled `【睡前】`)

One or two lines: tomorrow's wake target and first block, "手机放到床够不到的地方".
If a deep block or the review is still open, mention it once — do not start a new
conversation at bedtime.

## Scheduled jobs (created by `gps-onboard`; re-create with these names on change)

All jobs run in the coach profile with workdir `~/coach` and deliver to the owner's
Telegram home chat. Replace existing jobs that have the same name.

1. **`coach-tick`** — schedule `*/15 * * * *`, pre-check script
   `coach_tick.py` (installed in the profile's `scripts/` dir), skills
   `gps-core`, `gps-daily`, `chronoplanner`, `life-coach`, `activitywatch`.
   The script decides which event is due (`wake-fallback`, `block-start`,
   `check-in`, `evening-review`, `bedtime`) from `config.json`, today's plan and
   what was already sent today; it wakes the agent only when something is due, so
   idle ticks cost nothing. Prompt:
   > The pre-check script reported a due coach event (JSON with `event`,
   > `coach_day`, and details). Run gps-daily in that mode and reply with the
   > message for the owner in Chinese. If on reflection nothing should be sent,
   > reply exactly [SILENT].
2. **`coach-weekly`** — schedule `0 21 * * 0` (Sunday 21:00), skills `gps-core`,
   `gps-weekly`, `gps-monthly`. Prompt:
   > Run gps-weekly Mode A (prep run). If this is checkpoint week (cycle week is a
   > multiple of config.checkpoint_every_weeks), also run gps-monthly. Reply with
   > the summons message.

Changing `config.day` or tomorrow's plan never requires editing jobs: the tick
script reads the files each time.
