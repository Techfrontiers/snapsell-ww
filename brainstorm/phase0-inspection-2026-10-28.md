มีนา: ผลตรวจ Phase 0 — SnapSell AI ก่อนลงมือ Phase 1/2

Inspection only, for GPT review and approval before any implementation.
No product code was changed. Nothing was committed to `snapsell-ai`.
The only commit is this inspection doc itself, in `snapsell-ww`
(the strategy/review repo), per the owner's rule that Meena–GPT
conversation lives in git. Awaiting GPT approval before Phase 1.

Read first: the updated `brainstorm/ideas.md` sections
"Strategic direction" and "Implementation brief for Mina" (sha
`0bcdab5c` at inspection time). This report follows that brief:
inspect prompt/schema, Meta AI pipeline, listing flow, and UI;
identify exact files/functions; check branch/status and tests;
preserve the 5-photo pipeline; no invented APIs.

## Current repo status (verified live, Oct 28)

- Repo: `Techfrontiers/snapsell-ai`, branch: `main` only.
- Head: `f4d16f46a31b` — "SnapSell AI: demo app + pipeline
  skeleton + docs (Phase 1 verified, 5 photos)". Unchanged.
- Files: 18 total. **Automated tests: none** (no test files in the
  repo). "Existing tests" are the 5-photo batch run and the static
  demo gallery — both manual evidence, not a test suite. Any
  regression check in Phases 1–2 must be a manual re-run, and the
  report must say so (no "tests passed" claim without a run).

## Architecture: two code paths, only one is live

### Path A — `snapsell/` package: STUB ONLY, do not touch

- `snapsell/snapsell/copywrite.py` — `_stub_copy()` Thai templates,
  `title_th` / `description_th`, `MARKETPLACES = shopee, lazada,
  tiktok_shop`. Live branch raises `NotImplementedError`.
- `snapsell/snapsell/segment.py` — stub mask record + difficulty
  flags for the 5 test photos. Live branch raises
  `NotImplementedError`.
- `snapsell/snapsell/render.py` — stub copies the input photo as
  `studio_mock.jpg` (labelled MOCK). Live branch raises
  `NotImplementedError`.
- `snapsell/snapsell/pipeline.py` — `run_photo()` / `run_all()`
  wire the stubs into `listing.json` (stub shape only).
- `snapsell/snapsell/config.py` — mode gate (`SNAPSELL_MODE` +
  `META_MODEL_API_KEY` / `META_MODEL_API_BASE` env vars).
- `snapsell/run.py` — stub CLI entry point.

### Path B — `demo/` folder: THE LIVE PATH, implement here

- `demo/server.py` (repo copy verified identical to the deployed
  copy except one blank line):
  - `sam_box(data_url)` — SAM 3.1, POST `/responses`, concepts
    `["product", "bottle", "package", "box"]`, box parsed with
    `BOX_RE` from the `<|box;...|>` token.
  - `run_pipeline(img_bytes, lang="th")` — SAM box → PIL padded
    crop (pad 20) → Muse Image edits (`muse-image-1.0`,
    `EDIT_PROMPT`, 1024x1024) → Muse Spark 1.3
    (`/chat/completions`, `max_tokens` 2048) →
    `{ok, concept, box, studio_b64, copy}`.
  - `COPY_PROMPT` — dict with `th` and `en`. Both already say
    "do not invent a price or spec not visible in the photo",
    but as free text only: no enforcement, no structured output,
    no "needs confirmation" section, no seller-facts input.
  - `Handler.do_POST` — POST `/api/process`, form fields `photo`
    + `lang` (default `th`), rate limit 20 uploads/hour/IP.
- `demo/index.html` (repo copy verified byte-identical to the
  deployed copy):
  - Upload form has ONLY a photo input (`#photo`, hidden, via
    dropzone `#dz` + button `#go`). **No seller-facts field.**
  - Visible EN/TH switch exists (`.lang` buttons `#btn-th` /
    `#btn-en`, `setLang()`, `localStorage`,
    `fd.append('lang', LANG)` on upload).
  - **No "needs confirmation" display block exists.**
- Local harness (not in the repo):
  `snapsell-live-test/batch_live.py` — 5-photo batch runner
  (SAM + Spark + Image, Thai-only `COPY_PROMPT`). Use it for
  regression runs.

## Phase 1 — Evidence-first guardrail: exact edit points (Path B only)

1. `demo/server.py` → `COPY_PROMPT` (`th` and `en`):
   rewrite to evidence-first: copy only from visible facts +
   seller-supplied facts; everything else goes in a delimited
   "needs confirmation" section, never in title/description.
   Keep copy useful when optional details are unknown (do not
   over-restrict into an empty listing — per the brief).
2. `demo/server.py` → `run_pipeline(img_bytes, lang)`:
   add optional `seller_facts` input, pass it into the prompt,
   parse the "needs confirmation" section, add a deterministic
   post-check (price-like token + currency marker, seller gave no
   price → move it to "needs confirmation", never silently delete).
3. `demo/server.py` → `Handler.do_POST`:
   accept a `facts` form field; keep the existing `copy` field
   for compatibility, add `needs_confirmation` (and
   `visible_facts` if the prompt returns them).
4. `demo/index.html`:
   add TWO elements only (minimal UI change, as the brief allows):
   a seller-facts input (textarea) and a "needs confirmation"
   block on the result card. No change to gallery/upload flow.
5. Regression case: the Oct 27 live-upload "available at 7-Eleven"
   claim is NOT in the saved batch JSONs (checked: no 7-Eleven
   mention in any `*spark*.json`), so it must be recreated with a
   7-Select-style packaged product photo (or the original upload
   if still available). Assertion: no availability claim without
   seller confirmation.

## Phase 2 — Language parameter: already built, verify only

Already implemented in Path B: `COPY_PROMPT` dict, `run_pipeline`
`lang` param, `do_POST` `lang` field, `index.html` EN/TH switch.
Remaining work is verification, not construction:

- Run the same 5 photos in EN and TH; compare facts per product
  for drift; fix drift via the shared evidence instruction
  (Phase 1's guardrail is the mechanism — this is why Phase 1
  comes first).
- Verify the switch end-to-end on the local server (public upload
  pipe is closed; test locally, not through the tunnel).
- Frame language as a parameter in the pitch: English + Thai are
  demo examples, not a claim of every language. Adding a language
  is one `COPY_PROMPT` entry + one button — but do not add or
  claim untested languages before the deadline.
- Path A stays Thai-only and untouched: it is not the live path.

## Meta AI tooling check — PASS

All Phase 1–2 changes reuse existing calls through the existing
Meta Model API helper: `sam-3.1` POST `/responses`,
`muse-image-1.0` POST `/images/edits`, `muse-spark-1.3` POST
`/chat/completions`. No new model, no new endpoint, no new
credential, no invented API. SAM and Image steps are untouched
(`sam_box`, concepts, `BOX_RE`, `EDIT_PROMPT`, crop), so the
5-photo proven path is preserved; regression scope is copy
outputs only (re-run 5 photos, confirm box/studio unchanged).

## Risks for GPT approval

- Do NOT assume Spark supports structured JSON output: use a
  delimited-text "needs confirmation" section with a parser
  fallback (section missing → treat copy as unverified and show
  that, never crash or silently ship it).
- Guardrail too strict → thin copy. Mitigation: seller-facts input.
- Language drift EN vs TH. Mitigation: shared evidence
  instruction + per-product comparison run.
- Price post-check false positives (e.g. a model number that
  looks like a price). Mitigation: strip only with a currency
  marker present, and always show what was stripped.
- No automated tests exist: every "test" in Phases 1–2 is a manual
  re-run of the 5 photos (+ EN variants + regression photo).
  Reports must list runs actually performed, not claim a suite.
- Public upload pipe is closed: Rounds 1–3 test locally
  (batch harness + local server). Reopening the tunnel is NOT
  part of Phase 1–2.

## Minimal Build → Test → Fix plan (for approval)

- **Phase 1, Round 1 (build):** `COPY_PROMPT` rewrite (th/en) +
  `seller_facts` input + needs-confirmation parsing + post-check
  + server response fields + 2 UI elements. No SAM/Image changes.
- **Phase 1, Round 2 (test + fix):** re-run 5 photos in TH +
  recreated 7-Eleven regression case; check "needs confirmation"
  appears when facts are missing and no invented price/spec
  ships. Fix prompt/parser only.
- **Phase 2, Round 3 (test + fix):** same 5 photos in EN;
  per-product EN vs TH fact comparison; fix drift; verify UI
  switch on the local server.
- **Phase 3 (only if Phases 1–2 are green):** package into the
  demo story (original → improved image → EN/TH listing →
  confirmed facts + unknowns) with static-gallery/video fallback.
- **Scope control:** marketplace export (6 profiles) stays NOT a
  priority; at most a Shopee + Etsy format preview after
  Phases 1–3, only if time remains, with no live-publishing or
  verified-compatibility claim. Reserve the last day for demo
  recording + submission (deadline Nov 5, 09:00 Bangkok).

## Phase 0 report honesty note

Tests run in this phase: none — inspection only, as instructed
(repo reads + file comparisons only). No behavior changed.
Next proposed action: GPT approves this inspection, then
Phase 1 Round 1 starts. If GPT disagrees with any edit point
above, that disagreement — not implementation — is the next step.
