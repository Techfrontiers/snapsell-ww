มีนา: ขั้นตอน Merge PR #1 — เตรียมไว้ ยังไม่ merge รอคำสั่ง

สถานะ: GPT third-pass review อนุมัติ Phase 1 ในแง่ code review
ตามขอบเขตที่กำหนดแล้ว (ดูคอมเมนต์ล่าสุดใน PR #1)
แต่ GPT ย้ำชัด: อย่า merge อัตโนมัติจากคอมเมนต์รีวิวเพียงอย่างเดียว
ให้ PR คง draft ไว้จนกว่าทีมพร้อม merge — เอกสารนี้คือขั้นตอน
ที่เตรียมไว้ ไม่ใช่การ merge

## สถานะที่ยืนยันแล้ว (2026-10-28, read-only)

- PR #1: open, draft, merged = false
- Branch `phase1-guardrail` head: `16c49d407dbb`
- Main head: `5a7a4cd88fe6` (ยังไม่มี Phase 1)
- Base: main, ไฟล์ที่เปลี่ยน: `demo/server.py`,
  `demo/index.html`, `demo/test_guardrail.py` เท่านั้น
  (ไม่แตะ `snapsell/` stub, ไม่มี secret)
- การอนุมัติของ GPT ไม่ใช่การยืนยันข้อเท็จจริงแบบครอบคลุม
  และไม่ใช่การอนุมัติให้เริ่ม Phase 2 ก่อน merge + ตรวจ main

## ประตูการตัดสินใจ (Decision gate — ต้องมีก่อน merge)

Merge เกิดขึ้นได้ก็ต่อเมื่อ sydear สั่ง merge ชัดเจนในรอบนั้น
(เช่น "merge ได้เลย" พร้อมวิธี merge — ดูตัวเลือกข้างล่าง)
คอมเมนต์อนุมัติของ GPT อย่างเดียวไม่พอ และไม่มีการ merge
อัตโนมัติจากคอมเมนต์ใด ๆ

## Pre-merge checks (รันใหม่ตอนจะ merge ห้ามใช้ผลเก่า)

1. PR ยัง open + draft + head ยังเป็น `16c49d407dbb`
   + base ยังเป็น main + merged ยัง false
2. Main head ยังเป็น `5a7a4cd88fe6` (ไม่มี commit อื่น
   แทรกเข้ามาหลัง review)
3. Diff branch vs main มีแค่ 3 ไฟล์ข้างบน และสแกน secret
   ใน diff ซ้ำ (ห้ามมี api_key, Bearer, sk-, ghp_, token values)
4. รัน mock tests จากไฟล์บน branch head ซ้ำ (ไม่ใช่ work dir เก่า)
   — ต้องได้ 25/25 ก่อน merge
5. เลือกวิธี merge (ให้ sydear เลือกตอนสั่ง):
   - (a) Squash — รวมเป็น commit เดียวบน main ประวัติสะอาด
     (ประวัติการแก้แบบทีละรอบยังอยู่ใน PR comments)
   - (b) Merge commit — เก็บ commit ทีละรอบไว้บน main
   - คำแนะนำของมีนา: (a) Squash เพราะ commit บน branch
     เป็นรอบแก้ review ไม่ใช่ feature ย่อยที่แยกกัน

## ขั้นตอน merge (ทำเมื่อ sydear สั่งแล้วเท่านั้น)

1. Mark PR เป็น Ready for review (undraft) — GitHub ไม่ให้
   merge draft PR
2. Merge ผ่าน API ด้วยวิธีที่เลือก
3. ยืนยัน: PR merged = true, main head เปลี่ยนเป็น commit
   merge ใหม่, tree บน main มี `enforce_claims`,
   `extract_prices`/`extract_sizes`, DOM rendering,
   `test_guardrail.py` ครบ
4. รายงานใน chat + สรุปใน snapsell-ww ว่า merge สำเร็จ
   พร้อม main head ใหม่

## หลัง merge (แยกขั้นตอน ไม่ทำอัตโนมัติ)

- ไม่เริ่ม Phase 2 อัตโนมัติ — เสนอ Phase 2 เป็นขั้นตอนแยก
  ตามที่ GPT ระบุ (ต้องมี brief + approval ใหม่)
- Merge ลง main ไม่เท่ากับ deploy เดโม live: demo server
  (server.py + tunnel) ปิดอยู่, Pages ที่เห็นเป็น static gallery
  แยกต่างหาก — การ deploy เส้นทาง live ต้องสั่งแยก
- Gallery claims audit (เอกสารแยก) ต้องเคลียร์ก่อนเดโมสุดท้าย
  ไม่ว่าจะ merge หรือไม่
- ถ้า main มีปัญหาหลัง merge: revert ด้วย revert PR
  ห้าม force-push ลง main
