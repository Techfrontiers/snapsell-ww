มีนา: SnapSell demo เป็นเว็บแอป — Tailwind + SweetAlert2 + อนิเมชัน
(คำสั่ง sydear 2026-10-29: "ทำลุคเว็บแอปใหม่ไปเลย แบบ workspace ของแอปจริง")

วันที่: 2026-10-29 ~07:20-07:35 Bangkok

## ผลลัพธ์

- Branch: `webapp-tailwind` จาก `ui-redesign` head 67471580
- Commit: `c798cf40c9dc` (demo/index.html เท่านั้น, +1 commit บน branch)
- PR: https://github.com/Techfrontiers/snapsell-ai/pull/4 — DRAFT, ยังไม่ merge, ยังไม่ deploy
- เปรียบเทียบ main...webapp-tailwind: ไฟล์เดียว demo/index.html, ahead 4, behind 0
- server.py / test_guardrail.py บน branch มี blob ตรงกับ main

## สิ่งที่เปลี่ยน (frontend เท่านั้น)

- Tailwind CSS (Play CDN): sticky header (brand + nav anchors + ปุ่ม TH/EN),
  hero 2 คอลัมน์ (ข้อความซ้าย, Lactasoy Before/After จริงขวา),
  pipeline strip, workspace grid — studio panel sticky ซ้าย
  (dropzone, preview, seller facts, CTA) + ผลลัพธ์/การ์ดขวา
- SweetAlert2 v11 (jsDelivr, pin version): loading modal ตอนประมวลผล,
  success toast (top-end, 3 วินาที), warning modal ตอน needs-confirmation
  (รายละเอียดยังอยู่ในการ์ด), error modal ตอน fail/serverFail/noFile
- ทุกการเรียก Swal อยู่หลัง `if (window.Swal)` — ถ้า CDN โหลดไม่ได้
  หน้าเว็บยังทำงานได้ครบ (พิสูจน์ด้วยเทสต์ no-Swal fallback)
- อนิเมชัน: fade-up ตอนโหลด (hero, showcase, panel, การ์ด),
  hover lift + zoom รูปในการ์ด, เคารพ prefers-reduced-motion
- I18N ใหม่ 5 คีย์ (2 ภาษา): swalOk, needsSwalText,
  navStudio, navResults, navGallery — ค่าเก่า 49 คีย์เหมือนเดิมทุกตัว,
  ข้อความการ์ด 5 ใบเหมือนเดิมทุกตัว

## สิ่งที่คงไว้ (ตรวจด้วยโปรแกรม)

- IDs ครบ (dz, photo, chip, facts, go, status, live, preview, previewWrap),
  form fields (photo, lang, facts), endpoint API_BASE + '/api/process',
  fetch() เดียว (ใน process()), revokeObjectURL เดียว (preview fix),
  gallery attribution + galleryNote, TH/EN ครบ, guardrail ไม่แตะ

## เทสต์ที่รันจริง (บนไฟล์ที่ commit ตรงตัว)

- Guardrail: 25/25 OK
- node --check: OK
- Lang-switch TH→EN→TH: 40 elements, 0 mismatches
- Preview Object-URL: PASS (fix ยังอยู่)
- process() + Swal harness (stub fetch/DOM): PASS ครบ 6 เคส —
  success+needs → loading แล้ว warning modal; success clean → toast;
  !ok → error modal + status; fetch reject → serverFail;
  no file → warning ไม่เรียก fetch; ไม่มี Swal → การ์ด + status ยังทำงาน
- Safe rendering: process() ไม่มี innerHTML, มี textContent + createElement;
  ทั้งไฟล์มี innerHTML เดียวคือ setLang() (static I18N) เหมือนเดิม

## ข้อจำกัดที่ต้องพูดตรงๆ

- สไตล์ขึ้นกับ Tailwind Play CDN ตอนรัน (demo-grade, ต้องมีเน็ต)
- Headless screenshot ใน VM นี้โหลด CDN ไม่ได้เลย — พิสูจน์แล้วว่า
  headless shell เปิดเน็ตไม่ได้แม้แต่ example.com (local JS ทำงานปกติ,
  remote fetch ว่างเปล่าทั้งแบบมีและไม่มี proxy) — บทเรียน: หน้าเว็บที่
  ใช้ CDN ตรวจภาพด้วย headless ใน env นี้ไม่ได้
- Live-browser render check ล้มที่ชั้น tab (เปิด tab ไม่ได้เลย —
  ไม่ใช่ความผิดของหน้าเว็บ) — หน้าตาแบบมีสไตล์จึงยังไม่มีใครเห็น
  ด้วยตาตัวเอง วิธีตรวจจริงคือ deploy แล้วดูบนมือถือ

## สถานะ

- PR #4 เป็น Draft, main ไม่แตะ, ยังไม่ deploy
- Deploy/merge รอคำสั่งทีมอย่างเดียว (deploy จะทับหน้า v2 ที่ live อยู่ตอนนี้)
