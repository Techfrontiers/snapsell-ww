# SnapSell WW — brainstorm repo

Snap a photo of a product, get a ready-to-post listing card back:
**SAM 3.1** cuts the product out → **Muse Image** makes a studio shot →
**Muse Spark** writes the listing copy. All through the Meta Model API.

This repo is the **worldwide (WW) brainstorm space** for SnapSell.
The original build lives at https://github.com/Techfrontiers/snapsell-ai
and the live demo gallery at https://snapsell-demo.pages.dev/.

## Scope rule — read this first

**Worldwide, NOT Thai-only.** The idea started from a Thai seller problem
the founder knows firsthand, but the product, the pitch, the demo and
the copy must serve small sellers **anywhere in the world**.

- Listing language is a **parameter**, never hardcoded to Thai.
  The demo must prove at least English + Thai, and be built to add more.
- Export targets include Asian marketplaces (Shopee, Lazada, TikTok Shop)
  **and** worldwide ones (Etsy, eBay, Shopify). Never one region only.

## What is already proven (do not redo, build on it)

- Full pipeline tested on 5 real photos: segmentation + studio shot +
  listing copy, labels preserved on all 5.
- Cost ≈ $0.02/photo from the $150 Meta Model API credits.
- SAM concept must be a concrete noun ("product" returned empty for
  some photos; a concrete noun fixed it).
- The demo gallery is static for now (the live-upload pipe is closed).

## Hackathon facts

- Meta Global AI Developer Hackathon, **Indie track**, submission via
  Cerebral Valley before **Nov 5, 2026, 09:00 Bangkok**
  (Nov 4, 9:00 PM ET).
- Judging rubric: Impact 30% / Use of Meta AI Tooling 25% / Demo 25% /
  Technical Depth & Execution 20%.
- Project themes: **Build for Your World** (this project — a problem
  known firsthand, in the founder's domain) and Push the Frontier.
- There are **no specific problem statements** — the themes above are
  the whole brief. A pivot is not forced by the rules.

## Hard rules for anything proposed here

1. **Never invent facts.** No guessed price, spec, or availability.
   Known failure to guard against: a model once invented
   "available at 7-Eleven" when the packaging said no such thing.
   Unknown = say unknown.
2. **No secrets in this repo.** No API keys, tokens, or credentials, ever.
3. Estimate effort in **rounds** (build-test-fix rounds), not hours.

## GPT brainstorm task

Propose **3–4 next features**, ranked by score-impact ÷ difficulty,
feasible before the Nov 5 deadline. Write them in
`brainstorm/ideas.md` — one short section per feature:
what it is, who it helps worldwide, impact, difficulty, rounds.
Keep it short and concrete. Do not rewrite this README.
