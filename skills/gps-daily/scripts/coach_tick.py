#!/usr/bin/env python3
"""Pre-check gate for the coach-tick cron job (Hermes `script=` / wakeAgent).

Runs every 15 minutes. Reads ~/coach/config.json, today's plan JSON and
~/coach/.tick_state.json, decides whether a coach event is due, and prints ONE
JSON line on stdout:

    {"wakeAgent": false}                                   -> nothing due, no LLM call
    {"wakeAgent": true, "context": {"event": "...", ...}}  -> agent runs gps-daily

Events (each sent at most once per coach day):
    wake-fallback   wake target + 60 min and no wake recorded
    block-start     a planned deep/shallow block starts (only if calendar is off)
    check-in        a deep block ended
    evening-review  plan.evening_review (default sleep target - 90 min)
    bedtime         plan.bedtime_nudge (default sleep target - 30 min)

A coach day runs until 04:00 the next morning; clock times before 04:00 belong to
the previous date. Stdlib only. Set COACH_NOW (ISO time) to test: that is a dry
run and never records events as sent (COACH_HOME points it at another data dir).
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

COACH = Path(os.environ.get("COACH_HOME", Path.home() / "coach"))
ROLLOVER_MIN = 4 * 60     # coach day ends at 04:00
WINDOW = timedelta(minutes=20)  # an event is due from its time until +20 min
QUIET = {"wakeAgent": False}


def out(obj):
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(0)


def load(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def minutes(value):
    """'13:30' -> minutes from the coach-day midnight; '00:30' -> 1470."""
    try:
        h, m = str(value).split(":")[:2]
        total = int(h) * 60 + int(m)
    except (ValueError, AttributeError):
        return None
    return total + 24 * 60 if total < ROLLOVER_MIN else total


def main():
    cfg = load(COACH / "config.json")
    if not cfg:
        out(QUIET)  # not onboarded yet
    tz = ZoneInfo(cfg.get("timezone") or os.environ.get("HERMES_TIMEZONE") or "Asia/Taipei")
    now = datetime.fromisoformat(os.environ["COACH_NOW"]).replace(tzinfo=tz) if os.environ.get("COACH_NOW") \
        else datetime.now(tz)
    coach_day = (now - timedelta(minutes=ROLLOVER_MIN)).strftime("%Y-%m-%d")
    midnight = datetime.strptime(coach_day, "%Y-%m-%d").replace(tzinfo=tz)

    if cfg.get("paused_until") and coach_day <= str(cfg["paused_until"]):
        out(QUIET)

    day_cfg = cfg.get("day", {})
    plan = load(COACH / "plans" / f"{coach_day}.json", {}) or {}
    state = load(COACH / "state.json", {}) or {}
    state_path = COACH / ".tick_state.json"
    tick = load(state_path, {}) or {}
    sent = set(tick.get(coach_day, []))
    calendar_on = bool((cfg.get("calendar") or {}).get("enabled"))

    candidates = []  # (minutes, key, extra context)

    wake_planned = plan.get("wake_planned") or day_cfg.get("wake_target") or "12:00"
    woke = plan.get("wake_actual") or (state.get("wake") or {}).get(coach_day)
    wake_m = minutes(wake_planned)
    if wake_m is not None and not woke:
        candidates.append((wake_m + 60, "wake-fallback", {"wake_planned": wake_planned}))

    for b in plan.get("blocks", []):
        start, end = minutes(b.get("start")), minutes(b.get("end"))
        if start is None or end is None:
            continue
        if end < start:
            end += 24 * 60
        status = b.get("status", "planned")
        if b.get("kind") in ("deep", "shallow") and not calendar_on and status == "planned":
            candidates.append((start, f"block-start:{b.get('id')}", {"block": b}))
        if b.get("kind") == "deep" and status in ("planned", "moved"):
            candidates.append((end, f"check-in:{b.get('id')}", {"block": b}))

    sleep_m = minutes(plan.get("sleep_target") or day_cfg.get("sleep_target") or "00:00")
    if sleep_m is not None:
        ev = minutes(plan.get("evening_review")) if plan.get("evening_review") else sleep_m - 90
        bed = minutes(plan.get("bedtime_nudge")) if plan.get("bedtime_nudge") else sleep_m - 30
        candidates.append((ev, "evening-review", {}))
        candidates.append((bed, "bedtime", {}))

    due = []
    for mins, key, ctx in candidates:
        at = midnight + timedelta(minutes=mins)
        if key not in sent and at <= now < at + WINDOW:
            due.append((at, key, ctx))
    if not due:
        out(QUIET)

    due.sort(key=lambda x: x[0])
    at, key, ctx = due[0]
    if not os.environ.get("COACH_NOW"):  # simulated time = dry run, keep real state
        sent.add(key)
        tick[coach_day] = sorted(sent)
        for old in sorted(tick)[:-7]:  # keep a week of dedupe state
            tick.pop(old, None)
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(tick, ensure_ascii=False), encoding="utf-8")
        tmp.replace(state_path)

    context = {
        "event": key.split(":")[0],
        "coach_day": coach_day,
        "now": now.strftime("%Y-%m-%d %H:%M"),
        "scheduled_for": at.strftime("%H:%M"),
        "has_plan": bool(plan),
        "calendar_enabled": calendar_on,
    }
    context.update(ctx)
    out({"wakeAgent": True, "context": context})


if __name__ == "__main__":
    main()
