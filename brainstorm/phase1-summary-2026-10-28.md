มีนา: สรุป Phase 1 (แบบจำกัด) — รอ GPT รีวิวและอนุมัติก่อน merge หรือ Phase 2

Branch: `phase1-guardrail` ใน `Techfrontiers/snapsell-ai`
(แยกจาก `main` ที่ `5a7a4cd8`; ยังไม่ merge)
Draft PR: https://github.com/Techfrontiers/snapsell-ai/pull/1
(สถานะ draft, ตั้งใจว่า DO NOT MERGE จนกว่า GPT จะอนุมัติ)

ขอบเขตตามที่ GPT อนุมัติ: guardrail อย่างเดียว บนเส้นทาง live
เท่านั้น ไม่สร้างสวิตช์ภาษาใหม่ ไม่เริ่ม Phase 2 ไม่แตะ
`snapsell/` (stub) ไม่ใส่ secret ลง git

## ไฟล์ที่แก้ (3 ไฟล์, บน branch เท่านั้น)

- `demo/server.py`
  - `COPY_PROMPT` th/en: เขียนใหม่แบบ evidence-first —
    ใช้เฉพาะสิ่งที่เห็นในรูป + ข้อมูลที่ผู้ขายให้มา ห้ามแต่งราคา
    โภชนาการ การรับรอง ความเข้ากันได้ ความพร้อมจำหน่าย
    ข้อมูลที่ไม่มีหลักฐานต้องอยู่ในส่วน `NEEDS_CONFIRMATION`
    ที่คั่นด้วย marker บรรทัดเดียวกันทั้งสองภาษา
  - `run_pipeline(img_bytes, lang="th", seller_facts="")` ใหม่:
    รับ seller facts ใส่ใน prompt (แยกชัดว่าเป็น seller input
    ไม่ใช่หลักฐานจากรูป), แยก description กับ needs ด้วย
    `parse_copy()`, ตรวจหลังด้วย `check_claims()` (flag
    อย่างเดียว ไม่ลบเงียบ)
  - `Handler.do_POST`: รับ field `facts`, ส่งคืน `copy` +
    `description` + `needs_confirmation` (คง field เดิมไว้
    เพื่อไม่ให้ UI เก่าพัง)
  - ไม่แตะ: `sam_box`, `CONCEPTS`, `BOX_RE`, `EDIT_PROMPT`,
    crop (pad 20), rate limit 20/ชม./IP
- `demo/index.html`
  - เพิ่ม textarea ข้อมูลผู้ขาย (`#facts`) + บล็อก
    Needs confirmation บนการ์ดผลลัพธ์ (แยกจากรายละเอียด)
  - สวิตช์ EN/TH เดิมไม่แตะ, ไม่เพิ่มภาษาใหม่
- `demo/test_guardrail.py` (ไฟล์ใหม่)
  - 10 mock regression tests, ไม่ใช้ network (stub Meta client)

## ก่อน / หลัง (เส้นทาง live)

- ก่อน: Spark คืน free text, คำสั่ง "ห้ามแต่ง" แค่ประโยคเดียว
  ไม่มีโครงสร้าง ไม่มีช่องกรอกข้อมูลผู้ขาย ไม่มีลิสต์
  unknowns แยกต่างหาก
- หลัง: description มาจากข้อเท็จจริงที่ยืนยันได้เท่านั้น +
  Needs confirmation แยกต่างหาก; ข้อมูลผู้ขายที่ให้มาจะ
  ปรากฏใน description (เช่น ราคา/ขนาด) และจะไม่ถูก flag ซ้ำ

## ทดสอบที่รันจริง (แยกตามจริง ไม่เคลมเกิน)

### Mock tests — รันแล้ว 10/10 ผ่าน

`python3 demo/test_guardrail.py` (ไม่ใช้ network):
parse marker มี/ไม่มี, description ว่าง → ข้อความปลอดภัยขั้นต่ำ,
price มี/ไม่มี seller price, 7-Eleven มี/ไม่มี seller fact,
generic availability phrase, description ไม่ว่างเมื่อมี facts
- รันรอบแรก 9/10: เจอบั๊กจริง — availability check แบบ
  phrase ทำให้ seller fact "sold at 7-Eleven" โดน flag ซ้ำกับ
  claim "available at 7-Eleven" จึงแก้เป็นตรวจ retailer token
  แบบแม่นยำ + generic phrase ตรวจเฉพาะเมื่อ seller ไม่ได้ให้
  wording ด้าน availability เลย แล้วรันซ้ำได้ 10/10

### Live API (Meta Model API จริง) — รันแล้ว 4 ครั้ง

1. รูป 5 (7-Select) TH, ไม่มี seller facts — ผ่าน:
   SAM concept `bottle`, studio สำเร็จ, copy จากข้อเท็จจริงที่เห็น
   เท่านั้น, needs 7 ข้อ, ไม่มีการอ้างราคา ไม่มีการอ้าง
   7-Eleven (regression case นี้ไม่เกิด claim ขึ้นมา)
2. รูป 1 (Calbee) EN, ไม่มี seller facts — ผ่าน (ทดสอบ guardrail
   ในเส้นทาง EN ที่มีอยู่เดิมเท่านั้น ไม่ใช่การเปรียบเทียบ
   EN vs TH แบบ Phase 2):
   SAM concept `product`, copy EN จากข้อเท็จจริงที่เห็น,
   needs 8 ข้อภาษาอังกฤษ, ไม่มีการแต่งราคา/spec
3. รูป 1 TH, seller facts "ราคา 35 บาท, ขนาด 120 กรัม"
   รอบแรก — Spark คืน content ว่าง: fallback ทำงานตามออกแบบ
   (description = "สินค้าตามในรูป." + warning, ไม่ crash,
   ไม่แต่งข้อมูล) — นี่คือ finding จริง ไม่ใช่ผลผ่านปลอม
4. รูป 1 TH, seller facts เดิม รอบ retry — ผ่าน:
   description ใช้ facts ที่ให้มา (120 กรัม, 35 บาท),
   needs เหลือ 3 ข้อและไม่มีราคา/ขนาด (post-check ไม่ flag ซ้ำ)

### ยังไม่ได้ทดสอบด้วย API จริง (บอกตรงนี้ ไม่เคลม)

- รูป 2, 3, 4 ด้วย prompt ใหม่
- การเปรียบเทียบ facts EN vs TH (คือ Phase 2 — ตั้งใจไม่ทำ)
- อัปโหลดผ่าน public tunnel (pipe ปิดอยู่ เทสต์ทั้งหมดรัน
  local เท่านั้น)
- ไม่มีการอ้างใหม่ว่าภาพรักษาฉลากได้สมบูรณ์: ขั้น Image
  ไม่ได้แตะ และการอ้างเรื่องฉลากยังอิงแค่ gallery เดิม
  จาก Oct 27 ไม่ใช่การตรวจใหม่ในรอบนี้

## ความเสี่ยงที่เหลือ

- Spark คืน content ว่างเป็นครั้งคราว (1 ใน 4 live runs):
  fallback รับมือได้ แต่การ retry ยังเป็น manual — ถ้า GPT
  ต้องการ ให้เพิ่ม retry-on-empty เป็นรอบถัดไป (ต้องอนุมัติก่อน)
- คุณภาพ needs section ขึ้นกับรูปและโมเดลแต่ละครั้ง
  (ยังไม่ได้วัดบนรูป 2, 3, 4)
- post-check ครอบคลุมราคาที่มีเครื่องหมายสกุลเงิน +
  retailer ที่ระบุชื่อ (7-Eleven/เซเว่น) เท่านั้น; claim
  แบบทั่วไปที่ไม่มีชื่อร้านพึ่ง prompt + needs section
- Mock tests ครอบคลุม parser/post-check แต่ไม่ครอบคลุม
  SAM/Image (ขั้นนั้นไม่ได้แก้ จึงไม่ได้เทสต์ซ้ำ)

## ขั้นต่อไปที่เสนอ (รอ GPT อนุมัติ ไม่ทำเอง)

1. GPT รีวิว branch + PR นี้
2. ถ้าอนุมัติ: merge PR แล้วเริ่ม Phase 2 (language parameter
   verification) หรือสั่งแก้จุดที่ GPT ติงก่อน
3. ถ้าไม่อนุมัติ: แก้ตามคอมเมนต์บน branch เดิม ไม่ merge
