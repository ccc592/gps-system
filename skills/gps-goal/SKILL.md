---
name: gps-goal
description: Revise or replace one existing GPS goal mid-cycle, in chat ('改目标', '换目标'). Edit a goal's target, milestones, why, if-thens, or operating procedure — rewritten in place with the owner's OK; or retire a goal and stand up a replacement in its slot, gated by a drift check. The guarded alternative to waiting for /gps-reset.
---

# GPS Goal — revise or replace one goal

Interactive, in chat (Hermes edition) — ask in plain conversation, one decision at a
time. Load `gps-core` first (tone, layout, rules) and read
`gps-core/references/method.md`, `~/coach/config.json`, the active goal files in the
current cycle dir, `~/coach/goals/anti-goals.md`, and `~/coach/profile.md`.

**Two hard rules:** never change or delete a goal without the owner's OK in chat; never
exceed 3 active goals.

## Step 1 — pick the goal and the mode

List the active goals; ask which one. Then ask: **revise** (edit this goal in place) or
**replace** (retire it and stand up a new goal in its slot)?

## A — Revise (edit in place)

2. Ask what changes (one or more): metric/target, a milestone (move / edit / add / drop),
   the why, an if-then, the operating procedure, or scope (shrink).
3. Apply the edits to the goal file. Guardrails:
   - **Shrinking the target** → re-score the second 80% check ("will I actually do it")
     against the base rate in `~/coach/profile.md`; record the new score in `## 80% checks`.
   - **Machine test** → if the change alters whether the goal is reached by repeating a
     unit of work, add or remove the `## Operating procedure` accordingly (fill it, or
     delete it — never leave it blank; no unused circuitry).
   - Don't quietly *expand* scope to dodge a hard week — if that's what's happening, name it.
4. **Rewrite in place**: the goal file shows only the new version, with no change note
   (`gps-core` rule 5).

## B — Replace (retire + new)

2. **Friction check first.** Replacing a goal mid-cycle is the shiny-object move the
   system is built to resist — the `no-new-projects` anti-goal applies, and promotion
   normally waits for `gps-reset`. State this plainly (per config tone) and confirm the
   owner truly wants to replace, rather than **revise** the current goal or **park** the
   new idea. If they hesitate, offer `park this idea: <one line>` and stop.
3. **Close the outgoing goal honestly — never hard-delete.** Score what actually got
   done, set its frontmatter `status:` to `done` / `missed` / `dropped`, harvest one
   lesson into the file (the lesson itself, not the story of the change). A
   non-active status frees the slot (keeping active goals ≤ 3).
4. **Stand up the replacement** in the freed slot via `gps-core/templates/goal-template.md`:
   specific measurable outcome (learning-goal override for novel work), identity why,
   milestones, the two 80% checks, WOOP + ≥3 if-thens covering the profile's obstacle
   classes, and the operating procedure (machine test). Write
   `~/coach/goals/<cycle>/g<N>-<slug>.md`.

## Both paths — close out

5. Update `~/coach/tracking/scorecard.md` (rename/replace the goal's row; keep retired
   goals' closing scores for the record).
6. If the goal's daily process target changed, tomorrow's plan must reflect it: say
   so, and the next evening review plans accordingly.
7. Confirm to the owner: what changed, where it's logged, and the next action.
