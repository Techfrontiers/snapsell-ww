มีนา: UI Redesign สำหรับ SnapSell AI — เสร็จแล้ว รอตรวจบน PR

วันที่: 2026-10-28 ~21:00 Bangkok

## ส่งงาน

- Branch: `ui-redesign` จาก main `2ec9d4ff` (ตรวจ main head
  ตรงก่อนเริ่ม)
- Commit: `7b5b8bf8ff19ac36f4c101ce708f017a1f55615c`
- PR #3 (DRAFT, ยังไม่ merge, ไม่ deploy):
  https://github.com/Techfrontiers/snapsell-ai/pull/3
- Main ไม่แตะ (ยัง `2ec9d4ff`)

## ไฟล์ที่เปลี่ยน

- `demo/index.html` ไฟล์เดียว (+137/-51)
- server.py / test_guardrail.py / deploy_pages.py บน branch
  มี blob ตรงกับ main เป๊ะ — backend, guardrail, endpoint,
  schema, pipeline, model, auth ไม่แตะเลย

## ดีไซน์ (ไฟล์เดียว, ไม่เพิ่ม dependency)

- Dark Graphite (#0d0e12) + gradient Electric Violet → Cyan,
  system font stack, ไม่มี secret ใน frontend
- Topbar บาง + Hero: kicker งาน hackathon, headline
  gradient "One photo. A listing ready to sell." /
  "รูปเดียว ได้การ์ดลงขายพร้อมโพสต์", tagline เดิมคงเดิม
- Pipeline เป็นการ์ด 3 ขั้น SAM 3.1 → Muse Image → Muse Spark
  (ข้อความ `how` เดิมยังเป็น intro ของ section)
- Upload: dropzone กดด้วยคีย์บอร์ดได้ (tabindex + role +
  Enter/Space), hover/focus states, preview รูปก่อนประมวลผล
  (object URL ฝั่ง client อย่างเดียว ไม่เรียก API), textarea
  โทนมืด, CTA gradient, status มีสี error + aria-live
- Gallery: grid 2 คอลัมน์ (มือถือ 1 คอลัมน์), คู่
  before/after เดิม, hover lift + zoom รูป (ปิดเมื่อ
  prefers-reduced-motion), focus-visible ครบ, contrast
  ตรวจแล้วบนพื้นมืด

## สิ่งที่คงไว้ (ตรวจจริง ไม่ได้อ้างลอยๆ)

- ID ทุกตัว, field photo/lang/facts, endpoint
  API_BASE + '/api/process', flow ของ process() เหมือนเดิม
- I18N เดิม 30 keys เหมือนเดิมทุกตัวอักษรทั้ง th/en;
  เพิ่ม key ใหม่ 9 ตัวครบ 2 ภาษา (heroKicker, heroTitle,
  pipeTitle, step1-3 Title/Desc)
- การ์ด gallery 5 ใบเหมือนเดิมทุกตัวอักษร (รวม d3
  attribution + galleryNote TH/EN)
- innerHTML มีที่เดียวคือ setLang (static I18N เท่านั้น);
  process() ยัง render ข้อมูล AI/ผู้ใช้ด้วย
  createElement/textContent เท่านั้น
- ไม่สร้างข้อมูลสินค้าหรือคำกล่าวอ้างใหม่

## ผลทดสอบ (ตัวเลขจริง)

- Guardrail suite: 25/25 OK (รันกับ index.html ใหม่ที่
  redesign แล้ว — รวม 3 test ที่อ่าน index.html เช่น
  safe-rendering)
- JS syntax: node --check ผ่าน
- Lang-switch runtime test (node + DOM stub ใช้โค้ด
  setLang จริง): TH → EN → TH, 35 elements ตรง dict
  ทุกตัว 0 mismatch
- Upload flow: ตรวจแบบ static ไม่ส่ง request ไป API จริง
  เลย — fetch มีตัวเดียวคือของ process() เดิม, preview
  เป็น client-side ล้วน
- Responsive: screenshot จาก headless Chromium จริง
  (desktop 1280 + mobile 390 + full page) — hero, steps,
  upload card, gallery grid 2 คอลัมน์, footer แสดงผลถูก
  ไม่ล้นบนมือถือ

## ข้อจำกัด (พูดตรงๆ)

- Screenshot เป็น render ภาษาไทย (ค่า default);
  ภาษาอังกฤษพิสูจน์ด้วย lang-switch test ข้างบน ไม่ได้
  แคป EN (headless ตั้ง localStorage ล่วงหน้าไม่ได้โดย
  ไม่แก้ไฟล์)
- ไม่ได้ทดสอบอัปโหลด end-to-end กับ API จริง — ตั้งใจ
  งดตามเงื่อนไข (โค้ด path อัปโหลดไม่เปลี่ยน ยกเว้น
  preview + สี status)
- PR นี้ไม่ deploy — เว็บ Pages ที่ live ยังเป็นเวอร์ชัน
  gallery เดิม

## หมายเหตุเครื่องมือ

- put-file helper ใช้ Contents API PUT แบบไม่ส่ง sha —
  ใช้ได้กับไฟล์ใหม่เท่านั้น อัปเดตไฟล์ที่มีอยู่ต้อง PUT
  พร้อม sha ของ blob ปัจจุบัน (รอบนี้ใช้ sha ของ
  index.html บน branch)
- Screenshot: `meta-chromium` ไม่มีใน PATH แต่เจอ
  binary ที่ /opt/meta-chromium/chrome กับ Playwright
  headless shell — ตัวหลังใช้ถ่าย screenshot ได้
  (ตัวแรกถ่ายไม่ออก ต้องใช้ headless shell)

## ยังไม่ได้ทำ

- ไม่ Merge, ไม่ Deploy (รอคำสั่งแยก)
- ไม่เริ่ม Phase 2 งานอื่น (ตามคำสั่ง — รอ redesign
  ผ่านการตรวจก่อน)
