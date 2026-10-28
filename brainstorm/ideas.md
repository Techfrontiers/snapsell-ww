# Brainstorm ideas — SnapSell WW

Ranked for the Meta Global AI Developer Hackathon (Indie track), due Nov 5, 2026, 09:00 Bangkok. Scores are planning estimates, not measured results. Impact is 1–5 (higher is better); difficulty is 1–5 (higher is harder). Priority = impact ÷ difficulty. Effort is estimated in build-test-fix rounds, not hours.

## Idea 1 — Evidence-first listing copy with an “unknown” guardrail

- **What it is:** Generate listing copy only from visible packaging/product evidence and user-provided facts. If a price, material, size, certification, compatibility, or availability is not supported, omit it or mark it unknown instead of guessing. Add a compact “Needs confirmation” list for missing facts; use the known 7-Eleven hallucination as a regression test.
- **Who it helps worldwide:** Sellers in any market who need persuasive copy without fabricated claims that could mislead customers.
- **Hackathon impact:** Strong trust/safety story and clear product value; directly demonstrates deliberate use of the AI pipeline rather than generic copy generation.
- **Impact:** 5/5
- **Difficulty:** 2/5
- **Priority (impact ÷ difficulty):** 2.5
- **Rounds:** 2–3 (build the guardrail and evidence/missing-facts output; test on varied products and languages; fix unsupported claims).

## Idea 2 — English/Thai language switch using one shared pipeline

- **What it is:** Make listing language an explicit input parameter, not a Thai-only prompt. Add a visible English/Thai switch to the demo and run the same product through both languages while preserving product facts and label details.
- **Who it helps worldwide:** Sellers who list in more than one language, including Thai sellers reaching international buyers and global sellers localizing listings.
- **Hackathon impact:** Makes the “worldwide, not Thai-only” promise visible in the demo and gives judges an immediate, easy-to-understand comparison.
- **Impact:** 5/5
- **Difficulty:** 2/5
- **Priority (impact ÷ difficulty):** 2.5
- **Rounds:** 2–3 (parameterize language; test both languages on the same products; fix factual drift and layout issues).

## Idea 3 — Marketplace-ready export profiles

- **What it is:** Offer clearly labeled copy/export templates for Shopee, Lazada, TikTok Shop, Etsy, eBay, and Shopify. Adapt field names and copy structure per destination; do not claim live publishing or platform API integration unless it is actually implemented and tested.
- **Who it helps worldwide:** Small sellers who reuse product content across Asian and global marketplaces.
- **Hackathon impact:** Proves the product is designed for multiple markets and makes the output more actionable than a single generic listing card.
- **Impact:** 4/5
- **Difficulty:** 3/5
- **Priority (impact ÷ difficulty):** 1.33
- **Rounds:** 2–3 (define conservative templates; test copy/export for each destination; fix confusing or unsupported fields). Treat platform-specific requirements as unverified until checked against official documentation.

## Idea 4 — A focused live demo with a visible before/after and cost note

- **What it is:** Build a short, reliable demo path around one product image: original photo → cut-out/studio result → listing copy, with English/Thai output and a clear note that the tested pipeline cost was approximately $0.02/photo based on current project evidence. Keep a prepared fallback gallery if live upload is not stable.
- **Who it helps worldwide:** Judges and prospective users who need to understand the workflow and value quickly.
- **Hackathon impact:** Directly supports the Demo rubric and reduces the risk of a live failure; the existing gallery is static and live upload is currently closed, so do not make live upload a dependency unless it is proven stable.
- **Impact:** 5/5
- **Difficulty:** 3/5
- **Priority (impact ÷ difficulty):** 1.67
- **Rounds:** 2–3 (script the demo and fallback; rehearse on multiple images; fix failure points and verify every claim shown).

## Recommended order

1. **Idea 1 — Evidence-first guardrail** (2.5)
2. **Idea 2 — English/Thai switch** (2.5)
3. **Idea 4 — Reliable demo path** (1.67)
4. **Idea 3 — Marketplace export profiles** (1.33)

Ideas 1 and 2 tie on the simple ratio; prioritize the evidence guardrail first because fabricated product claims are an explicit known failure mode. These are scope recommendations, not claims that the features are already implemented. Keep the demo narrow, verify each change, and do not rewrite README.md.
---

## Strategic direction — make SnapSell more than an AI image-and-copy wrapper

**Core product thesis:** SnapSell should help small sellers turn one real product photo into a marketplace-ready listing while preserving product truth. The differentiator to test is not “AI makes prettier pictures”; it is **trustworthy product transformation**: improve presentation, generate localized copy, and clearly separate supported facts from unknowns.

This is a strategic direction to validate, not a claim that the product already guarantees perfect fidelity or is unique in the market.

### The experience we want to demonstrate

1. **Start with the real product:** show the original photo and preserve identifiable details such as label, logo, color, and shape as far as the current pipeline allows.
2. **Improve presentation:** use the existing Meta AI image pipeline for cut-out/studio presentation. Do not promise perfect preservation; test for changes and disclose limitations.
3. **Write from evidence:** generate listing copy from visible evidence and seller-provided facts. Do not invent price, material, size, certification, compatibility, stock, or retailer availability.
4. **Expose uncertainty:** show a short “Needs confirmation” list for important missing facts and let the seller provide them. Avoid making the listing so cautious that it becomes empty.
5. **Localize without changing truth:** use a language parameter (demonstrate English + Thai) and check that product facts remain consistent across both outputs.

### Why this could improve the hackathon submission

- **Impact (30%):** addresses the real work and risk small sellers face when preparing product listings.
- **Meta AI tooling (25%):** demonstrates a connected workflow using the existing Meta AI pipeline for segmentation, image generation, and listing copy, rather than presenting isolated model calls.
- **Demo (25%):** a clear original → improved image → English/Thai copy → supported facts/unknowns story is easy to understand quickly.
- **Technical depth & execution (20%):** show how evidence, missing facts, and regression tests are handled. Technical depth should come from reliable orchestration and evaluation, not unnecessary complexity.

These are strategic arguments, not guaranteed judging outcomes. Do not claim competitor uniqueness or measured improvements without evidence.

## Implementation brief for Mina (Muse agent)

**Work only in the actual app repo:** https://github.com/Techfrontiers/snapsell-ai
**Use this repo (snapsell-ww) for strategy and review notes. Do not modify README.md.**

### Phase 0 — inspect before coding

- Inspect the current prompt/schema, Meta AI pipeline, listing-generation flow, and UI.
- Identify exact files/functions that would implement the evidence-first guardrail and language parameter.
- Check current branch/status and existing tests. Preserve the working pipeline tested on five real photos.
- Report findings, likely risks, and a minimal build-test-fix plan before broad changes. Do not invent APIs or claim a feature works without running it.

### Phase 1 — evidence-first guardrail (priority 1)

- Distinguish facts supported by the image from facts supplied by the seller and facts that remain unknown.
- Never fill unknown price, size, material, certification, compatibility, or availability with guesses.
- Provide a compact “Needs confirmation” section and a simple way for the seller to supply missing facts if the existing UI allows a minimal change.
- Avoid over-restricting the copy: use confirmed facts to write useful copy even when optional details are unknown.
- Add a regression case for the known false claim “available at 7-Eleven”; it must not be emitted unless explicitly supported by input.
- Test a small varied set of products, including packaging with labels, and inspect output for invented claims.

### Phase 2 — language parameter (priority 2)

- Make listing language an explicit parameter rather than hardcoding Thai.
- Demonstrate English and Thai for the same product and compare facts across outputs.
- Do not describe the product as supporting every language; English + Thai are the demo examples and the parameter is designed to allow more.
- Test for factual drift between languages and fix any differences that change product claims.

### Phase 3 — demo packaging (priority 3)

- Combine the proven results from Phases 1 and 2 into a short, repeatable demo: original photo → improved image → English/Thai listing → confirmed facts and unknowns.
- Keep a static-gallery/video fallback. Live upload is currently closed according to the strategy brief; do not make reopening it a dependency unless its stability is demonstrated.
- If mentioning approximately $0.02/photo, label it as an observed cost from the existing test, not a guaranteed price for every image.

### Scope control and reporting

- Export profiles for six marketplaces are **not a priority**. Only consider a small format preview (for example, Shopee + Etsy) after Phases 1–3 are working and only if time remains. Do not claim live publishing or verified platform compatibility without checking official documentation.
- Estimate work in build-test-fix rounds, not hours. Reserve time for final submission and demo recording before the deadline.
- Never add secrets to any repository.
- After each phase, report: files changed, behavior changed, tests actually run and results, remaining risks, and the next proposed action. Do not claim tests passed if they were not run.
