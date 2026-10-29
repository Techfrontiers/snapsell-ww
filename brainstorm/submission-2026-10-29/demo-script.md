# SnapSell AI — Demo Video Script (60–90 seconds)

Recording status: NOT RECORDED YET. This file is the script + shot list only.
Do not claim the video exists until it is recorded and its link is pasted
into the submission form.

## Recording setup (proven path — use exactly this)

- Machine: a human machine (not this VM's headless screenshots).
- Code: checkout branch `backend-reliability` (PR #5, final SHA
  `640b3c1ac83e79d7dc514432583745e35d10136e`) and run `python3 demo/server.py`.
  This is the code with the verified live run. Do NOT record against `main`:
  main's `server.py` still has the F-2 token bug and returns fallback copy.
- Photo: the Lactasoy photo already in the repo (`demo/assets/before3.jpg`
  and the original in `snapsell-test-photos/`). No new photo shoot needed.
- Seller facts to type on camera: `แลคตาซอย นมถั่วเหลือง สูตรต้นตำรับ 500 มล.`
- Language: English narration (worldwide positioning). Thai subtitles optional.
- Rule: if a run returns the fallback sentence ("สินค้าตามในรูป."), STOP.
  Do not use that take. Re-run once; if it still fails, report it — never
  present a fallback take as a success.

## Script (target ~80 seconds)

| Time | Shot | Narration (say this) | Must be visible on screen |
|---|---|---|---|
| 0–10s | Phone photo of a product on a table, then the SnapSell page | "Small sellers take a photo. Then they stare at a blank listing form. Writing it takes longer than selling." | The Lactasoy carton photo, unedited |
| 10–20s | Upload the photo, type the seller facts, press Process | "SnapSell takes the photo, plus only what the seller actually knows." | File picked, facts field filled, Process clicked |
| 20–32s | Detection overlay / result area showing the found product | "SAM 3.1 finds the product in the photo — concept 'product', one box, no guessing outside the frame." | The detected box on the carton |
| 32–48s | Studio image appears next to the original | "Muse Image rebuilds it as a clean studio shot, same carton, same label." | Before/after side by side |
| 48–64s | Listing copy appears | "Muse Spark writes the listing — from the label and the seller's facts only. No invented price, no invented claims." | Real title + description (see below) |
| 64–78s | Needs-confirmation block | "And this is the point: anything unproven goes here, as 'needs confirmation' — never into the ad." | The needs list, clearly readable |
| 78–85s | Closing card: live URL + repo URL | "SnapSell. One photo in, an honest listing out." | https://snapsell-demo.pages.dev/ and https://github.com/Techfrontiers/snapsell-ai |

## Real outputs to show (from the verified live run, PR #5 code)

Do not retype these from memory — they are the recorded outputs of the
live run on 2026-10-29 (25.7s, HTTP 200, `spark_finish_reason: "stop"`):

- SAM: concept `product`, box `[128, 808, 739, 1682, 921, 2048]`
- Studio image: 1600×1600 PNG, real render (not a placeholder)
- Listing title: "แลคตาซอย Lactasoy สูตรต้นตำรับ Original 500 มล."
- Listing body (284 chars): carton description — blue-white pack, SINCE 1981,
  Delicious band, cap + straw, front text, 500 ml, PRODUCT OF THAILAND
- Needs confirmation (4 items, shown on camera):
  1. soy-milk type not clearly visible in the photo — confirm
  2. seller facts are not independently verified
  3. price / shipping / stock / expiry / condition — not provided
  4. nutrition / ingredients / certification / health claims — not verified
- Note for the narrator: the seller's "นมถั่วเหลือง" (soy milk) was
  deliberately KEPT OUT of the listing copy and put in needs instead,
  because it is not clearly visible in the photo. That is the trust feature.

## Honest framing for the video description

- The upload flow in this video runs on a local server (`demo/server.py`),
  because the public Pages link is a static demo (gallery + web-app UI).
  Say so in the video description; do not imply the public link uploads.
- The public link judges can open any time: https://snapsell-demo.pages.dev/
- Full evidence (audit + backend fix + logs): see the submission checklist.
