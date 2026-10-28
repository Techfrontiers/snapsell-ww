มีนา: Visual Redesign v2 — Premium Editorial Commerce
(แทน v1 ที่ยังดูเป็น template SaaS ทั่วไป)

วันที่: 2026-10-28 ~21:15 Bangkok

## ส่งงาน

- Branch: `ui-redesign` ต่อจาก be85a5f3
- Commit ใหม่: `674715800cdb8905e62604a12a01a5eaa5eb378e`
- PR #3 ยังเป็น DRAFT (body + comment อัปเดตแล้ว):
  https://github.com/Techfrontiers/snapsell-ai/pull/3
- Main: ยัง `2ec9d4ff` (ไม่แตะ), ไม่ Deploy

## ทำไมต้องรอบใหม่

v1 (พื้นมืด + gradient + การ์ด generic) โครงสร้างและ
ฟังก์ชันถูก แต่ไม่มี visual hierarchy และไม่แสดงคุณค่า
ของผลิตภัณฑ์ผ่านภาพ — GPT ตัดสินว่าไม่ผ่านด้าน Visual
Design รอบนี้จึงเปลี่ยน composition จริง ไม่ใช่แค่เปลี่ยนสี

## Art Direction ใหม่

- พื้น warm off-white (#faf7f1), ผิวกระดาษ #fffdf8
- Headline serif (Georgia stack; ภาษาไทย fallback เป็น
  ฟอนต์ไทยของเครื่อง) + body sans
- Accent สีเดียว: burnt sienna #b23a12 (ขาวบนสีนี้
  contrast ผ่าน)
- เส้น hairline, พื้นเรียบ — ไม่มี gradient, ไม่มี glow,
  ไม่มีเงาหนัก, ไม่มีการ์ดซ้อนการ์ด, ไม่มี emoji แทนงาน
  ออกแบบ (ไอคอนกล้องใน dropzone เป็น SVG outline,
  📎 หน้าชื่อไฟล์เอาออก)

## Composition ใหม่

- Hero split: ซ้าย = kicker + headline serif ใหญ่ +
  tagline + ปุ่ม anchor 2 ปุ่ม (ลองอัปโหลด / ดูผลลัพธ์);
  ขวา = showcase Before/After จริง (Lactasoy
  before3/after3 จาก assets เดิม — รูปถ่ายรกๆ เทียบกับ
  รูปสตูดิโอสะอาด) เห็นคุณค่าในไม่กี่วินาที
  ไม่สร้างภาพสินค้าใหม่ ไม่อ้างผลลัพธ์ที่ไม่มีจริง
- Pipeline เป็น strip กระชับ: ตัวเลข serif 01/02/03
  คั่นด้วยเส้น (key เดิม ไม่ใช่การ์ด 3 ใบแบบเดิม)
- Upload เป็น bench 2 คอลัมน์เงียบๆ ใต้เส้น hairline:
  dropzone + preview ซ้าย, facts + CTA + status ขวา
  เป็นส่วนหนึ่งของ flow ไม่แย่งซีน Hero
- Gallery ภาพนำ มีจังหวะ: grid 6 คอลัมน์ การ์ด 1–2
  span 3 (แถวบน 2 ใบใหญ่) การ์ด 3–5 span 2 (แถวล่าง
  3 ใบเล็ก) — การ์ด 5 ใบเหมือนเดิมทุกตัวอักษร
  attribution + galleryNote ครบ
- ข้อความใหม่แค่ 2 ปุ่ม (heroCtaTry/heroCtaSee ครบ
  2 ภาษา); I18N เดิม 47 keys เหมือนเดิมทุกตัว

## Screenshot (ตัดสินด้วยตาจริง ไม่ใช่คำอธิบาย)

ถ่ายจาก headless Chromium ของจริง:
- v2 desktop 1440 TH, v2 desktop 1440 EN, v2 mobile 390,
  v2 full page 1440, v1 desktop 1440 + v1 mobile 390
  (เทียบขนาดเดียวกัน)
- ผลที่เห็น: hero split + showcase อ่านค่าทันที,
  process strip, upload bench, gallery rhythm, footer
  แสดงผลตามออกแบบ มือถือไม่ล้น EN แปลครบทั้ง
  showcase captions และปุ่ม
- ภาพ EN: ใช้ variant ที่บังคับ default lang เป็น 'en'
  เพื่อแคปเท่านั้น (แก้บรรทัดเดียว) — ไฟล์ที่ commit
  ไม่เปลี่ยน และการสลับภาษาพิสูจน์ด้วย runtime test
- ความเห็นตรงๆ: รอบนี้หลุดจาก template แล้ว — องค์
  ประกอบแบบ editorial (masthead + hairline + serif +
  ภาพนำ) ต่างจาก v1 ชัดเจน ไม่ใช่แค่เปลี่ยนสี/เงา

## ผลทดสอบบนไฟล์ v2 (ตัวเลขจริง)

- Guardrail: 25/25 OK (กับ index.html v2)
- JS syntax: node --check OK
- Lang-switch runtime: TH → EN → TH, 37 elements,
  0 mismatch
- Preview Object URL: file-select + drag-and-drop +
  เลือกซ้ำ PASS, in-use URL ไม่เคยถูก revoke,
  preview fix ครบ (revoke ครั้งเดียว, live-result URL
  ไม่แตะ)
- Diff: demo/index.html ไฟล์เดียว (+187/-56 vs main);
  server.py / test_guardrail.py blob ตรง main เป๊ะ
- ไฟล์ที่ commit ตรงกับไฟล์ที่ทดสอบ (byte-identical)
- ไม่ส่ง request ไป API จริงเลย

## ยังไม่ได้ทำ

- ไม่ Merge, ไม่ Deploy — PR เป็น Draft รอตรวจภาพ
  และอนุมัติ
- ไม่เริ่ม Phase 2 งานอื่น
