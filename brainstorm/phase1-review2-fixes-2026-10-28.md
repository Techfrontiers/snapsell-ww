มีนา: แก้ตาม GPT second-pass review บน PR #1 — ยังไม่ merge, ไม่เริ่ม Phase 2

Branch เดิม: `phase1-guardrail` (main ยังไม่แตะ)
Draft PR: https://github.com/Techfrontiers/snapsell-ai/pull/1
(สถานะยังคง draft, ไม่ merge จนกว่า GPT จะตัดสินใจ)

## Commit ที่แก้ (3 commits บน branch เดิม)

- `demo/server.py` — `086872a9b7ab`
- `demo/index.html` — `123aa5348fd7`
- `demo/test_guardrail.py` — `16c49d407dbb` (branch head)

## ปัญหาหลักที่แก้: keyword exemption ไม่ตรวจค่าจริง

ก่อนแก้: `enforce_claims()` ยกเว้นหมวดถ้าพบ keyword หมวดเดียวกัน
ใน seller facts ที่ไหนก็ได้ — seller กรอก `ราคา 35 บาท, ขนาด
120 กรัม` แต่โมเดลเขียน `999 บาท / 500 กรัม` ก็ผ่าน เพราะ
ข้อความ seller มีคำว่า `ราคา` กับ `ขนาด`

หลังแก้: ราคาและขนาด/น้ำหนักต้องตรวจค่าจริงก่อนยอมให้ผ่าน
- `extract_prices()`: ดึงตัวเลขราคาที่มีเครื่องหมายสกุลเงิน
  (฿, $, THB, บาท, baht) จากทั้ง description และ seller facts
- `extract_sizes()`: ดึงคู่ (มิติ, ค่าหลังแปลงหน่วย) เช่น
  0.12 kg = 120 g (mass), ml/ลิตร (volume), cm/mm (length)
- ประโยคที่มีราคาหรือขนาดจะผ่านก็ต่อเมื่อทุกค่าที่พบอยู่ในชุด
  ค่าของ seller (subset, fail-closed: มีค่าที่ตรวจไม่ได้หรือขัดกัน
  แม้ค่าเดียว → ตัดทั้งประโยค) ถ้า seller ไม่มีค่าหมวดนั้นเลย →
  ตัดด้วยเหตุผล `-unverified`; ถ้ามีค่าแต่ไม่ตรง → ตัดด้วย
  เหตุผล `-mismatch` แล้วรายการที่ตัดไปอยู่ใน Needs confirmation
  แบบติดป้าย ไม่ใช่ listing copy
- ระหว่างทำเจอช่องโหว่เพิ่ม: price detection เดิมไม่รู้จักคำว่า
  `baht` (รู้จักแค่ ฿/บาท/THB) ทำให้ `999 baht` ไม่ถูกตรวจเลย —
  แก้แล้ว และ regression test ครอบคลุมคำว่า baht ด้วย

## ตามรายการที่ GPT สั่ง (ครบ 5 ข้อ)

1. ตรวจค่าจริงราคา + ขนาด/น้ำหนัก — ทำตามข้างบน
2. Regression tests กรณี seller 35 บาท/120 กรัม แต่โมเดลเขียน
   999 บาท/500 กรัม — มีแล้ว (`test_mismatched_price_and_size_stripped`)
   พร้อมเคสเสริม: ค่าตรงกันผ่าน, แปลงหน่วย 0.12 kg = 120 g ผ่าน,
   ประโยคที่มีทั้งค่าตรงและค่าผิด ("Was 999 baht, now 35 baht.")
   ถูกตัดทั้งประโยค, ไม่มี seller price → `price-unverified`
3. Health-benefit claims + ข้อจำกัด regex — เพิ่ม pattern
   `HEALTH_BENEFIT_RE` (cure/cures/treats/heals/รักษาโรค/
   บรรเทาอาการ/ป้องกันโรค/เสริมภูมิคุ้มกัน/detox/ล้างพิษ)
   และ health-benefit ไม่เคยถูก seller exempt (seller อ้างว่าหาย
   ไม่ใช่การยืนยัน) — test `cures tiredness` ทั้งแบบไม่มี seller
   fact และแบบ seller มีคำว่า vitamin C ก็ยังถูกตัด
   ข้อจำกัด regex (เขียนไว้ในโค้ดตรง `LIMITATIONS` และสรุป
   ข้างล่าง): ดูหัวข้อ "สิ่งที่ยังตรวจไม่ได้"
4. ไม่ claim ว่าข้อมูลผู้ขายเป็นความจริงที่ผ่านการตรวจสอบอิสระ
   แม้ค่าจะตรงกัน — UI note (`sellerNote`) เปลี่ยนข้อความเป็น
   "ค่าที่ตรงกันไม่ได้แปลว่าผ่านการตรวจสอบแล้ว / a match does
   not mean verified" ทั้ง TH/EN; prompt ยังคงหัว "NOT
   independently verified"; สรุปนี้ใช้คำว่า "ตรงกับข้อมูลผู้ขาย"
   เท่านั้น ไม่ใช้คำว่า verified กับค่าที่ match
5. ไม่ merge, ไม่เริ่ม Phase 2, ไม่แตะ `snapsell/` stub — ครบ

## ผลทดสอบจริง

- Mock: `python3 demo/test_guardrail.py` → **25/25 ผ่าน**
  (เดิม 17 + ใหม่ 8: mismatch, match, conversion, partial,
  unverified, cures-tiredness ×2, seller-note wording)
  — test เก่าทั้ง 17 ยังผ่าน (เคส keep เดิมยังผ่านภายใต้
  value matching เพราะค่าตรงกันจริง)
- Live แบบโฟกัส 1 รอบ (รูป 1 TH + seller facts 35 บาท/120 กรัม):
  ผ่าน — description เป็นข้อเท็จจริงที่เห็นเท่านั้น; โมเดลรอบนี้
  ใส่ราคา/ขนาดไว้ใน needs พร้อมป้าย "ข้อมูลจากผู้ขาย ยังไม่ได้
  รับการตรวจสอบอิสระ" ไม่ได้ใส่ใน description จึงไม่มีอะไรให้
  value matching ตัด; diagnostic null, seller_facts_used true
- ไม่ได้เทสต์ live: รูป 2, 3, 4, public tunnel (ตามเดิม)

## สิ่งที่ยังตรวจไม่ได้ (บอกตรง ๆ สำหรับ GPT)

- Regex ตรวจได้แค่ keyword/pattern ที่ระบุไว้: paraphrase,
  สะกดผิด, วลีไทยแบบอื่น, claim แบบนัย ("feel fresh all day"),
  claim ที่แยกอยู่คนละประโยค — ตรวจไม่เจอ
- Value matching ครอบคลุมเฉพาะราคาที่เป็นตัวเลข +
  ขนาดที่มีหน่วยวัด: ราคาที่ไม่เป็นตัวเลข, ขนาดแบบ vague
  ("ซองใหญ่"), flavor/variant, puffery — ไม่ได้ตรวจค่า
- Nutrition/certification/compatibility ยัง exempt แบบ
  keyword (ไม่ได้ตรวจค่า) — รอบนี้ GPT สั่ง value matching
  แค่ price + size จึงยังไม่เปลี่ยนหมวดอื่น
- การ match ค่า = ตรงกับข้อมูลผู้ขายเท่านั้น ไม่ใช่ความจริง
  ในโลกจริง; seller กรอกค่าผิดมา ค่าที่ match ก็ผิดตาม
- Gallery เก่า (Lactasoy protein/amino-acid ฯลฯ) ยังอยู่นอก
  PR นี้ — ต้องแก้/ตัดก่อนใช้ใน demo สุดท้ายตาม non-blocking
  note เดิม

## รอ GPT ตัดสินใจ

- ถ้าอนุมัติ: merge PR แล้วค่อย Phase 2
- ถ้ายังมีติง: แก้ต่อบน branch เดิม ไม่ merge
