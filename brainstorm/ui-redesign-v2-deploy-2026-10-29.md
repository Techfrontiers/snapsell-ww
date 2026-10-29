มีนา: Deploy หน้า UI Redesign v2 ขึ้น Pages ตามคำสั่ง sydear
("ลอง deploy เลย จะดูหน้าตาจริง")

วันที่: 2026-10-29 ~07:10 Bangkok

## ผลลัพธ์

- Deployment ID: `43ac04e9-26ce-4259-b00f-a32a53e617c3`
- Project: `snapsell-demo` (Cloudflare Pages, production)
- URL หลัก: https://snapsell-demo.pages.dev/
- URL deployment: https://43ac04e9.snapsell-demo.pages.dev/
- Commit ที่ Deploy: branch `ui-redesign` ที่ `67471580`
  (ไฟล์ demo/index.html จาก branch, blob 581b3412454b)
- ไฟล์ที่ Deploy: 11 ไฟล์ — index.html (39,698 bytes)
  + assets 10 ใบ (ตรงกับ main ทุกไฟล์)

## ตรวจก่อน Deploy

- Branch head = 67471580 ตรง, index มีครบ: warm
  off-white (--paper), showcase-pair, masthead,
  heroCtaTry, galleryNote + d3 attribution TH/EN,
  preview fix (prevPreviewURL) — ไม่มี marker ของ v1
  dark, ไม่มี gradient
- Deploy script demo/deploy_pages.py บน branch มี blob
  ตรงกับ main, target snapsell-demo
- Credential ตรวจก่อนด้วย cf.py GET /zones → success
- Secret scan บน dist = clean

## ตรวจหน้าเว็บจริงหลัง Deploy

- จาก NexNodo (path ภายนอก): ทั้ง URL หลักและ URL
  deployment คืน HTTP 200, 39,698 bytes ตรงกับไฟล์
  ที่ Deploy ทุกประการ, มีครบทุก marker ของ v2
- Browser fetch ที่ URL หลัก: หน้าโหลดครบ — kicker,
  hero headline, process strip 01/02/03, upload section,
  gallery note + การ์ด 5 ใบ + d3/d4 attribution
- หมายเหตุ: NexNodo tunnel หลุดตอนแรก (127.0.0.1:2222
  refused) — กู้ตามวิธีเดิมแล้วตรวจใหม่ผ่าน

## สถานะที่ต้องจำ

- ที่ Deploy คือโค้ดจาก branch `ui-redesign` เท่านั้น
  — main ยัง `2ec9d4ff` (ไม่แตะ), PR #3 ยังเป็น Draft
  ยังไม่ merge
- Static อย่างเดียว ไม่เปิด live server/tunnel — ปุ่ม
  อัปโหลดบนหน้า live จะแสดงข้อความเดิมว่าใช้ไม่ได้ถ้า
  ไม่เปิดผ่าน server.py (เหมือนเวอร์ชัน gallery เดิม)
  ส่วนที่ดูได้คือหน้าตาและการ์ดตัวอย่าง
- ย้อนกลับได้: ถ้าต้องการกลับไปเวอร์ชัน gallery เดิม
  แค่ re-deploy จาก main 2ec9d4ff
