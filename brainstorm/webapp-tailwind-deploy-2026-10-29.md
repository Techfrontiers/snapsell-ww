มีนา: Deploy เว็บแอป (Tailwind + SweetAlert2) ขึ้น Pages ตามคำสั่ง sydear
("deploy เว็บแอปขึ้น live เลย")

วันที่: 2026-10-29 ~07:40 Bangkok

## ผลลัพธ์

- Deployment ID: `304fc51e-bc7a-4ec1-aa92-b1fef5723f5b`
- Project: `snapsell-demo` (Cloudflare Pages, production)
- URL หลัก: https://snapsell-demo.pages.dev/
- URL deployment: https://304fc51e.snapsell-demo.pages.dev/
- Commit ที่ Deploy: branch `webapp-tailwind` ที่ `c798cf40c9dc`
  (ไฟล์ demo/index.html จาก branch, blob 8ebd2dfc0792)
- ไฟล์ที่ Deploy: 11 ไฟล์ — index.html (42,425 bytes)
  + assets 10 ใบ (ตรงกับ main ทุกไฟล์)

## ตรวจก่อน Deploy

- Branch head = c798cf40c9dc ตรง, index มีครบ: Tailwind CDN,
  SweetAlert2 v11, workspace grid, navStudio, galleryNote +
  d3 attribution TH/EN, preview fix (prevPreviewURL)
- Deploy script demo/deploy_pages.py บน branch มี blob
  ตรงกับ main, target snapsell-demo
- Credential ตรวจก่อนด้วย cf.py GET /zones → success
- Secret scan บน dist = clean

## ตรวจหน้าเว็บจริงหลัง Deploy

- จาก NexNodo (path ภายนอก): ทั้ง URL หลักและ URL
  deployment คืน HTTP 200, 42,425 bytes ตรงกับไฟล์
  ที่ Deploy ทุกประการ, มีครบทุก marker
  (หมายเหตุ: grep รอบแรกขึ้น MISSING สำหรับคลาส
  workspace grid เพราะ `[` `]` เป็น regex — ตรวจซ้ำ
  ด้วย fixed-string แล้วพบว่าคลาสอยู่ครบ)
- browser.open คืนสำเนาเก่าที่ crawl ไว้ตอน 07:09 (v2)
  ไม่ใช่ไฟล์ใหม่ — การยืนยันไฟล์ใหม่จึงอ้างอิง
  NexNodo byte-exact check เป็นหลัก

## สถานะที่ต้องจำ

- หน้า live ตอนนี้คือเว็บแอป (ทับ v2 ที่ deploy ตอน 07:10)
  — v2 ยังอยู่ใน branch `ui-redesign` / PR #3 ไม่หายไปไหน
- PR #4 ยังเป็น Draft, main ยัง 2ec9d4ff (ไม่แตะ)
- Static อย่างเดียว ไม่เปิด live server/tunnel — ปุ่ม
  อัปโหลดบนหน้า live จะแสดงข้อความเดิมว่าใช้ไม่ได้ถ้า
  ไม่เปิดผ่าน server.py; Tailwind/SweetAlert2 โหลดจาก
  CDN ตอนเปิดหน้า (ต้องมีเน็ต — บนมือถือโหลดได้ปกติ)
- ย้อนกลับได้: re-deploy จาก main 2ec9d4ff หรือจาก
  ui-redesign 67471580 (v2) ได้ทันที
