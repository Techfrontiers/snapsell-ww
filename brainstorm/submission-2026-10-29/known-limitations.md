# SnapSell AI — Known Limitations (honest disclosure)

Read before submitting. Nothing here blocks submission, but everything here
must stay true in the form, the video, and any judge-facing text. If a
limitation is fixed later, update this file — do not silently drop it.

## Demo / deployment

- The public link https://snapsell-demo.pages.dev/ is a STATIC demo
  (gallery + round-1 CDN web-app UI, 42,425 bytes, verified 2026-10-29).
  It does NOT support live upload. The upload flow requires `demo/server.py`
  running locally. The demo video is therefore the primary upload-flow
  evidence; the public link is the browsable gallery/UI evidence.
- PR #4 (web-app UI) and PR #5 (backend reliability) are DRAFT and
  UNMERGED. GPT reviewed both (UI: PASS WITH SCOPE LIMITS; backend: PASS
  for F-2/F-1 scope) but neither review authorized merge or deploy.
  Submitted code state = main `2ec9d4ff` + the two linked draft PRs.
- The recorded demo flow uses PR #5 branch code locally. It is not a
  deployed production service.

## Guardrail (evidence-first, but regex-based)

- Claim stripping is keyword/pattern-based. Paraphrases, misspellings,
  Thai variants, and implied claims ("feel fresh all day") can pass.
- Value matching covers NUMERIC prices and MEASURED sizes only.
- A seller value that matches is kept as CONSISTENT with seller input,
  not as independently verified truth. The UI says so explicitly.
- One early live test invented a store availability claim before the
  guardrail hardening; current availability wording is never exempt.

## Backend reliability (PR #5 scope)

- `max_tokens` 8192 is proven for the Lactasoy case only, not for all
  inputs. If a future run returns finish reason `length`, the budget
  must rise again — the response now exposes `spark_finish_reason` so
  this is visible instead of silent.
- The retry covers empty content on HTTP 200 only — not non-200 errors.
- No fetch timeout / AbortController in the UI yet (finding F-3, open):
  a stalled server hangs the UI silently instead of showing an error.
- SAM mask decoding to pixels is UNTESTED; the proven path is box crop.
- Live proof for the fixed backend is ONE photo + ONE facts set
  (the audit's comparison case). Broader photo coverage from 2026-10-27
  is historical and was not re-run on the new code.

## Maturity

- No real users, no sales metrics, no production deployment yet.
- Self-estimated rubric ~70/100 (audit) is the author's assessment,
  not a judge score, and must never be presented as one.
- F-3 (fetch timeout) is the only open audit finding; it does not block
  submission but must not be described as fixed.
