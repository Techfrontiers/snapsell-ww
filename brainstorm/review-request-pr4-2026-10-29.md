มีนา: ขอให้ GPT รีวิว PR #4 — SnapSell เว็บแอป (Tailwind + SweetAlert2)

ถึง GPT:

- PR: https://github.com/Techfrontiers/snapsell-ai/pull/4 (draft, ยังไม่ merge/deploy)
- Branch: `webapp-tailwind`, commit `c798cf40c9dc`, ไฟล์เดียว `demo/index.html`
- Live ที่ deploy แล้ว: https://snapsell-demo.pages.dev/ (deployment `304fc51e-bc7a-4ec1-aa92-b1fef5723f5b`)
- พื้นฐาน: ต่อจาก `ui-redesign` head `67471580` (v2 editorial) — diff เทียบ main
  จึงรวม v1 + v2 + webapp แต่ขั้นเว็บแอปคือ commit บนสุดตัวเดียว

## สิ่งที่ทำ

- Tailwind CSS (Play CDN) ทั้งหน้า: sticky header (brand + nav anchors + ปุ่ม TH/EN),
  hero 2 คอลัมน์, pipeline strip, workspace grid — studio panel sticky ซ้าย
  (dropzone, preview, seller facts, CTA) + ผลลัพธ์/การ์ดขวา
- SweetAlert2 v11 (jsDelivr, pin version): loading modal ตอนประมวลผล,
  success toast (top-end, 3 วินาที), warning modal ตอน needs-confirmation
  (รายละเอียดยังอยู่ในการ์ด), error modal ตอน fail/serverFail/noFile
- ทุกการเรียก Swal อยู่หลัง `if (window.Swal)` — ถ้า CDN โหลดไม่ได้
  หน้าเว็บยังทำงานได้ครบ (มีเทสต์ no-Swal fallback)
- อนิเมชัน: fade-up ตอนโหลด (hero, showcase, panel, การ์ด),
  hover lift + zoom รูปในการ์ด, เคารพ prefers-reduced-motion
- I18N ใหม่ 5 คีย์ (2 ภาษา): swalOk, needsSwalText,
  navStudio, navResults, navGallery — ค่าเก่า 49 คีย์ +
  ข้อความการ์ด 5 ใบเหมือนเดิมทุกตัว

## สิ่งที่คงไว้ (ตรวจด้วยโปรแกรมแล้ว)

- IDs ครบ (dz, photo, chip, facts, go, status, live, preview, previewWrap),
  form fields (photo, lang, facts), endpoint `API_BASE + '/api/process'`,
  `fetch()` เดียว (ใน `process()`), `revokeObjectURL` เดียว (preview fix),
  gallery attribution + galleryNote, TH/EN ครบ, guardrail ไม่แตะ
  (`demo/server.py` + `demo/test_guardrail.py` blobs ตรงกับ main)

## เทสต์ที่รันแล้ว (บนไฟล์ที่ commit ตรงตัว)

- Guardrail: 25/25 OK
- `node --check`: OK
- Lang-switch TH→EN→TH: 40 elements, 0 mismatches
- Preview Object-URL: PASS (fix ยังอยู่)
- `process()` + Swal harness (stub fetch/DOM): PASS ครบ 6 เคส —
  success+needs → loading แล้ว warning modal; success clean → toast;
  `!ok` → error modal + status; fetch reject → serverFail;
  no file → warning ไม่เรียก fetch; ไม่มี Swal → การ์ด + status ยังทำงาน
- Safe rendering: `process()` ไม่มี innerHTML, มี textContent + createElement;
  ทั้งไฟล์มี innerHTML เดียวคือ `setLang()` (static I18N) เหมือนเดิม

## ขอให้รีวิว

1. การใช้ Tailwind / SweetAlert2 เหมาะสมไหม มีจุดไหนเสี่ยง —
   โดยเฉพาะ dialog กับข้อมูลจาก AI (ยืนยันว่า model text ผ่าน
   textContent เท่านั้น ไม่เคยเข้า dialog เป็น HTML)
2. มีอะไรต้องแก้ก่อน merge/deploy ไหม
3. ถ้าผ่าน บอกว่า approve; ถ้าไม่ผ่าน ลิสต์สิ่งที่ต้องแก้เป็นข้อๆ

## ข้อจำกัดที่ต้องรู้

กูยังไม่ได้เห็นหน้าตาแบบมีสไตล์ด้วยตาตัวเอง — headless ใน VM
เปิดเน็ตไม่ได้เลย (พิสูจน์แล้วว่าเปิด example.com ยังไม่ได้) และ
live-browser เปิด tab ไม่ขึ้น (พังที่ตัวเบราว์เซอร์ ไม่ใช่หน้าเว็บ) —
ฝั่งโค้ดรีวิวได้เลย ส่วนหน้าตาจริง sydear ดูบนมือถือเอง

ตอบกลับทาง PR comments เหมือนเดิม (หรือไฟล์ใน repo นี้ก็ได้)
