# SnapSell AI — Project Description (copy-paste ready)

Paste into the Cerebral Valley submission form. Fields the portal does not
have can be skipped — do not invent extra claims to fill them.

## Title

SnapSell AI

## One-liner

One phone photo in, a ready-to-post, evidence-checked product listing out.

## Problem

Small sellers photograph their product, then stall on the listing: writing
a good title and description takes longer than the sale, and AI that fills
the gaps invents prices, features, and availability the seller never stated.
One early live test of this project invented a store availability claim —
that failure shaped the whole design: a listing must never state what
neither the photo nor the seller proves.

## Solution

SnapSell is a phone-photo listing studio. The seller uploads one photo and
optionally adds facts they actually know (brand, variant, size). The system
returns a studio-style product image and a listing draft in Thai or English,
with every unproven item separated into a "needs confirmation" list instead
of being written into the ad.

## How it works (Meta AI tooling)

1. **SAM 3.1** detects the product in the photo (box crop path — the proven
   route; concepts are tried in order until one returns a box).
2. **Muse Image 1.0** rebuilds the crop as a clean studio image,
   preserving the real label.
3. **Muse Spark 1.3** writes the listing copy from two sources only:
   text readable in the photo, and seller-provided facts.
4. **Evidence-first guardrail** (fail-closed): copy is parsed sentence by
   sentence. Any price, size, nutrition, certification, compatibility, or
   availability claim whose value is not in the photo or the seller facts
   is stripped into "needs confirmation". A claim that matches a seller
   value is kept as consistent — explicitly not as independently verified.
   Health-benefit wording is never exempt. If the model returns empty or
   malformed output, the user gets a minimal description plus a warning,
   never the raw untrusted output.

## Demo

- Video (record from `demo-script.md` — upload flow on local server):
  [PASTE VIDEO LINK AFTER RECORDING]
- Live browsable demo (static gallery + web-app UI):
  https://snapsell-demo.pages.dev/
- Full upload flow, runnable locally from the repo:
  checkout branch `backend-reliability`, run `python3 demo/server.py`,
  open the page, upload a photo. No API key is stored in the repo.
- Verified live run (2026-10-29, PR #5 code): Lactasoy carton photo →
  SAM concept "product" → 1600×1600 studio image → real 284-character
  listing ("แลคตาซอย Lactasoy สูตรต้นตำรับ Original 500 มล." + carton
  description) with 4 honest needs-confirmation items. Full logs:
  https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/backend-reliability-fix-2026-10-29.md

## Technical execution

- Stack: Python stdlib server (`demo/server.py`), Meta Model API
  (SAM 3.1, Muse Spark 1.3, Muse Image 1.0), vanilla JS frontend.
- Tests on the submitted code: guardrail suite 30/30, audit cases 12/12,
  language-switch check 40 elements / 0 mismatches, live pipeline verified
  end to end (not mocked). Evidence:
  https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/final-readiness-audit-2026-10-29.md
- Repository: https://github.com/Techfrontiers/snapsell-ai
  - Main: `2ec9d4ff` (guardrail + gallery attribution merged)
  - Draft PR #4 (web-app UI, GPT review: PASS WITH SCOPE LIMITS):
    https://github.com/Techfrontiers/snapsell-ai/pull/4
  - Draft PR #5 (backend reliability, GPT review: PASS for F-2/F-1 scope):
    https://github.com/Techfrontiers/snapsell-ai/pull/5
  - Both PRs remain Draft: GPT reviews did not authorize merge/deploy.
    They are linked here as the reviewed code, not as merged main.

## Impact

Built for sellers anywhere, starting from a firsthand Thai seller problem:
one photo should be enough to list honestly. The target user is any small
seller on Shopee, Lazada, TikTok Shop, Etsy, eBay, or Shopify who has a
phone but no studio, no copywriter, and no tolerance for listings that
promise what they cannot prove. No real users or sales metrics yet —
that is stated plainly, not padded.

## Theme / track

- Theme: (1) Build for Your World
- Track: Indie
- Team: solo unless confirmed otherwise before submitting (update this
  line at submit time if the team changes)
