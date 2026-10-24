# Hermes edition (fork of anis-marrouchi/gps-system)

This fork runs the GPS system inside a [Hermes Agent](https://github.com/NousResearch/hermes-agent)
profile that coaches one owner over Telegram, instead of Claude Code + launchd.

What changed:

- `skills/` is the canonical Hermes skill set (point `skills.external_dirs` at it).
  `.claude/skills/` and `system/` are the untouched upstream Claude Code layout.
- New `skills/gps-core/` carries what used to live at the repo root (operating
  manual, method, science notes, goal template), because Hermes loads skills one
  directory at a time.
- Data lives in `~/coach/` (the profile's working directory), not `data/`.
- Delivery goes through Hermes (chat replies and cron deliveries); no wacli/mail
  dispatch, no dashboard (`gps-dashboard` removed from `skills/`).
- `gps-daily` is a whole day loop (wake plan, block reminders, check-ins,
  deviation re-plans, evening review that plans tomorrow, bedtime) driven by one
  15-minute cron job with a zero-cost pre-check script
  (`skills/gps-daily/scripts/coach_tick.py`, copy it into `$HERMES_HOME/scripts/`).
- `gps-onboard` adds a 4-round discovery interview (adapted from
  BayramAnnakov/2026-coach) before goal setting.
- `gps-monthly` became a 4-week checkpoint inside the 12-week cycle.
- Intensity levels (push / steady / rebuild / reset-talk), adapted from
  Paitesanshi/ClawBoss, live in `gps-core`.
- The partner never gets messages from the agent; the owner forwards a drafted
  report himself.
- Owner-facing messages are in Simplified Chinese.

Companion skills used by these rituals: `chronoplanner` (fork:
ccc592/chronoplanner), `life-coach` (fork: ccc592/agent-skills), `activitywatch`
(fork: ccc592/activitywatch-analysis-skill), and Hermes' bundled
`google-workspace` for Calendar.
