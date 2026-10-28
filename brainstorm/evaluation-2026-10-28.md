# Meena evaluation — GPT's 4 ideas (2026-10-28)

Review of `brainstorm/ideas.md` for the Meta Global AI Developer
Hackathon, Indie track. Deadline: **Nov 5, 2026, 09:00 Bangkok**
(Nov 4, 9:00 PM ET). Rubric: Impact 30% / Use of Meta AI Tooling 25% /
Demo 25% / Technical Depth & Execution 20%.

This file is the evaluation itself, for GPT review. No code was changed.

## Verdict

Mostly agree with GPT's ranking, with one cut:
**do 1 → 2 → 4 → 3 (minimal version only).**

## Idea 1 — Evidence-first listing copy with an "unknown" guardrail: DO FIRST

- Strongest fit. It fixes a known real failure (the model once invented
  "available at 7-Eleven" when the packaging said no such thing) and
  gives a trust/safety story judges remember, unlike generic copy tools.
- Low difficulty (prompt + output schema + "Needs confirmation" list).
  2–3 rounds is realistic.
- Risk: a guardrail that is too strict leaves thin, empty copy.
  Mitigation: add a user-facts input so the seller can supply what the
  photo does not show.

## Idea 2 — English/Thai language switch, one shared pipeline: DO SECOND

- Makes the "worldwide, not Thai-only" promise visible in seconds.
  Low difficulty (language as a parameter + a visible switch).
- Must come after Idea 1: without the guardrail first, two languages
  multiply hallucinations into two languages instead of one.
- Risk: do not sell this as "worldwide support" from only 2 languages.
  Frame it as a language parameter, with English + Thai shown as proof.
  Test the same product in both languages for factual drift.

## Idea 4 — Focused live demo with before/after and cost note: DO THIRD

- Demo is 25% of the score, so this is worth doing — but as packaging
  for Ideas 1 + 2, not as a separate build, and only after 1 + 2 exist.
- The live-upload pipe is currently closed (server + tunnel stopped
  Oct 27). Reopening it risks burning rounds on stability.
  GPT's hedge is correct: keep a fallback gallery, and do not depend on
  live upload unless it is proven stable. A pre-recorded demo video
  from Ideas 1 + 2 is the safer path.
- The $0.02/photo figure must be labelled as cost measured from past
  tests, not a promise that every photo costs the same.

## Idea 3 — Marketplace-ready export profiles (6 platforms): CUT TO MINIMAL

- Disagree with GPT's Impact 4/5: export templates are convenience,
  not core value. They score low on Meta AI Tooling (formatting, not
  model use) and low on Technical Depth.
- Platform requirements are still unverified against official docs.
  Doing all 6 in the remaining time is a scope-creep trap and risks
  claiming compatibility that is not real.
- Decision: if rounds remain after 1 + 2 + 4, build at most
  **2 profiles (e.g. Shopee + Etsy) as a structure proof**, clearly
  labelled "format preview, not live publishing". If no rounds remain,
  cut it and list it as future work in the submission.

## Overall risks

- About 7 days left. Ideas 1 + 2 + 4 take roughly 6–9 rounds, which is
  feasible — but reserve the last day for the demo video and the
  submission itself. Do not build on the night of Nov 4.
- Doing Idea 3 in full would push the total to roughly 8–12 rounds
  and collide with the deadline.
- The $150 Meta credits are not a risk (spent well under $1 so far).
  The real risks are rounds spent and demo stability, not cost.
