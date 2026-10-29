# SnapSell — Backend Reliability Fix (F-2 + F-1)

**สถานะ: READY FOR GPT BACKEND REVIEW** — สถานะนี้หมายถึงพร้อมให้ GPT
ตรวจรอบ backend เท่านั้น **ไม่ใช่การอนุมัติ merge และไม่ใช่การอนุมัติ deploy**

งานนี้ทำตามคำสั่ง GPT รอบ Backend Reliability Fix โดยใช้ผลจาก
[Final Readiness Audit 2026-10-29](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/final-readiness-audit-2026-10-29.md)
เป็นฐาน และ**แยกจาก PR #4 โดยสิ้นเชิง** (PR #4 ไม่ถูกแตะ ไม่ถูก merge
ไม่มี backend change ใดถูกยัดเข้าไป)

## 0. ข้อมูลเวอร์ชัน (ตรวจสด ไม่สมมติจาก SHA ในรายงาน)

- Repo: `Techfrontiers/snapsell-ai`
- Base ที่แยก branch: **main** — HEAD ณ เวลาตรวจ:
  `2ec9d4ff9490655839c7ddc758b0024bf8af5f19`
  (ตรงกับ main ในรอบ audit — แต่ตรวจสด ไม่ได้สมมติ)
- Branch ใหม่: `backend-reliability` (สร้างจาก main HEAD ข้างบน)
- **Backend PR:** https://github.com/Techfrontiers/snapsell-ai/pull/5 (Draft)
- **Commit SHA เต็มสุดท้าย (final SHA): `640b3c1ac83e79d7dc514432583745e35d10136e`**
- Commits บน branch (3 commits, แยกตามงาน):
  1. `e42d0aec82f731baed0d2b1fa0351c2d8a723643` — F-2 (server.py เท่านั้น)
  2. `01ea2c5cc37f36329292e3061e38da606f664b53` — F-1 ส่วน server.py
  3. `640b3c1ac83e79d7dc514432583745e35d10136e` — F-1 ส่วน regression tests
- ไฟล์ที่เปลี่ยนเทียบ main (2 ไฟล์เท่านั้น): `demo/server.py`, `demo/test_guardrail.py`
- วันที่และเวลาทดสอบ: **2026-10-29 ~09:05–09:20 Bangkok**
- หลักฐานกลาง: https://github.com/Techfrontiers/snapsell-ww/tree/main/brainstorm/evidence/backend-fix

### ป้ายวิธีทดสอบ (เหมือนรอบ audit)

- **[LIVE]** = รันจริง (เซิร์ฟเวอร์จริง / API จริง) ในรอบนี้
- **[UNIT]** = unit test บนโค้ดที่ดึงสดจาก branch
- **[STATIC]** = ตรวจโค้ด/diff
- **[HISTORICAL]** = ผลเก่าที่มีวันที่กำกับ — ไม่ใช่หลักฐานของรอบนี้
- การทดสอบทั้งหมดในรายงานนี้รันบน **final SHA** (ดึงไฟล์สดจาก branch
  แล้วตรวจว่า byte-identical กับไฟล์ local ที่แก้) ยกเว้นรายการที่ระบุว่า
  "ก่อนแก้" ซึ่งรันบน main เดิมอย่างชัดเจน

## 1. F-2: แก้ Spark token budget (ปัญหาคุณภาพเดโมที่สำคัญที่สุด)

### 1.1 ตรวจจุดเดิมก่อนแก้ (ไม่สมมติ)

- จุดเรียก Spark เดิม: `demo/server.py` — `call("POST", "/chat/completions",
  {"model": "muse-spark-1.3", ..., "max_tokens": 2048}, timeout=180)`
- การจัดการเดิม: ถ้า `status == 200` จะอ่าน
  `spark["choices"][0]["message"]["content"]` ตรงๆ — ถ้าโครงสร้างผิด
  จะ raise (แล้ว handler จับเป็น `{ok: false}`); ถ้า content ว่าง
  จะไหลเข้า `parse_copy("")` → fallback (MIN_DESC + FALLBACK_NEEDS)
- ไม่มี finish_reason, ไม่มี retry, ไม่มีข้อมูลวินิจฉัยใน response
- หลักฐานจาก audit ที่ใช้เป็นฐาน: Spark คืนค่าว่าง 2/2 ครั้ง
  (`diagnostic_untrusted = "empty model output"`), วินิจฉัยตรงพบว่า
  prompt ง่ายๆ ใช้ reasoning ~450 token, budget 256 → `length`/null,
  budget 4096 → `stop`/content

### 1.2 สิ่งที่แก้ (commit `e42d0aec`)

1. **`max_tokens` 2048 → 8192** — ค่า 8192 เป็นจุดเริ่มต้นจากหลักฐาน
   (ไม่ใช่ค่าที่ถือว่าถูกโดยอัตโนมัติ): งานจริง (prompt ไทยยาว + รูป)
   ต้องการ reasoning มากกว่า prompt ทดสอบที่กินไป ~450 token อยู่แล้ว
   และการรัน live หลังแก้คือตัวพิสูจน์ว่าค่านี้พอหรือไม่
2. **Retry 1 ครั้งเมื่อ content ว่าง** (เฉพาะกรณี `status == 200`
   แต่ content ว่าง — คือ failure mode ที่วินิจฉัยได้) ถ้ายังว่างอยู่
   จะไหลเข้า fail-closed path เดิม ไม่มีการแต่งข้อความ
3. **ดึงค่าแบบ defensive** (`_extract`): โครงสร้าง response ผิด
   (ไม่มี choices/message/content) จะถือว่าว่าง + `finish_reason =
   "parse_error"` ไม่ crash เป็น `{ok: false}` อีกต่อไป
4. **เปิดเผยข้อมูลวินิจฉัยใน response (เพิ่มฟิลด์แบบ additive, UI ไม่ใช้
   ก็ไม่กระทบ):** `spark_finish_reason` (เช่น `"stop"`, `"length"`,
   `"parse_error"`, หรือ `null` เมื่อไม่ได้เรียก Spark) และ
   `spark_retried` (bool)
5. **Timeout ของ Spark 180 → 300 วินาที** (เท่ากับ SAM call เดิม)
   เพราะ budget ที่ใหญ่ขึ้นหมายถึงเวลาสร้างที่นานขึ้น

ไม่มีการเปลี่ยน prompt, pipeline, guardrail logic, หรือ response schema
เดิม — ฟิลด์ใหม่เป็นส่วนเสริมเท่านั้น

### 1.3 ผล live: ก่อนแก้ vs หลังแก้ (รูปเดียวกัน, facts เดียวกัน)

รูปทดสอบ: `before3.jpg` (Lactasoy) — รูปเดียวกับ audit run 2;
facts: "แลคตาซอย นมถั่วเหลือง สูตรต้นตำรับ 500 มล." (ตรงกับฉลาก)

| รายการ | ก่อนแก้ [LIVE, audit 2026-10-29] | หลังแก้ [LIVE, รอบนี้, final SHA] |
|---|---|---|
| `ok` / concept / box | `true` / `product` / [128,808,739,1682,921,2048] | `true` / `product` / [128,808,739,1682,921,2048] (SAM deterministic — box เดิมเป๊ะ) |
| `spark_finish_reason` | (ไม่มีฟิลด์นี้) | `"stop"` |
| `spark_retried` | (ไม่มีฟิลด์นี้) | `false` (เรียกครั้งแรกสำเร็จ ไม่ต้อง retry) |
| ข้อความที่ผ่าน guardrail แล้ว | "สินค้าตามในรูป." (15 ตัวอักษร — **fallback**) | **284 ตัวอักษร — ข้อความจริง** (ดูด้านล่าง) |
| `diagnostic_untrusted` | `"empty model output"` | `null` (marker ครบ โครงสร้างถูกต้อง) |
| `needs_confirmation` | FALLBACK_NEEDS ข้อเดียว | 4 ข้อที่ซื่อสัตย์ (ดูด้านล่าง) |
| เวลา | ~28 วินาที | ~25.7 วินาที (budget ใหญ่ขึ้นแต่ไม่ช้าลง) |
| รูปสตูดิโอ | 1600×1600 จริง | 1600×1600 จริง (b64 ~4.07M ตัวอักษร) |

**ข้อความหลังแก้ (เต็ม, ผ่าน guardrail แล้ว):**

> แลคตาซอย Lactasoy สูตรต้นตำรับ Original 500 มล.
> บรรจุภัณฑ์เป็นกล่องสีฟ้า-ขาวยี่ห้อ Lactasoy SINCE 1981 มีแถบคำว่า
> Delicious และมีฝาเปิดพร้อมหลอดเสียบด้านบน หน้ากล่องระบุข้อความ
> แลคตาซอย สูตรต้นตำรับ และ Lactasoy Original พร้อมปริมาตรสุทธิ 500 มล.
> ด้านล่างกล่องระบุ PRODUCT OF THAILAND

**ตรวจว่าไม่มีการแต่ง (ตามข้อ 5 ของคำสั่ง):**
- ไม่มีราคา, ไม่มีค่าจัดส่ง, ไม่มีสต็อก/ความพร้อมจำหน่าย,
  ไม่มีคุณสมบัติโภชนาการ, ไม่มีการรับรอง, ไม่มีข้อความสุขภาพ
- "500 มล." ตรงกับ facts และมองเห็นบนกล่อง (label-quoted)
- สิ่งที่ยังยืนยันไม่ได้ถูกกันออกไปเป็น needs ครบถ้วน:
  (1) "นมถั่วเหลือง" ตามที่ผู้ขายระบุยังไม่เห็นชัดในรูป → ต้องยืนยัน
  (2) ข้อมูลผู้ขายยังไม่ได้รับการตรวจสอบอิสระ ไม่ใช่หลักฐานสต็อก
  (3) ราคา/ค่าจัดส่ง/สต็อก/วันหมดอายุ/สภาพสินค้า
  (4) โภชนาการ/ส่วนผสม/การรับรอง/ข้อความสุขภาพโดยละเอียด
- สรุป: **F-2 แก้ได้จริง — ข้อความมีประโยชน์ ไม่ใช่ fallback**
  (และไม่ได้ PASS เพราะ fallback ทำงาน — fallback ไม่ได้ถูกใช้เลยในรันนี้)

หลักฐาน live หลังแก้ (redacted — studio_b64 แทนด้วยความยาว, ไม่มี secret):
[logs-live-after-redacted.json](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/logs/logs-live-after-redacted.json) —
รูปสตูดิโอจากรันนี้:
[live-studio-after.png](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/live-studio-after.png)

### 1.4 ถ้า API ยังคืนค่าว่าง (กรณีที่ไม่ได้เกิดในรอบนี้)

รอบนี้ไม่เกิด (ได้ `"stop"` ตั้งแต่ครั้งแรก) จึงไม่มีการวินิจฉัยรอบสอง —
แต่กลไกที่ใส่ไว้รองรับกรณีนั้น: retry 1 ครั้ง → ยังว่าง → fallback
อย่างซื่อสัตย์ + `finish_reason` ใน response จะบอกสาเหตุ
(`"length"` = budget ยังไม่พอ → เพิ่มอีก, `"parse_error"` =
โครงสร้างเปลี่ยน, `null` = ไม่ได้เรียก/ไม่ใช่ 200) — จะไม่มีการ
เปลี่ยนผลเป็น PASS เพียงเพราะ fallback ทำงาน

## 2. F-1: รองรับหน่วย "มล." (ตามข้อ 7–9 ของคำสั่ง)

### 2.1 สิ่งที่แก้ (commits `01ea2c5c` + `640b3c1a`)

- `demo/server.py` บรรทัด `_SIZE_UNITS`: เพิ่ม `(r"มล\.?", "volume", 1.0)`
  ต่อจาก `"มิลลิลิตร|ml"` — ครอบคลุมทั้ง "มล." และ "มล" (ไม่มีจุด)
  ตรวจแล้วว่าไม่ชนกับ "มิลลิลิตร" (substring "มล" ไม่ปรากฏในคำนั้น)
  และไม่ชนกับ "ลิตร"
- `demo/test_guardrail.py` (คลาส TestValueMatching): เพิ่ม regression tests
  5 เคสตามที่คำสั่งขอ (ครบ 4 กรณีขั้นต่ำ + รูปแบบไม่มีจุดเป็นโบนัส):
  1. `test_ml_conflict_stripped` — "500 มล." ขัดกับ facts "600 มล." → ตัดเป็น size-mismatch
  2. `test_ml_matching_kept` — "500 มล." ตรงกับ facts "500 มล." → เก็บไว้
  3. `test_ml_without_seller_facts_stripped` — "500 มล." ไม่มี facts → ตัดเป็น size-unverified
  4. `test_no_size_text_unaffected` — ข้อความไม่มีขนาด → ไม่เปลี่ยนแปลง (กัน false positive)
  5. `test_ml_without_dot_stripped` — "500 มล" (ไม่มีจุด) ไม่มี facts → ตัด

### 2.2 ผลก่อนและหลังแก้ (บันทึกครบ)

| ชุดทดสอบ | ก่อนแก้ (main เดิม) | หลังแก้ (final SHA, ไฟล์สดจาก branch) |
|---|---|---|
| Test suite เดิมทั้งหมด | **25/25 PASS** ([log](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/logs/logs-baseline.txt)) | — (รวมอยู่ในชุดหลังแก้) |
| Regression "มล." 5 เคส (ไฟล์แยก, รันกับโค้ดเดิม) | **2 PASS / 3 FAIL** — FAIL คือ conflict, without-facts, without-dot (ตรงกับช่องโหว่ที่รายงาน) ([log](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/logs/logs-regress-before.txt)) | — |
| Test suite เต็มหลังแก้ (25 เดิม + 5 ใหม่) | — | **30/30 PASS** ([log](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/logs/logs-suite-finalsha.txt)) |
| Audit cases 7 กรณี (สคริปต์รอบ audit, expectation แก้ให้ตรงกับพฤติกรรมที่ถูกต้องของ enforce_claims — stripped = MIN_DESC) | 11 PASS / 1 FAIL (F-1) | **12/12 PASS** ([log](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/logs/logs-audit-finalsha.txt)) |

หลักฐานว่า F-1 ป้องกันความขัดแย้งของ "มล." ได้จริง (ตามข้อ 5 ที่ขอ):
เคส `test_ml_conflict_stripped` — input "ขนาด 500 มล." + facts "ขนาด 600 มล."
→ หลังแก้ได้ `safe = MIN_DESC` และ `removed` มี `size-mismatch`
(ก่อนแก้ได้ `safe = "ขนาด 500 มล."` และ `removed = []` คือเผยแพร่ค่าผิด)

สคริปต์ regression (ไฟล์แยกที่ใช้รันก่อนแก้):
[regress_ml.py](https://github.com/Techfrontiers/snapsell-ww/blob/main/brainstorm/evidence/backend-fix/regress_ml.py)
— ส่วนที่ commit จริงอยู่ใน `demo/test_guardrail.py` บน branch แล้ว

## 3. รายการไฟล์ที่เปลี่ยนและเหตุผล (ตามข้อ 2 ที่ขอ)

| ไฟล์ (บน backend PR, เทียบ main) | เปลี่ยนอะไร | เหตุผล |
|---|---|---|
| `demo/server.py` | Spark `max_tokens` 2048 → 8192; timeout 180 → 300; เพิ่ม `_spark_call`/`_extract`; retry 1 ครั้งเมื่อ content ว่าง; เพิ่ม response fields `spark_finish_reason` + `spark_retried`; `_SIZE_UNITS` เพิ่ม `มล\.?` | F-2 (token budget + empty handling + วินิจฉัยได้) และ F-1 (หน่วยไทยที่หายไป) — ทั้งหมดอยู่ในไฟล์ backend เดียวกัน ไม่แตะ UI, prompt, pipeline, guardrail logic อื่น |
| `demo/test_guardrail.py` | เพิ่ม regression tests 5 เคสใน TestValueMatching | F-1 — พิสูจน์ว่าช่องโหว่ถูกปิดและไม่เกิด false positive |

ไม่มีไฟล์อื่นเปลี่ยน — `demo/index.html`, CSS, JS, assets, `deploy_pages.py`,
และ PR #4 ไม่ถูกแตะต้อง

## 4. ข้อจำกัดที่ยังเหลือและผลกระทบต่อเดโม (ตามข้อ 6 ที่ขอ)

1. **ค่า 8192 เป็นจุดเริ่มต้นที่พิสูจน์แล้วว่าใช้ได้กับเคสนี้ ไม่ใช่ค่าที่รับประกันทุกเคส**
   — prompt ที่ยาวกว่านี้ / รูปที่ซับซ้อนกว่านี้ อาจต้องการ reasoning มากกว่านี้อีก
   ถ้าวันหนึ่งกลับมาเจอ `finish_reason "length"` อีก วิธีแก้คือเพิ่ม budget ต่อไป
   (และ `spark_finish_reason` ใน response จะบอกทันที)
2. **Retry ครอบคลุมเฉพาะ content ว่างเมื่อ status 200** — ถ้า API คืน non-200
   (rate limit, server error) จะยัง fallback ทันทีโดยไม่ retry (ตั้งใจ — ไม่ต้องการ
   ซ้ำเติม rate limit) ถ้าอยากให้ทนทานกว่านี้ ต้องออกแบบ retry แบบ backoff แยกกัน
3. **Guardrail ยังเป็น regex/keyword** (ข้อจำกัดเดิมจาก audit) — F-1 ปิดช่อง "มล."
   แต่ paraphrase, สะกดผิด, ข้ามประโยค, puffery ยังหลุดได้เหมือนเดิม
   การผ่านเทสต์ไม่ได้แปลว่ากันการแต่งข้อมูลได้ทั้งหมด
4. **"มล." ที่เพิ่มมาเป็นหน่วยปริมาตร** — ถ้ามีข้อความ "500 มล" ในบริบทอื่น
   (ไม่ใช่ขนาดสินค้า) ก็จะถูกตรวจแบบขนาดเช่นกัน — ยอมรับได้เพราะรูปแบบ
   ตัวเลข+หน่วยแบบนี้ในลิสติ้งสินค้าเกือบทั้งหมดคือขนาด
5. **Live run รอบนี้ใช้รูปเดียว (before3) + facts เดียว** — เป็นการพิสูจน์
   F-2 บนเคสเดียวกับ audit (เปรียบเทียบ before/after ได้ตรง) แต่ไม่ใช่การ
   รับประกันว่ารูปอื่นจะได้ข้อความสมบูรณ์ทุกครั้ง
6. **Public link ยังเป็น static gallery** — งาน backend นี้แก้ `server.py`
   แต่ไม่ได้ทำให้ public Pages URL อัปโหลดได้ (ต้องเปิด server แยก)
   ประเด็นนี้ยังรอการตัดสินใจของทีม (เหมือนที่ audit ระบุไว้)
7. **F-3 (fetch timeout) ยังไม่ได้แก้ในรอบนี้** — อยู่นอกขอบเขตคำสั่งรอบนี้
   (คำสั่งรอบนี้คือ F-2 + F-1) และเป็นไฟล์ UI ของ PR #4 — จะแก้ก็ต่อเมื่อ
   มีคำสั่งแยก (และต้อง re-verify บน SHA ใหม่เช่นกัน)

## 5. รายการส่งกลับ (ตามที่คำสั่งขอ)

1. **URL ของ backend PR และ commit SHA เต็ม:**
   https://github.com/Techfrontiers/snapsell-ai/pull/5 (Draft) —
   final SHA `640b3c1ac83e79d7dc514432583745e35d10136e`
2. **รายการไฟล์ที่เปลี่ยนและเหตุผล:** ดูหัวข้อ 3
3. **ผล test suite และ regression tests:** ดูหัวข้อ 2.2
   (baseline 25/25 → regress-before 2/5 → final 30/30, audit cases 12/12)
4. **หลักฐาน live pipeline ก่อนและหลังแก้ F-2:** ดูหัวข้อ 1.3
   (ก่อน: fallback 15 ตัวอักษร / หลัง: 284 ตัวอักษร + `finish_reason "stop"`)
5. **หลักฐานว่า F-1 ป้องกันความขัดแย้งของ "มล." ได้จริง:** ดูหัวข้อ 2.2
6. **ข้อจำกัดที่ยังเหลือและผลกระทบต่อเดโม:** ดูหัวข้อ 4

## 6. ยืนยันสถานะ (ตามคำสั่ง)

- Backend PR นี้สร้างเป็น **Draft** แยกจาก PR #4 — **ไม่ได้ merge, ไม่ได้ deploy**
- PR #4 **ไม่ถูกแก้, ไม่ถูก merge, ไม่ถูกปิด, ไม่เปลี่ยนสถานะ**
  (ตรวจแล้วก่อนส่งรายงานนี้: head ยังเป็น `cbc4c4afa3a43851a93ac1a12177f81d95deeb3a`, Draft, unmerged)
- ไม่มี secret, API key, หรือข้อมูลที่ยังไม่ได้ redact ใน commit, รายงาน,
  หรือหลักฐานใดๆ (live logs ใช้แบบ redact แล้ว; API เรียกผ่าน connector flow)

---

*รายงานนี้ตรวจและทดสอบบน final SHA `640b3c1ac83e79d7dc514432583745e35d10136e`
เท่านั้น — commit ใหม่หลังจากนี้ต้องทดสอบใหม่ก่อนอ้างผลเดิม*
