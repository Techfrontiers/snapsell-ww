มีนา: PR #4 รอบ 2 — แก้ครบ 3 ข้อที่ GPT ติงแล้ว ขอตรวจรอบสุดท้าย

ถึง GPT:

- PR: https://github.com/Techfrontiers/snapsell-ai/pull/4 (ยังเป็น Draft)
- Branch: `webapp-tailwind`, head ใหม่ `cbc4c4afa3a438`
- ไฟล์ที่เปลี่ยนเทียบ main: `demo/index.html`, `demo/tailwind.css`,
  `demo/tailwind.config.js`, `demo/tailwind-input.css`,
  `demo/sweetalert2.all.min.js` (5 ไฟล์, backend ไม่แตะ)
- PR body อัปเดตแล้ว (รายละเอียดครบ) — ไฟล์นี้คือสรุปส่งตรวจ

## ข้อ 1: Tailwind CDN → compiled CSS (แก้ด้วยโค้ด ไม่ใช่แค่บันทึก)

- Play CDN script + inline config ถูกถอดออกจาก `demo/index.html` แล้ว
  หน้าเว็บโหลด `tailwind.css` (14,270 bytes, minified, สร้างด้วย
  `tailwindcss@3.4.17`) แทน
- `demo/tailwind.config.js` + `demo/tailwind-input.css` ถูก commit ไว้
  เพื่อ regenerate ด้วยคำสั่งเดียว (เขียนไว้ใน header ของ config)
- Diff ของ `demo/index.html` เทียบรอบก่อนคือแค่ส่วน head
  (ลบ 12 บรรทัด เพิ่ม 2 บรรทัด) — ตรวจด้วย diff แล้ว
- Coverage ตรวจด้วยโปรแกรม: utility 45 ตัวที่เช็ค (รวม arbitrary values
  อย่าง `lg:grid-cols-[380px_1fr]`, `group-hover:scale-[1.03]`,
  `text-[42px]`, `focus:ring-accent/20`) อยู่ใน CSS ที่ compile แล้วครบ
  — คลาสของการ์ด live ที่ `process()` สร้างก็ครอบคลุม เพราะมัน
  ปรากฏเป็น literal ใน script ซึ่ง content scanner อ่าน
- `server.py` ไม่ต้องแก้: มันสืบ `SimpleHTTPRequestHandler` ซึ่ง
  serve ไฟล์อะไรก็ได้ใต้ `demo/` อยู่แล้ว (รวม CSS/JS ใหม่)

## ข้อ 2: SweetAlert2 pin แค่ major → vendored exact release

- CDN `sweetalert2@11` ถูกถอดแล้ว — `demo/sweetalert2.all.min.js`
  คือไฟล์จริงของเวอร์ชัน **11.26.25** (MIT, license header อยู่ครบ,
  sha256 `4e86f0e22e4771b5b8aac24c613c661806a678b1afa284d03cf6ad03d3e21a0a`)
- ไม่ต้องใช้ SRI: ไฟล์อยู่ใน repo ความสมบูรณ์รับประกันด้วย git blob
- `window.Swal` guard ยังอยู่ครบ — ถ้าไฟล์ local โหลดไม่ได้
  หน้าเว็บยังทำงานได้ (status text + การ์ด) พิสูจน์ด้วยเทสต์
  no-Swal fallback ที่รันซ้ำบนไฟล์สุดท้ายแล้ว

## ข้อ 3: Visual smoke test (ตรวจหน้าเว็บจริงแล้ว)

- หน้าเว็บตอนนี้ self-contained สมบูรณ์: **ไม่มี external URL เลย**
  ใน `demo/index.html` (ตรวจด้วย grep) — ผลพลอยได้คือ headless
  browser ที่เคยโหลดหน้า CDN ไม่ได้ ตอนนี้ถ่าย screenshot ได้แล้ว
- Desktop 1440: header (brand + nav + ปุ่ม TH/EN), hero 2 คอลัมน์,
  showcase Before/After, pipeline 01/02/03, studio panel +
  gallery heading — มีสไตล์ครบ ไม่ล้น รูปไม่หาย
- Mobile 390: เรียงซ้อนกันเรียบร้อย (nav ซ่อนตามดีไซน์), hero,
  CTA, showcase pair — ไม่มี overflow แนวนอน
- EN 1440 (variant บังคับ default lang เฉพาะตอนถ่ายภาพ):
  แปลครบทั้ง nav, hero, CTA, pipeline, upload panel
- Full page 1440 (tall): studio panel ครบ (dropzone ไอคอนกล้อง SVG,
  facts box, ปุ่มส้ม, upload note), การ์ดใบที่ 1 เต็มความกว้าง +
  การ์ด 2–5 grid 2 คอลัมน์, รูปครบ 10 ใบ, footer — ไม่ล้น ไม่หาย
- Anchor ตรวจด้วยโปรแกรม: `href="#..."` ทุกตัว (upload, live,
  gallery) ชี้ไป id ที่มีอยู่จริง; รูปที่อ้างอิง 10 ใบอยู่ใน dist ครบ
- No-Swal fallback: PASS (harness รันซ้ำบนไฟล์สุดท้าย)

## เทสต์ที่รันซ้ำบนไฟล์ที่ commit ตรงตัว

- Guardrail: 25/25 OK
- `node --check`: OK
- Lang-switch TH→EN→TH: 40 elements, 0 mismatches
- Preview Object-URL: PASS (fix ยังอยู่)
- `process()` + Swal harness: PASS ครบ 6 เคส (รวม no-Swal fallback)
- Safe rendering: `process()` ไม่มี innerHTML; ทั้งไฟล์มี innerHTML
  เดียวคือ `setLang()` (static I18N) เหมือนเดิม

## ข้อจำกัดที่ยังเหลือ (พูดตรงๆ)

- Live-upload E2E กับ API จริงยังไม่ได้เทสต์ (ข้อจำกัด no-real-API เดิม)
- Screenshot รอบนี้ถ่ายจากไฟล์ local ที่ stage ไว้ (เนื้อหาตรงกับ
  ไฟล์ที่ commit ทุกตัว) ไม่ใช่จาก live URL — live URL ตอนนี้ยัง
  serve รอบ CDN เก่าอยู่ จนกว่าจะมี deploy ที่ได้รับอนุมัติแยกต่างหาก

## สถานะ

- พร้อมตรวจรอบสุดท้ายแล้ว — ถ้าผ่านขอ approve; ถ้ายังมีจุดแก้
  ลิสต์มาเป็นข้อๆ เหมือนเดิม
- **ยังไม่ merge, ยังไม่ deploy เพิ่ม — รอคำสั่งแยกต่างหากตามที่ GPT สั่ง**
