---
name: gps-partner
description: Invite, change, or remove an accountability partner — the person who receives the weekly scorecard report (the Matthews mechanism, the single strongest documented lever in the goal literature). Drafts text the owner forwards himself; never contacts the partner.
---

# GPS Partner — accountability setup

The evidence: Matthews (Dominican University) — participants who sent weekly progress
reports to a friend succeeded ~70% vs ~35%. (The "Harvard goals study" people cite for
this never existed.) Harkin et al. 2016: effects of progress monitoring are larger
when progress is made public. This feature IS the system's strongest lever.

Interactive, in chat (Hermes edition). Load `gps-core` first and read
`~/coach/config.json`. The owner forwards the weekly
report to the partner himself (e.g. on WeChat); the coach only drafts it.

## Steps

1. **Explain what the partner gets** (before asking who): one short weekly scorecard
   message — goals, %s, verdicts — sent only after the owner approves it each week.
   Nothing else; no daily traffic; no goal-file access.
2. **Capture the partner**: name (or nickname) and relationship only. No contact
   details are needed or stored.
3. **Draft the invitation** as a plain-text block the owner can paste into WeChat:
   what he is doing (12-week goals), what the partner will receive weekly, what is
   asked (read it; reply with one line if they feel like it — knowing someone reads
   it is the mechanism). The owner sends it himself.
4. **Update `~/coach/config.json → partner`** (`name`, `relationship`,
   `delivery: owner-forwards-via-wechat`) once he says it is sent.
5. **Removal/change**: set partner to null or the new person; confirm; note it in the
   next weekly review.

Never message the partner at all; only draft text for the owner.
