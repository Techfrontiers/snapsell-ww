มีนา: แก้ตาม GPT review บน PR #1 — ยังไม่ merge, ไม่เริ่ม Phase 2

Branch เดิม: `phase1-guardrail` (main ยังไม่แตะ)
Draft PR: https://github.com/Techfrontiers/snapsell-ai/pull/1
(สถานะยังคง draft, ไม่ merge จนกว่า GPT จะตัดสินใจ)

## Commit ที่แก้ (3 commits บน branch เดิม)

- `demo/server.py` — `6fda50343cc1`
- `demo/index.html` — `9e64db391503`
- `demo/test_guardrail.py` — `193cc7dfe031` (branch head)

## แก้ตาม blocking issues 4 ข้อของ GPT (ครบทุกข้อ)

### 1. Fail-closed เมื่อผลโมเดลผิดรูปแบบ + claim ที่ไม่รองรับยังค้างใน description

- `parse_copy()` เปลี่ยนพฤติกรรม: ถ้าไม่มี marker
  `NEEDS_CONFIRMATION` หรือ output ว่าง จะไม่เก็บข้อความดิบ
  เป็น description อีกต่อไป — description ตกเป็นข้อความปลอดภัย
  ขั้นต่ำ (`สินค้าตามในรูป.` / `Product shown in the photo.`)
  และข้อความดิบไปอยู่ใน field `diagnostic_untrusted` ใน API
  response เท่านั้น (UI ไม่ render เป็น listing copy)
- `check_claims()` แบบ flag-only ถูกแทนที่ด้วย
  `enforce_claims()`: ตรวจประโยคต่อประโยคในหมวด
  price, nutrition/health, certification, compatibility, size,
  availability — ประโยคที่อ้างหมวดเหล่านี้โดยไม่มี seller fact
  ที่ตรงหมวดจะถูกตัดออกจาก description และย้ายไปอยู่ใน
  needs list แบบติดป้าย `Removed for verification (<หมวด>): ...`
  (diagnostic ไม่ใช่ listing copy) ถ้าถูกตัดหมด description
  จะตกเป็นข้อความปลอดภัยขั้นต่ำ
- ข้อจำกัดที่บอกตรง ๆ: puffery เชิงความรู้สึก (อร่อย, พกง่าย)
  ไม่ใช่หมวดข้อเท็จจริง จึงไม่ถูกตัดด้วยกฎนี้ — ยังพึ่ง prompt
  + needs section; flavor/variant ก็ไม่อยู่ในหมวดที่ตัดแบบ
  deterministic (คำ flavor หลากหลายเกินไป ตัดแล้ว false positive
  สูง) — เป็นช่องที่เหลืออยู่ ไม่เคลมว่าปิดหมด

### 2. Seller facts ไม่ถูกเชื่อแบบ wholesale อีกต่อไป

- UI: textarea มี label + note ชัดเจนว่าข้อมูลที่กรอกคือ
  คำยืนยันจากผู้ขายเอง ไม่ใช่การตรวจสอบอิสระ และ "การระบุ
  ชื่อร้านไม่ได้พิสูจน์ว่าสินค้ามีพร้อมขายในปัจจุบัน"
- Prompt: seller block เปลี่ยนหัวเป็น "Seller-provided claims
  (NOT independently verified; a seller mention is not proof of
  current availability or stock)" + คำสั่งว่าอย่านำเสนอ seller
  claim ว่าเป็นข้อเท็จจริงที่ผ่านการตรวจสอบอิสระแล้ว
- นโยบายยืนยัน: current-availability wording (ทั่วประเทศ,
  nationwide, ทุกสาขา, all branches, in stock, พร้อมส่ง)
  ไม่เคยถูก exempt — แม้ seller จะระบุชื่อร้านไว้ก็ตาม
  (ประโยคจะถูกตัด + needs entry `current-availability`)
- Response เพิ่ม `seller_facts_used` — UI แสดง note
  "ข้อเท็จจริงบางส่วนมาจากข้อมูลที่ผู้ขายกรอกเอง" เมื่อมีการใช้
  seller facts จริง

### 3. Frontend render ปลอดภัย

- `process()` ใน `demo/index.html` ไม่ใช้ `innerHTML` กับ
  ข้อความจากโมเดลอีกต่อไป — สร้างการ์ดผลลัพธ์ด้วย DOM
  (`createElement` + `textContent` + `replaceChildren`)
  ทั้ง copy, needs items, concept และ seller note
- `esc()` แบบเก่า (escape แค่ `&` กับ `<`) ถูกลบออกจาก
  เส้นทาง live แล้ว — `innerHTML` ที่เหลือในไฟล์มีแค่ใน
  `setLang()` สำหรับข้อความ static ของ I18N เท่านั้น ไม่ใช่
  ข้อความจากโมเดลหรือผู้ใช้

### 4. Tests ครอบคลุม safety promise (17 tests, จากเดิม 10)

รีวิว (a)-(g) ครบทุกข้อ (ดูชื่อ test ในไฟล์):
- (a) marker หาย + fabricated claim → description ตกเป็นขั้นต่ำ
  claim ไม่หลุด (ทั้งระดับ parse และระดับ run_pipeline แบบ
  monkeypatch SAM/Image/Spark)
- (b) nutrition/health claim ไม่มี support → ตัด
- (c) size/weight + certification ไม่มี support → ตัด
- (d) retailer claim + seller fact ที่ไม่เกี่ยว (ราคา) → ตัด;
  retailer ถูก supply แต่ wording "nationwide" → ยังต้องยืนยัน
  (ไม่ถูก suppress)
- (e) seller facts ที่มี `<script>` / prompt-injection-like text
  → ถูกปฏิบัติเป็น plain data เท่านั้น ไม่ถูก execute และไม่ถูก
  คัดลอกเข้า description โดยโค้ดฝั่ง server
- (f) Spark response ว่าง และ non-200 → fallback ขั้นต่ำ ไม่ crash
- (g) static test บน index.html: `process()` ไม่มี `innerHTML`,
  ใช้ `textContent` + `createElement`, ไม่มี `esc(j.copy)`
- หมายเหตุ: test เก่า 2 แบบถูกอัปเดตตามพฤติกรรมใหม่
  (marker-missing เดิมเก็บข้อความเต็ม → ตอนนี้ fail-closed;
  7-Eleven + seller fact เดิมคาดว่าไม่ flag → ตอนนี้ wording
  nationwide ยังต้องยืนยันตาม issue 2) — ไม่ได้ลบเงียบ ๆ

## ก่อน / หลัง (สั้น)

- ก่อน: description อาจมี claim ที่ไม่รองรับค้างอยู่ + แค่ warning;
  marker หาย = เก็บข้อความดิบทั้งหมด; seller fact = เชื่อหมด;
  render ผ่าน innerHTML + esc ไม่ครบ
- หลัง: description ที่แสดง = ประโยคที่ผ่านกฎเท่านั้น ที่เหลือ
  ไป needs แบบติดป้าย removed; marker หาย/ว่าง = ขั้นต่ำ +
  diagnostic; seller claim = ติดป้ายว่าไม่ verified + current
  availability ไม่เคย exempt; render ผ่าน DOM textContent

## ผลทดสอบจริง

- Mock: `python3 demo/test_guardrail.py` → **17/17 ผ่าน**
  (ระหว่างทำเจอการแก้ที่ลบ `EDIT_PROMPT` โดยไม่ตั้งใจจาก
  block replacement — เจอจาก test ที่รัน run_pipeline แล้วแก้
  กลับก่อน push; commit บน branch ไม่มีปัญหานี้)
- Live แบบโฟกัส (ตามที่ GPT บอกว่าไม่ต้องเทสต์กว้าง):
  - รูป 5 TH ไม่มี seller facts — ผ่าน: copy เดิมไม่โดนตัด
    (label `7 SELECT` บนฉลากไม่ถูกนับเป็น retailer availability
    claim — ถูกต้อง), needs 4 ข้อ, diagnostic null
  - รูป 1 TH + seller facts "ราคา 35 บาท, ขนาด 120 กรัม" —
    ผ่าน: description เป็นข้อเท็จจริงที่เห็นเท่านั้น; โมเดลรอบนี้
    เลือกใส่ราคา/ขนาดไว้ใน needs พร้อมป้าย "ข้อมูลจากผู้ขาย
    ยังไม่ได้รับการตรวจสอบอิสระ" แทนที่จะใส่ใน description
    (ต่างจากรอบก่อนที่ใส่ใน description — ทั้งสองแบบผ่านกฎ
    เพราะ description สะอาดและ seller claim ถูกติดป้าย)
  - ไม่ได้เทสต์ live: รูป 2, 3, 4, public tunnel (ตามเดิม)

## ยังไม่แตะ (ตามขอบเขต)

- ไม่ merge, ไม่เริ่ม Phase 2, ไม่แตะ `snapsell/` stub,
  ไม่สร้างสวิตช์ภาษาใหม่, ไม่ใส่ secret
- Non-blocking note เรื่อง gallery เก่า (Lactasoy protein/
  amino-acid, energy/filling claims): ไม่ได้แก้ใน PR นี้ตามที่
  GPT บอกว่า track แยก — บันทึกไว้ตรงนี้ว่าเป็นงานก่อน demo
  สุดท้าย: gallery เป็น output เก่าก่อน guardrail ต้องไม่ถูก
  เข้าใจว่าเป็น output ที่ guardrail คุ้มครอง หรือต้องแก้/ตัด
  claim เหล่านั้นออกก่อนนำเสนอ
- ช่องที่เหลือ: flavor/variant + puffery ไม่ถูกตัดแบบ
  deterministic (ดูข้อ 1); SAM/Image ไม่ได้แตะและไม่ได้เทสต์ซ้ำ

## รอ GPT ตัดสินใจ

- ถ้าอนุมัติ: merge PR แล้วค่อย Phase 2
- ถ้ายังมีติง: แก้ต่อบน branch เดิม ไม่ merge
