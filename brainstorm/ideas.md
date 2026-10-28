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
