# SnapSell — Final Hackathon Readiness Audit

**สถานะ: READY FOR GPT FINAL REVIEW** — สถานะนี้หมายถึงพร้อมให้ GPT
ตรวจรอบสุดท้ายเท่านั้น **ไม่ใช่การอนุมัติ Merge และไม่ใช่การอนุมัติ Deploy**

## 0. ข้อมูลการตรวจ (Audit identity)

- Repo ที่ตรวจ: `Techfrontiers/snapsell-ai`, PR: https://github.com/Techfrontiers/snapsell-ai/pull/4
- Branch: `webapp-tailwind`
- **Commit SHA เต็มที่ตรวจ: `cbc4c4afa3a43851a93ac1a12177f81d95deeb3a`**
- สถานะ PR ณ เวลาตรวจ: **Draft, เปิดอยู่ (open), ยังไม่ merge, base = main, ahead 9 / behind 0, mergeable = true (เป็นแค่ flag ของ GitHub ไม่ใช่การอนุมัติ)**
- ไฟล์ที่เปลี่ยนเทียบ main (5 ไฟล์เท่านั้น): `demo/index.html`, `demo/tailwind.css`,
  `demo/tailwind.config.js`, `demo/tailwind-input.css`, `demo/sweetalert2.all.min.js`
- วันที่และเวลาทดสอบ: **2026-10-29 ~08:47–08:55 Bangkok**
- ผู้ตรวจ: มีนา (Muse)
- หลักฐานกลาง: https://github.com/Techfrontiers/snapsell-ww/tree/main/brainstorm/evidence/pr4-final

### ป้ายวิธีทดสอบ (อ่านก่อนเชื่อผล)

- **[LIVE]** = รันจริง (เซิร์ฟเวอร์จริง / API จริง) ในรอบตรวจนี้
- **[HARNESS]** = เทสต์ด้วย DOM/fetch stub (ไม่ได้รันเบราว์เซอร์จริง)
- **[UNIT]** = unit test บนโค้ด `server.py` ที่ดึงมาสดจาก branch
- **[STATIC]** = ตรวจโค้ด/diff ด้วยโปรแกรม (ไม่ได้รัน)
- **[VISUAL]** = ดูจาก screenshot ที่ถ่ายในรอบตรวจนี้
- **[HISTORICAL]** = ผลเก่าที่มีวันที่กำกับ — **ไม่ใช่หลักฐานของรอบตรวจนี้** อ้างอิงเป็นบริบทเท่านั้น
- **[NOT TESTED]** = ไม่ได้ทดสอบในรอบนี้ พร้อมเหตุผล

### หลักการซื่อสัตย์ของรายงานนี้

- ผลทดสอบทุกชิ้นในรายงานนี้ **รันซ้ำบนไฟล์ที่ดึงสดจาก branch ในรอบตรวจนี้** — ไม่มีผลเก่าที่ถูกนำมาอ้างว่าเป็นผลของ commit ใหม่
- ไม่มีคำว่า PASS ที่ไม่มีหลักฐาน — ทุก PASS มี log หรือไฟล์อ้างอิง
- ผล live กับผล mock/harness แยกกันชัดเจนทุกตาราง
- ไม่มี secret, API key, token หรือข้อมูลส่วนบุคคลในรายงานและหลักฐาน (สแกนแล้วสะอาด, ดูหัวข้อ 1)
- การเรียก API จริงใช้ connector flow (surrogate auth) — ไม่มีการพิมพ์ค่าของ secret ออกมา
- **ไม่มีการแก้โค้ดใดๆ ในรอบตรวจนี้** — ไฟล์ audit ทั้งหมดอยู่ใน `snapsell-ww` ไม่ได้แตะ `snapsell-ai`
  ดังนั้น SHA ที่ล็อกไว้ข้างบนจึงยังเป็น SHA เดียวกับที่ตรวจ

### คำสั่งที่ใช้ทดสอบ (ทำซ้ำได้)

```
# ดึงไฟล์สดจาก branch
gh_api.py call GET /repos/Techfrontiers/snapsell-ai/contents/demo/<file>?ref=webapp-tailwind
gh_api.py call GET /repos/Techfrontiers/snapsell-ai/compare/main...webapp-tailwind
# guardrail (บนไฟล์สด: server.py + test_guardrail.py + index.html)
python3 test_guardrail.py
# harness (node, DOM/fetch stub)
node audit-langtest.js / audit-preview-test.js / audit-process-test.js
# audit cases (python, import server.py สด)
python3 audit_tests.py
# เซิร์ฟเวอร์จริง (ไฟล์สดทั้งโครงสร้าง demo)
python3 server.py 8902  (bind 127.0.0.1)
curl http://127.0.0.1:8902/  (+ /tailwind.css, /sweetalert2.all.min.js, /assets/*.jpg)
curl -X POST http://127.0.0.1:8902/api/process -F "photo=@assets/before3.jpg" -F "lang=th" -F "facts=..."
# วินิจฉัย Spark (ตรง ไม่ผ่าน server.py)
meta_api.py chat --model muse-spark-1.3 --prompt "Say the word TEST and nothing else." --max-tokens 256|4096
# screenshot (ไฟล์สด, byte-identical กับ branch — ตรวจด้วย cmp)
chrome-headless-shell --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=W,H --virtual-time-budget=15000 --screenshot=out.png file://...
```

## 1. ตรวจ PR #4 และล็อกเวอร์ชัน (ตามข้อ 2 ของคำสั่ง)

| รายการตรวจ | ผล | หลักฐาน |
|---|---|---|
| Tailwind Play CDN ถูกถอดจริง | **PASS** [STATIC] — ไม่มี `cdn.tailwindcss.com`, ไม่มี `jsdelivr`, ไม่มี inline `tailwind.config` ใน `index.html` | [section2-checks.txt](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/section2-checks.txt) |
| ใช้ compiled CSS | **PASS** [STATIC] — `href="tailwind.css"`, ไฟล์ 14,270 bytes (minified, สร้างด้วย tailwindcss 3.4.17), utility 45 ตัวที่เช็คครบรวม arbitrary values (`lg:grid-cols-[380px_1fr]`, `group-hover:scale-[1.03]`, `focus:ring-accent/20`) | section2-checks.txt |
| SweetAlert2 vendored 11.26.25 | **PASS** [STATIC] — header `sweetalert2 v11.26.25`, MIT, 79,150 bytes, `src="sweetalert2.all.min.js"` (local) | section2-checks.txt |
| ไม่มี external dependency ที่ UI ต้องใช้เพื่อ render โดยไม่ตั้งใจ | **PASS** [STATIC] — `src`/`href` ทั้งหมดเป็น relative + anchor เท่านั้น (external = NONE); `tailwind.css` ไม่มี `url(`; สตริง `https://` เดียวในไฟล์ Swal คือ URL เอกสารในข้อความ warning (`showLoaderOnConfirm ... see usage example`) — **ไม่เคยถูก fetch** | section2-checks.txt |
| รูป/CSS/JS ที่อ้างอิงมีอยู่จริงและโหลดได้จากโครงสร้างเดโม | **PASS** [LIVE] — ผ่าน `server.py` จริง: `/` 200 (41,906 bytes), `/tailwind.css` 200 (14,270), `/sweetalert2.all.min.js` 200 (79,150), `/assets/before3.jpg` 200 (211,811), `/assets/after3.jpg` 200 (267,458), ไฟล์ไม่มีอยู่จริง → 404 ถูกต้อง | [server-static-2026-10-29.txt](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/server-static-2026-10-29.txt) |
| API endpoint / form contract / Guardrail / gallery attribution / TH/EN / preview fix ครบ | **PASS** [UNIT+HARNESS+STATIC] — guardrail 25/25 บนไฟล์สด; lang-switch 40/0; preview PASS; `API_BASE + '/api/process'`, fields `photo/lang/facts`, `galleryNote` + d3 attribution, `prevPreviewURL` ตรวจพบในไฟล์สด | [guardrail log](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/guardrail-2026-10-29.txt), [langswitch](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/langswitch-2026-10-29.txt), [preview](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/preview-2026-10-29.txt) |
| ไม่มี secret/API key/token/PII หลุดเข้า repo หรือ logs | **PASS** [STATIC] — สแกน pattern (sk-, ghp_, github_pat_, Bearer, api_key, email, เบอร์โทร, เลข 13 หลัก) บนไฟล์ PR 5 ไฟล์ + `server.py` + `test_guardrail.py` = **CLEAN ทั้งหมด**; log live ถูก redact (studio_b64 แทนด้วยความยาว) | section2-checks.txt |
| ไม่มีการแก้ backend หรือขอบเขตนอก PR โดยไม่จำเป็น | **PASS** [STATIC] — compare = 5 ไฟล์ demo เท่านั้น; `server.py` blob `024c8753f981` และ `test_guardrail.py` blob `80b491ec31ad` **ตรงกับ main** | section2-checks.txt |

## 2. คุณภาพและความปลอดภัยของข้อมูลสินค้า (ตามข้อ 3 ของคำสั่ง)

สคริปต์เทสต์รอบตรวจนี้ (audit-only, ไม่ได้อยู่ใน `snapsell-ai`):
[audit_tests.py](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/audit_tests.py) —
ผลรัน: [audit-cases log](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/audit-cases-2026-10-29.txt)
(**11 PASS, 1 FAIL** — FAIL เดียวคือ F-1 ด้านล่าง ไม่ใช่ความผิดของ harness)

| กรณีตามคำสั่ง | Input fixture (ปลอดภัย) | Expected | Actual (รอบตรวจนี้) | ผล / วิธี |
|---|---|---|---|---|
| 1. ภาพชัด ฉลากอ่านได้ | รูป Lactasoy `before3.jpg` (รูปเทสต์เดิมของทีม) | SAM เจอสินค้า, ได้รูปสตูดิโอ, ข้อความอ่านฉลากได้ | SAM เจอ box (concept `product`, box [128,808,739,1682,921,2048]) + รูปสตูดิโอ 1600×1600 จริง | **PARTIAL** [LIVE] — SAM/Image ผ่าน; การอ่านฉลากโดย Spark **[NOT TESTED]** live (Spark คืนค่าว่าง 2/2 ครั้ง ดู F-2) |
| 2. ฉลากไม่ชัด / ข้อมูลไม่ครบ | ข้อความคลุมเครือไม่มี marker / ข้อความว่าง / marker แต่ไม่มีรายละเอียด | fail-closed: ได้คำอธิบายปลอดภัยขั้นต่ำ + needs | ได้ `สินค้าตามในรูป.` + FALLBACK_NEEDS ครบทั้ง 3 แบบ | **PASS** [UNIT] |
| 3. ภาพย้อนแสง / มีมือบัง / พื้นหลังรก | — (ไม่มีรูปแบบนี้รันในรอบนี้) | SAM fallback concept ช่วย + guardrail ไม่แต่งข้อมูล | โค้ดมี `CONCEPTS = ["product","bottle","package","box"]` ลองตามลำดับ [STATIC] | **[NOT TESTED]** live ในรอบนี้ (ไม่มีรูปเงื่อนไขนี้ + ไม่มีเครดิตเผื่อรันหลายรูป); [HISTORICAL] 27 ต.ค.: รูป 5 ใบหลายสภาพผ่าน pipeline (อ้างเป็นบริบทเท่านั้น) |
| 4. โมเดลคืนข้อความว่าง / response ผิดรูปแบบ | `""`, ข้อความขยะไม่มีโครงสร้าง, ข้อความมี marker ปกติ | ว่าง/ผิดรูปแบบ → fail-closed; ปกติ → แยก description/needs ได้ | ว่าง → `empty model output` + fallback ครบ; ขยะ → raw เก็บเป็น diagnostic เท่านั้น ไม่กลายเป็นข้อความขาย; ปกติ → แยกได้ถูกต้อง | **PASS** [UNIT] และ **PASS** [LIVE] — Spark คืนค่าว่างจริง 2/2 ครั้งในรอบนี้ แล้ว guardrail fail-closed ถูกต้องทั้ง 2 ครั้ง |
| 5. โมเดลสร้างราคา / คุณสมบัติ / สถานที่ / ข้ออ้างไม่มีหลักฐาน | "ซื้อได้ที่ 7-Eleven ราคา 999 บาท" (ไม่มี facts) / "มีวิตามินซีสูง..." / "พร้อมส่งวันนี้ มีของในสต็อก" | ถูกตัดออกเป็น needs ไม่ขึ้นเป็นข้อความขาย | ถูกตัดทั้งหมด (price-unverified / nutrition / current-availability) เหลือคำอธิบายปลอดภัยขั้นต่ำ; ส่วนค่าที่ตรงกับ seller facts ("ราคา 35 บาท") ถูกเก็บไว้ตามออกแบบ | **PASS** [UNIT] (+ suite เดิม: nutrition/cert/compat/retailer/health-benefit) |
| 6. seller facts ขัดแย้งกับภาพ | copy "ราคา 50 บาท" + facts "ราคา 100 บาท"; copy "ขนาด 500 มล." + facts "ขนาด 600 มล." | ขัดแย้ง → ตัดทิ้ง (ทิศปลอดภัย) ไม่เผยแพร่ | ราคาขัดแย้ง → ตัดเป็น price-mismatch ✓; **ขนาด "มล." ขัดแย้ง → ไม่ถูกตัด (ยังเผยแพร่)** ✗ | **PARTIAL — FINDING F-1** [UNIT] (ดูกล่อง F-1) |
| 7. API error / timeout / response ไม่ใช่ JSON | fetch reject / `json()` throw / POST ไม่มีรูป / ผิด path | เข้า error path: status + error modal, ไม่ค้าง ไม่ crash | fetch reject → serverFail + error modal ✓; non-JSON → serverFail + error modal ✓; POST ไม่มีรูป (เซิร์ฟเวอร์จริง) → `{"ok": false, "error": "ไม่พบไฟล์รูป"}` ✓; ผิด path → 404 ✓ | **PASS** [HARNESS+LIVE] ยกเว้น timeout = **GAP F-3** (ไม่มี AbortController) |

### คำเตือนที่ต้องเขียนไว้ตรงนี้ (ห้ามอ้างเกินจริง)

การผ่าน unit tests **ไม่ได้แปลว่า** guardrail ป้องกันการแต่งข้อมูลได้ทั้งหมด —
ข้อจำกัดนี้เขียนไว้ในโค้ดเอง (`server.py` ส่วน LIMITATIONS) และยืนยันจากการตรวจ:
regex จับเฉพาะ keyword/pattern ที่ระบุไว้ — paraphrase, คำสะกดผิด,
ถ้อยคำไทยแปรผัน, ข้ออ้างเป็นนัย ("feel fresh all day"), ข้ออ้างที่แยก
ข้ามประโยค **ไม่ถูกจับ**; nutrition/certification/compatibility ยังเป็น
keyword-based (ไม่ได้ value-verified แบบราคา/ขนาด); ค่าที่ตรงกับ seller
= ความสอดคล้องกับ input ของผู้ขายเท่านั้น **ไม่ใช่ความจริงที่ผ่านการตรวจสอบอิสระ**

## 3. เส้นทางเดโมต้นจนจบ (ตามข้อ 4 ของคำสั่ง)

รันผ่าน `server.py` จริง (ไฟล์สด, bind 127.0.0.1:8902) — **ผล live กับ mock แยกกันชัดเจน ห้ามเรียก mock test ว่า live E2E**

| ขั้น | วิธี | ผล (รอบตรวจนี้) |
|---|---|---|
| 1. เปิดหน้าเดโมผ่าน `server.py` | [LIVE] | GET `/` → 200, 41,906 bytes (= ไฟล์ branch) |
| 2. เลือกรูปสินค้า | [HARNESS] | input.files + change handler ทำงาน (preview test) — ไม่ได้ขับ file picker ในเบราว์เซอร์จริง |
| 3. Preview ภาพ | [HARNESS] | สร้าง URL → แสดง → เลือกใหม่ revoke เฉพาะ URL เก่า (URL ที่กำลังใช้ไม่เคยถูก revoke) PASS |
| 4. กรอก seller facts ถ้ามี | [HARNESS]+[LIVE] | harness: FormData มี `photo/lang/facts` ครบ; live รันที่ 2 ใส่ facts "แลคตาซอย นมถั่วเหลือง สูตรต้นตำรับ 500 มล." → `seller_facts_used: true` |
| 5. กดประมวลผล | [LIVE] | POST `/api/process` 2 ครั้ง → 200 ทั้ง 2 ครั้ง (~28 วินาที/ครั้ง) |
| 6. ตรวจ API request และ response | [LIVE] | request multipart ถูกต้อง; response มีครบทุกฟิลด์ (`ok/concept/box/studio_b64/copy/needs_confirmation/seller_facts_used/diagnostic_untrusted`) — log แบบ redact: [run 1](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/live-before3-redacted.json), [run 2 (facts)](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/live-before3-facts-redacted.json) |
| 7. ตรวจภาพที่สร้างและข้อความประกาศขาย | [LIVE] | รูปสตูดิโอจริง 1600×1600 RGB (2.8–2.9 MB): [live-studio-before3.png](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/live-studio-before3.png); **ข้อความประกาศขาย = fallback** ("สินค้าตามในรูป.") เพราะ Spark คืนค่าว่าง — ดู F-2 (นี่คือข้อเท็จจริง ไม่ใช่ผลที่แต่ง) |
| 8. ตรวจ needs-confirmation / unknown handling | [LIVE]+[HARNESS] | live: response มี FALLBACK_NEEDS ถูกต้อง; harness: needs list render ในการ์ดครบ |
| 9. ตรวจ error handling และ no-Swal fallback | [LIVE]+[HARNESS] | live: POST ไม่มีรูป → `{ok:false}`; harness: fetch reject / non-JSON → serverFail + error modal; ไม่มี Swal → การ์ด + status ยังทำงาน ไม่ crash |
| 10. เปลี่ยนภาษา TH/EN และตรวจ navigation | [HARNESS]+[STATIC]+[VISUAL] | lang-switch 40/0; anchor ทุกตัวชี้ไป id ที่มีอยู่จริง; EN shot แปลครบ — **click-scroll ในเบราว์เซอร์จริง [NOT TESTED]** (ไม่มี interactive run ในรอบนี้) |

หมายเหตุเรื่อง API key: การเรียก API จริงใช้ connector flow (surrogate auth)
ของ `custom.meta-model-api` — server.py import `call/call_multipart` จาก
helper นี้โดยตรง ไม่มีการใส่ key ลง repo/log/screenshot และไม่มีการพิมพ์
ค่าของ secret ออกมาในรอบตรวจนี้

## 4. Screenshot และผลตรวจ Visual (ตามข้อ 5 ของคำสั่ง)

ไฟล์ทั้งหมดอยู่ใน https://github.com/Techfrontiers/snapsell-ww/tree/main/brainstorm/evidence/pr4-final
(ถ่ายจากไฟล์ที่ดึงสดจาก branch ในรอบนี้ และตรวจด้วย `cmp` ว่า
byte-identical กับไฟล์ branch ก่อนถ่าย — **ไม่ใช่การเปลี่ยนชื่อภาพเก่า**;
ภาพรอบนี้บังเอิญตรงกับภาพรอบก่อนแบบ byte-identical เพราะไฟล์ต้นทางเหมือนกันทุก byte)

- [desktop-1440.png](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/desktop-1440.png) — viewport 1440×1000, TH
- [mobile-390.png](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/mobile-390.png) — viewport 390×844, TH
- [desktop-en-1440.png](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/desktop-en-1440.png) — viewport 1440×1000, EN (variant บังคับ default lang เฉพาะตอนถ่ายภาพ ไฟล์ที่ commit ไม่เปลี่ยน)
- [full-page-1440.png](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/full-page-1440.png) — viewport 1440×4600, TH (เต็มหน้า)
- [metadata.md](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/metadata.md) — commit SHA, viewport, tool, วันที่, วิธีสร้าง, sha256 ของภาพ

| รายการตรวจ | ผล |
|---|---|
| horizontal overflow | **PASS** [VISUAL] — ไม่มีที่ 1440 และ 390 |
| missing image / asset | **PASS** [VISUAL+STATIC] — รูปครบ 10/10 ใน full-page shot; ทุก ref มีไฟล์อยู่จริง |
| TH/EN translation | **PASS** [VISUAL+HARNESS] — EN shot แปลครบ (nav/hero/CTA/pipeline/upload); lang-switch 40/0 |
| anchor navigation | **PASS** [STATIC] — ทุก href ชี้ไป id ที่มีอยู่จริง; click-scroll ในเบราว์เซอร์จริง **[NOT TESTED]** |
| layout บนมือถือ | **PASS** [VISUAL] — 390 เรียงซ้อนเรียบร้อย (nav ซ่อนตามดีไซน์) |
| reduced-motion behavior | **STATIC เท่านั้น** — media query `prefers-reduced-motion` มีอยู่ในโค้ด; พฤติกรรมจริงเมื่อเปิด reduced-motion **[NOT TESTED]** (ไม่มี interactive run) |
| modal/toast และ no-Swal fallback | **PASS** [HARNESS] — ลำดับการเรียก Swal (loading → warning/toast/error) และ fallback เมื่อไม่มี Swal ถูกต้อง; **หน้าตา modal/toast จริง [NOT TESTED]** (ไม่มี modal เปิดอยู่ตอนถ่ายภาพ) |

## 5. สิ่งที่พบ (Findings) — ไฟล์/บรรทัด/หลักฐาน/วิธีแก้

### F-1 (ความรุนแรง: ปานกลาง) — หน่วย "มล." หลุดจากการตรวจขนาด

- **ไฟล์/บรรทัด:** `demo/server.py` บรรทัด 125 (`_SIZE_UNITS`) — รายการหน่วยไม่มี `มล.`
  (มี กิโลกรัม/kg, กรัม/g, มิลลิลิตร/ml, ลิตร, ซม./cm, มม./mm — แต่ไม่มี มล.)
- **หลักฐาน:** audit case `case6-conflict-size-stripped` FAIL —
  copy "ขนาด 500 มล." + facts "ขนาด 600 มล." → **ไม่ถูกตัด ยังเผยแพร่** (`removed=[]`);
  ขณะที่ราคาขัดแย้ง ("50 บาท" vs "100 บาท") ถูกตัดถูกต้องเป็น price-mismatch
- **ทำไม suite เดิมจับไม่ได้:** test `test_mismatched_price_and_size_stripped` ใช้ "500 g"
  (หน่วยละติน) จึงผ่าน — ช่องโหว่นี้เฉพาะหน่วยย่อไทย "มล." ซึ่งเป็นหน่วยที่
  ใช้กันแพร่หลายที่สุดในลิสติ้งไทย (การ์ด Lactasoy เองเขียน "500 มล.")
- **ผลกระทบ:** ข้อความขนาดที่เขียนเป็น "มล." จะไม่ถูก value-checked ทั้งกรณี
  ไม่มี facts (size-unverified ไม่ทำงาน) และกรณี facts ขัดแย้ง (size-mismatch ไม่ทำงาน)
- **วิธีแก้ที่เสนอ (ยังไม่แก้ในรอบนี้):** เพิ่ม `r"มล\.?"` เป็น volume factor 1.0 ใน
  `_SIZE_UNITS` + regression tests 3 เคส (mismatch/match/unverified ด้วย "มล.")
- **ทำไมยังไม่แก้:** เป็นโค้ด backend ของ main (Phase 1) ไม่ใช่ส่วนของ PR #4 —
  การแก้ตอนนี้จะเปลี่ยน SHA ที่ล็อกไว้และทำให้รายงานนี้หมดความหมาย
  แนะนำให้แก้ก่อนส่งประกวด (แก้เล็ก ได้ความน่าเชื่อถือของเรื่อง trust กลับมา)

### F-2 (ความรุนแรง: สูงต่อคุณภาพเดโมสด) — Spark คืนค่าว่าง 2/2 ครั้ง: `max_tokens` ไม่พอให้โมเดล always-thinking

- **ไฟล์/บรรทัด:** `demo/server.py` บรรทัด 335 — Spark call ใช้ `"max_tokens": 2048`
- **หลักฐาน live:** pipeline run 2 ครั้ง (รูปเดียวกัน, ครั้งหนึ่งไม่มี facts อีกครั้งมี facts) →
  `ok: true`, SAM box เดิมทั้ง 2 ครั้ง, รูปสตูดิโอจริง 1600×1600,
  แต่ `copy` = fallback "สินค้าตามในรูป." และ `diagnostic_untrusted = "empty model output"` ทั้ง 2 ครั้ง
- **การวินิจฉัยถึงราก (แยกจาก server.py):** เรียก Spark 1.3 ตรงด้วย prompt ง่ายๆ
  "Say the word TEST and nothing else." —
  `max_tokens 256` → `finish_reason "length"`, `content null`, reasoning 254/256 tokens;
  `max_tokens 4096` → `finish_reason "stop"`, `content "TEST"`, reasoning 450 tokens
  (log: [spark-diagnostic](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/pr4-final/logs/spark-diagnostic-2026-10-29.txt))
- **สรุปด้วยความมั่นใจสูง:** โมเดล always-thinking ใช้ reasoning หลายร้อย token แม้กับ
  prompt ง่ายๆ — `max_tokens 2048` บนงานที่ prompt ยาว (คำสั่งไทย + รูป) จึงหมดโควตาก่อน
  ได้เนื้อความ นี่ไม่ใช่ transient (เกิด 2/2 ครั้ง + อธิบายได้ด้วย token budget)
- **วิธีแก้ที่เสนอ (ยังไม่แก้ในรอบนี้):** เพิ่ม `max_tokens` อย่างมาก (เช่น 8192)
  ใน Spark call แล้วรัน live ตรวจว่าได้ข้อความจริง — เป็นการแก้ backend นอกขอบเขต
  PR #4 และจะเปลี่ยนผลการตรวจ จึงต้องทำเป็นงานแยกพร้อม re-verify ของตัวเอง
- **ผลกระทบถ้าไม่แก้:** กรรมการที่กดอัปโหลดสดจะเห็นการ์ดที่มีแค่ "สินค้าตามในรูป."
  (gallery ที่สร้างไว้ก่อนยังโชว์ข้อความเต็มได้ แต่ live upload จะดูกลวง)

### F-3 (ความรุนแรง: ต่ำ) — `process()` ไม่มี timeout

- **ไฟล์/บรรทัด:** `demo/index.html` บรรทัด 292 (`async function process()`) —
  มี `fetch(` เดียว ไม่มี `AbortController`/`signal` ที่ไหนในไฟล์
- **ผลกระทบ:** ถ้าเซิร์ฟเวอร์ค้าง การกดประมวลผลจะค้างโดยไม่มีข้อความอะไร
  (ปุ่ม disabled ค้าง) — บนเดโม local ความเสี่ยงต่ำ
- **วิธีแก้ที่เสนอ (ยังไม่แก้ในรอบนี้):** เพิ่ม `AbortController` (เช่น 120 วินาที)
  แล้วให้ timeout เข้า path `serverFail` เดิม — เป็นไฟล์ของ PR #4 เอง
  แต่การแก้ตอนนี้จะเปลี่ยน SHA ที่ล็อกไว้ จึงเลื่อนไปทำหลังรอบตรวจนี้พร้อม re-verify เล็กน้อย

### ข้อจำกัดเดิมที่มีอยู่แล้ว (ไม่ใช่ defect — อย่าอ่านเป็นข้ออ้าง)

- Guardrail เป็น regex/keyword (ดูหัวข้อ 2 ตอนท้าย) — paraphrase, สะกดผิด,
  ข้ามประโยค, puffery, nutrition/cert/compat แบบ keyword-only ยังหลุดได้
- การ match กับ seller = ความสอดคล้อง ไม่ใช่ความจริงที่ผ่านการตรวจสอบ
- Gallery 5 ใบเป็นผลลัพธ์ pre-guardrail ที่อ้างอิงฉลากที่เห็น (Tier 1: "ฉลากระบุว่า"
  ไม่ใช่ความจริงทางวิทยาศาสตร์) — ป้าย `galleryNote` บอกไว้ชัดเจนแล้ว

## 6. ประเมินความพร้อมสำหรับ Hackathon (ตามข้อ 6 ของคำสั่ง)

คะแนนด้านล่างคือ**การประเมินของมีนา** (ไม่ใช่คะแนนกรรมการ) ให้เป็นช่วงพร้อม
เหตุผลและลิงก์หลักฐาน — **ไม่ได้บวกคะแนนเพราะ UI สวยหรือเพราะ test เยอะ**
(ดูที่ Demo: ทั้งที่ UI ผ่าน smoke test แต่คะแนนถูกกดเพราะ public link
อัปโหลดไม่ได้ และยังไม่มีวิดีโอ)

| Rubric | คะแนน (ช่วง) | เหตุผล + หลักฐาน |
|---|---|---|
| Impact 30% | **19/30** (18–20) | ปัญหาจริงของพ่อค้าแม่ค้า (ถ่ายรูปมือถือ → ได้การ์ดลงขาย) + กลไก trust (evidence-first guardrail) ที่พิสูจน์ได้ด้วยเทสต์ — แต่**ยังไม่มีผู้ใช้จริง ไม่มี metric** (ยอดผู้ใช้/เวลาที่ประหยัดได้) จึงกดไว้ไม่ให้สูงกว่านี้ หลักฐาน: pipeline live + gallery + guardrail 25/25 |
| Use of Meta AI Tooling 25% | **19/25** (18–20) | ใช้ครบ 3 โมเดลจริงใน pipeline (SAM 3.1 หาตัวสินค้า, Muse Image วาดรูปสตูดิโอ, Muse Spark เขียนข้อความ) — SAM/Image พิสูจน์ live ในรอบนี้, Spark **พิสูจน์ไม่ได้ในรอบนี้** (คืนค่าว่าง 2/2, ดู F-2) จึงไม่ใช่เต็ม หลักฐาน: live logs + โค้ด `run_pipeline` |
| Demo 25% | **17/25** (16–18) | หน้าเดโม static สมบูรณ์ (smoke test ผ่าน, screenshot 4 ขนาด) + อัปโหลดผ่าน `server.py` ได้จริง — แต่ **public link (Pages) อัปโหลดไม่ได้** (ต้องเปิด server) และ**ยังไม่มีวิดีโอเดโม** จึงกดคะแนนไว้ หลักฐาน: screenshots + server-static log |
| Technical Depth & Execution 20% | **15/20** (14–16) | ลึกจริง: fail-closed guardrail, value matching (ราคา/ขนาด + แปลงหน่วย), seller-match≠verified, safe rendering (textContent only), preview URL discipline, vendored deps, self-contained page, เทสต์ 25/25 + harness + live E2E + วินิจฉัยรากของปัญหา Spark ได้ — หักเพราะ F-1, F-3 และ live copy วันนี้ยังเป็น fallback |
| **รวม (ประมาณ)** | **~70/100** (66–74) | เป็นช่วงประเมิน ไม่ใช่คำมั่นสัญญา |

### แยกตามที่คำสั่งขอ

- **สิ่งที่พิสูจน์แล้ว:** pipeline ทำงานต้นจนจบผ่าน `server.py` (SAM box, รูปสตูดิโอ,
  guardrail fail-closed, error paths); หน้าเว็บ self-contained ไม่มี external dependency;
  guardrail 25/25 + harness ครบ; smoke test visual 4 ขนาด; ไม่มีการหลุดของ secret
- **สิ่งที่ทีมรายงานแต่ตรวจซ้ำไม่ได้ในรอบนี้:** ผล pipeline 27 ต.ค. (รูป 5 ใบ,
  ฉลากครบ, ใช้จ่ายต่ำกว่า $1) — เป็น [HISTORICAL] และ**ผล live รอบนี้ไม่ยืนยัน
  ข้ออ้างเรื่องข้อความ Spark** (2/2 ครั้งได้ fallback) — รายงานนี้ไม่ปกปิดความขัดแย้งนี้
- **ช่องว่างที่ยังเหลือ:** F-1 (มล.), F-2 (Spark max_tokens), F-3 (timeout);
  click-scroll / reduced-motion behavior / หน้าตา modal (ยังไม่ได้เห็น);
  รูปเงื่อนไขยาก (ย้อนแสง/มือบัง) ยังไม่ได้รัน live ในรอบนี้
- **ความเสี่ยงที่กรรมการอาจถาม:** (1) "กดอัปโหลดสดแล้วได้ข้อความจริงไหม?"
  — วันนี้คำตอบคือยัง (fallback) จนกว่าจะแก้ F-2; (2) "การ์ด gallery เป็นผล
  จากระบบปัจจุบันหรือไม่?" — ต้องตอบตรงว่าเป็น pre-guardrail (ป้ายบอกไว้แล้ว);
  (3) "guardrail กันการแต่งข้อมูลได้แค่ไหน?" — ต้องตอบตามข้อจำกัด regex
  ไม่ใช่ "กันได้ทั้งหมด"; (4) "ทำไม public link อัปโหลดไม่ได้?" — ต้องอธิบาย
  static Pages vs server.py
- **สิ่งที่ควรแก้ก่อน deadline (เรียงตามผลกระทบต่อคะแนนเทียบกับความยาก):**
  1. **F-2: เพิ่ม max_tokens ของ Spark + รัน live ยืนยัน** — ผลกระทบสูง (Demo+Tooling), ยากต่ำ
     (แก้ 1 บรรทัด + รัน 1 ครั้ง) — ทำก่อนอย่างอื่น
  2. **วิดีโอเดโม + ส่ง Cerebral Valley** — ผลกระทบสูงที่สุด (ไม่มี = ไม่ได้ส่ง),
     ยากปานกลาง — deadline **พฤหัส 5 พ.ย. 2026 09:00 Bangkok**; วิดีโอควรโชว์
     อัปโหลดผ่าน `server.py` ที่ทำงานได้จริง
  3. **F-1: เพิ่ม "มล." ใน `_SIZE_UNITS` + regression tests** — ผลกระทบปานกลาง
     (ความน่าเชื่อถือของเรื่อง trust), ยากต่ำ
  4. **F-3: fetch timeout** — ผลกระทบต่ำ, ยากต่ำ
  5. **เทสต์กับผู้ขายจริง 1–2 คน** — ผลกระทบปานกลางต่อ Impact, ยากสูง (หาเวลา/คน)
     — ทำถ้าเวลายังเหลือหลังข้อ 1–2
  6. **ตัดสินใจเรื่อง public upload** — จะเปิด tunnel ให้ `server.py` รับกรรมการ
     หรือจะชี้แจงในหน้าวิดีโอ/คำอธิบายว่า public link เป็น static gallery —
     เป็นการตัดสินใจของทีม ไม่ใช่การแก้โค้ด

## 7. รายการส่งกลับ (ตามข้อ 8 ของคำสั่ง)

1. **ลิงก์รายงานนี้:** https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/final-readiness-audit-2026-10-29.md
2. **commit SHA เต็มของ PR #4 ที่ตรวจ:** `cbc4c4afa3a43851a93ac1a12177f81d95deeb3a`
3. **ลิงก์ directory หลักฐาน:** https://github.com/Techfrontiers/snapsell-ww/tree/main/brainstorm/evidence/pr4-final
4. **ลิงก์ screenshot ทุกขนาด:** desktop-1440 / mobile-390 / desktop-en-1440 / full-page-1440
   (ดูหัวข้อ 4 — ลิงก์ครบทั้ง 4 ไฟล์)
5. **ลิงก์ test logs และผล Guardrail:** logs/ ใน directory หลักฐาน
   (guardrail 25/25, langswitch, preview, process-swal, process-nonjson, audit-cases)
6. **สรุป PASS / FAIL / NOT TESTED:**
   - Guardrail suite: 25/25 PASS [UNIT, ไฟล์สด]
   - Lang-switch: PASS 40/0 [HARNESS] | Preview: PASS [HARNESS] | process+Swal: PASS [HARNESS]
   - Audit cases (7 กรณี): 11 PASS / 1 FAIL (F-1) [UNIT]
   - Live E2E: pipeline PASS (SAM/Image), copy DEGRADED (F-2), error paths PASS [LIVE]
   - Visual smoke: PASS (overflow/images/TH-EN/mobile) [VISUAL]
   - NOT TESTED (พร้อมเหตุผล): Spark อ่านฉลาก live (คืนค่าว่าง 2/2), รูปเงื่อนไขยาก live,
     click-scroll, reduced-motion behavior, หน้าตา modal/toast
7. **คะแนน Hackathon พร้อมหลักฐาน:** ดูหัวข้อ 6 (~70/100, ช่วง 66–74)
8. **Blocker ที่ยังเหลือและสิ่งที่แก้แล้ว:**
   - **Blocker ที่กันการส่งประกวด: ไม่มี** — ส่งได้ (static demo + วิดีโอ + คำอธิบาย)
   - **ความเสี่ยงสูงสุดต่อคุณภาพเดโมสด: F-2** (Spark คืนค่าว่าง — แก้ด้วย max_tokens + verify live)
   - **Gap ปานกลาง: F-1** (มล.) — แก้เล็กก่อนส่ง
   - **Gap ต่ำ: F-3** (timeout)
   - **สิ่งที่แก้แล้วในรอบก่อน (round 2, ยืนยันในรอบนี้):** compiled Tailwind CSS,
     vendored SweetAlert2 11.26.25, smoke test — ทั้ง 3 ข้อยืนยันซ้ำในรอบนี้แล้วว่ายังอยู่ครบ
9. **ยืนยันสถานะ PR:** PR #4 **ยังเป็น Draft, ยังไม่ Merge, ยังไม่ Deploy เพิ่ม**
   (ตรวจสถานะก่อนส่งรายงานนี้; live URL ตอนนี้ยัง serve รอบ CDN เก่าจาก 07:40)

---

*หมายเหตุสุดท้าย: รายงานนี้ตรวจเฉพาะ commit ที่ล็อกไว้ข้างบนเท่านั้น
ถ้ามี commit ใหม่ (เช่น แก้ F-1/F-2/F-3) ผลในรายงานนี้จะไม่ครอบคลุม commit ใหม่ —
ต้อง re-verify อย่างน้อย guardrail + live run บน commit ใหม่ก่อนอ้างผลเดิม*
