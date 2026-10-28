# Implementation plan — Idea 1 + Idea 2 (PLAN ONLY, no code changed)

For GPT review before any implementation starts.
No code was edited and nothing was committed to `snapsell-ai`.
This plan file itself is the only new file, in `snapsell-ww`.

## Repos compared

- `Techfrontiers/snapsell-ai` — the product repo (read live, Oct 28).
- `Techfrontiers/snapsell-ww` — this brainstorm repo (README + ideas +
  Meena evaluation 2026-10-28).

## Critical finding: there are TWO code paths, and only one is live

### Path A — `snapsell/` package: STUB ONLY, do not implement here

- `snapsell/snapsell/copywrite.py` — Thai template stub (`_stub_copy`,
  `title_th` / `description_th`, `MARKETPLACES = shopee, lazada,
  tiktok_shop`). Its live branch raises `NotImplementedError`.
- `snapsell/snapsell/segment.py` — SAM 3.1 stub (placeholder mask
  record + difficulty flags for the 5 test photos). Live branch raises
  `NotImplementedError`.
- `snapsell/snapsell/render.py` — Muse Image stub (copies the input
  photo as `studio_mock.jpg`, labelled MOCK). Live branch raises
  `NotImplementedError`.
- `snapsell/snapsell/pipeline.py` — `run_photo()` / `run_all()` wire
  the three stubs together into `listing.json` (stub shape only).
- `snapsell/snapsell/config.py` — mode gate (`SNAPSELL_MODE` +
  `META_MODEL_API_KEY` / `META_MODEL_API_BASE` env vars).

Implementing Idea 1 or 2 in Path A would change code that never runs
in the demo. Leave Path A alone for this hackathon.

### Path B — `demo/` folder: THE LIVE PATH, implement here

- `demo/server.py` — the live demo server (verified: the deployed
  copy differs from the repo copy by one blank line only).
  - `sam_box(data_url)` — SAM 3.1, POST `/responses`, concepts tried
    in order `["product", "bottle", "package", "box"]`, box parsed with
    `BOX_RE` from the `<|box;...|>` token.
  - `run_pipeline(img_bytes, lang="th")` — SAM box → PIL padded crop
    (pad 20) → Muse Image edits (`muse-image-1.0`, `EDIT_PROMPT`,
    1024x1024) → Muse Spark 1.3 (`/chat/completions`,
    `max_tokens` 2048) → `{ok, concept, box, studio_b64, copy}`.
  - `COPY_PROMPT` — already a dict with `th` and `en` entries. Both
    already say "do not invent a price or spec not visible in the
    photo" — but as free text only, with no enforcement and no
    structured output.
  - `Handler.do_POST` — POST `/api/process`, form fields `photo` +
    `lang` (default `th`), rate limit 20 uploads/hour/IP.
- `demo/index.html` — the demo UI. Already has a visible EN/TH switch
  (`.lang` buttons ไทย/EN, `setLang()`, `localStorage`, and
  `fd.append('lang', LANG)` on upload).
- Local test harness (not in the repo):
  `snapsell-live-test/batch_live.py` — the 5-photo batch runner
  (SAM + Spark + Image, Thai-only `COPY_PROMPT`). Use it for
  regression runs; do not treat it as the product.

## Idea 1 — Evidence-first guardrail: real edit points (all in Path B)

1. `demo/server.py` → `COPY_PROMPT` (`th` and `en`):
   rewrite from a one-sentence "do not invent" into an evidence-first
   instruction — copy only from visible packaging/product facts and
   seller-supplied facts; anything else goes in a delimited
   "needs confirmation" section, never in the title/description.
2. `demo/server.py` → `run_pipeline(img_bytes, lang)`:
   add an optional `seller_facts` input, pass it into the prompt,
   and parse the "needs confirmation" section out of the Spark reply.
   Add a deterministic post-check: if the copy contains a price-like
   token (currency symbol / บาท / $) and the seller supplied no price,
   strip it into "needs confirmation" instead of shipping it.
3. `demo/server.py` → `Handler.do_POST`:
   accept a `facts` form field; return the existing `copy` field
   unchanged for compatibility, plus new `needs_confirmation` (and
   `visible_facts` if the prompt returns them) fields.
4. `demo/index.html`:
   add a "needs confirmation" block on the result card. No change to
   the gallery or the upload flow itself.
5. Regression test (must be recreated — it is NOT in the saved batch
   JSONs): the Oct 27 live-upload case where the model guessed
   "sold at 7-Eleven". Use a 7-Select-style packaged product photo
   (or the original upload if still available) and assert the new
   copy makes NO availability claim without seller confirmation.

## Idea 2 — English/Thai language parameter: what is already done

Already implemented in Path B, so do NOT rebuild it:

- `COPY_PROMPT` dict (`th` / `en`) + `run_pipeline(lang)` +
  `do_POST` `lang` field + `index.html` EN/TH switch all exist.
- Remaining work is verification, not construction:
  (a) run the same 5 photos in EN and TH and compare facts for drift;
  (b) confirm the switch works end-to-end on the local server
  (the public upload pipe is currently closed, so test locally);
  (c) frame language as a parameter in the pitch — adding a language
  is one `COPY_PROMPT` entry + one button — but do NOT add or claim
  untested languages before the deadline.
- Path A (`copywrite.py` `title_th` / `description_th`) stays
  Thai-only and stays untouched: it is not the live path.

## Meta AI tooling check — PASS, no new tooling needed

- All changes reuse existing calls through the existing Meta Model API
  helper: `sam-3.1` POST `/responses`, `muse-image-1.0`
  POST `/images/edits`, `muse-spark-1.3` POST `/chat/completions`.
- No new model, no new endpoint, no new credential.
- SAM and Image steps are untouched (`sam_box`, `CONCEPTS`, `BOX_RE`,
  `EDIT_PROMPT`, crop pad 20), so the 5-photo proven path is
  preserved. Only the Spark prompt and response handling change, so
  regression scope is copy outputs only: re-run the 5 photos and
  confirm box/studio outputs are unchanged while copy outputs gain
  the guardrail.

## Do NOT change

- `sam_box`, `CONCEPTS`, `BOX_RE`, `EDIT_PROMPT`, the crop step,
  the 20/hour rate limit.
- Anything in `snapsell/` (Path A stub package).
- `snapsell-ai` repo content in this planning step (no commits there).

## Risks

- Do NOT assume Spark supports a structured JSON output mode: use a
  delimited-text "needs confirmation" section with a parser fallback
  (if the section is missing, treat the whole copy as unverified
  and surface that, rather than crashing or silently shipping it).
- Guardrail too strict → thin copy. Mitigation: the seller-facts
  input (Idea 1, edit point 2).
- Language drift: EN and TH copies of the same product stating
  different facts. Mitigation: Idea 1's shared evidence instruction
  + the EN/TH comparison run in Round 3.
- Price-pattern post-check false positives (e.g. a model number that
  looks like a price). Mitigation: only strip when a currency marker
  is present, and always show what was stripped in
  "needs confirmation" — never silently delete.
- Live upload pipe is closed: all testing in Rounds 1–3 runs locally
  (batch harness + local server), not through the public tunnel.

## Build → Test → Fix rounds (Idea 1 + Idea 2 only)

- **Round 1 — Idea 1, build:** rewrite `COPY_PROMPT` (th/en) +
  `seller_facts` input + needs-confirmation parsing + post-check +
  server response fields + UI block. No SAM/Image changes.
- **Round 2 — Idea 1, test + fix:** re-run the 5 photos in TH;
  run the recreated 7-Eleven regression case; check that
  "needs confirmation" appears when facts are missing and that no
  invented price/spec ships. Fix prompt/parser, not the pipeline.
- **Round 3 — Idea 2, test + fix:** run the same 5 photos in EN;
  compare EN vs TH facts product by product; fix drift via the
  shared evidence instruction; verify the UI switch end-to-end on
  the local server.
- **Round 4 (only if Rounds 1–3 are green) — Idea 4 prep:**
  package Rounds 1–3 outputs into the demo path (before/after +
  cost note). Idea 3 (marketplace export) stays cut to minimal
  or deferred, per the Oct 28 evaluation.

Total for Ideas 1 + 2: 3 rounds, plus Round 4 only on green.
If any round fails on parsing reliability, fall back to the
delimited-text version — do not add a new model to fix it.
