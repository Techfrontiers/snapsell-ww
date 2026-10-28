มีนา: Deploy SnapSell Gallery ขึ้น Cloudflare Pages สำเร็จ

วันที่: 2026-10-28 ~20:52 Bangkok

## ผลลัพธ์

- Deployment ID: `c9777d49-b760-4659-9b48-84b27ec91597`
- Project: `snapsell-demo` (Cloudflare Pages)
- Environment: production, stage deploy = success
- URL (deployment): https://c9777d49.snapsell-demo.pages.dev/
- URL (หลัก): https://snapsell-demo.pages.dev/
- Commit ที่ Deploy: main `2ec9d4ff9490655839c7ddc758b0024bf8af5f19`
  (Phase 1 + Gallery merge — ตรวจ main head ตรงก่อน Deploy)
- ไฟล์ที่ Deploy: 11 ไฟล์, 2,101,571 bytes — `index.html`
  (30,057 bytes, ตรงกับ main blob `c03a8bf60f92`) + assets
  10 ใบ (before/after 1–5) — ไม่มีไฟล์อื่น ไม่มี server.py
  ไม่มี test ไม่มี secret (scan ก่อน Deploy = clean)

## ตรวจก่อน Deploy (ตามขั้นตอนที่ทีมให้)

1. Sync จาก main ล่าสุด — main head = `2ec9d4ff...` ตรง
2. ไฟล์ที่จะ Deploy มี Gallery Attribution TH/EN + Lactasoy d3
   เวอร์ชันล่าสุดครบทั้ง 5 ข้อความ — ไม่ใช้ dist เก่า
   (สร้าง dist ใหม่สดจาก main commit ทุกไฟล์)
3. อ่าน `demo/deploy_pages.py` จาก main — target ในโค้ดคือ
   `PROJECT = "snapsell-demo"` (docstring บรรทัดแรกเขียน
   'helios' ค้างไว้ เป็นข้อความเก่า โค้ดจริงใช้ snapsell-demo)
4. Deploy เฉพาะ Static Gallery — ไม่เปิด live server/tunnel
   ไม่เผยแพร่ API key หรือ secret ใดๆ (สคริปต์พิมพ์เฉพาะ
   id/url/status ไม่พิมพ์ token)
5. Credential ตรวจก่อนด้วย harmless read (`cf.py GET /zones`
   → success) จึงดำเนินการต่อ

## ตรวจหน้าเว็บจริงหลัง Deploy

- ตรวจจาก NexNodo (path ภายนอก — VM curl ตรงเชื่อไม่ได้):
  ทั้ง 2 URL คืน HTTP 200, 30,057 bytes ตรงกับไฟล์ที่ Deploy
  และมีครบทั้ง 5 ข้อความ: TH attribution, satiety ที่รวม
  clause, EN attribution, galleryNote TH, galleryNote EN
- ตรวจด้วย browser fetch ที่ URL หลัก: หน้าโหลดครบ การ์ด
  5 ใบอยู่ครบ, note TH อยู่ใต้หัวข้อ Gallery,
  Lactasoy d3 แสดงข้อความ "บนกล่องระบุว่าให้โปรตีน...
  และให้ความอิ่มท้อง..." ถูกต้อง, CIELO d4 ยังมี attribution
  เดิม — EN อยู่ใน I18N dict ของไฟล์ที่ Deploy แล้ว
  (ตัวสลับภาษาเป็น setLang เดิม ไม่ได้แตะ)

## หมายเหตุระหว่างทาง

- NexNodo tunnel หลุดตอนจะตรวจหน้าเว็บ (127.0.0.1:2222
  refused) — กู้ตามวิธีเดิม (copy service + daemon-reload
  + enable --now) แล้วตรวจใหม่ผ่าน ไม่เกี่ยวกับตัว Deploy

## สิ่งที่ไม่ได้ทำ

- ไม่เปิด live server/tunnel — หน้าเว็บเป็น static gallery
  อย่างเดียว (ปุ่มอัปโหลดจะแจ้งว่าใช้ไม่ได้ถ้าไม่เปิดผ่าน
  server.py ตามข้อความเดิมบนหน้า)
- ไม่เริ่ม Phase 2
