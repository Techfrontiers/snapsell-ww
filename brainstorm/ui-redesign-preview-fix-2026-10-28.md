มีนา: แก้ Preview Object URL บน PR #3 — รอตรวจรอบสุดท้าย

วันที่: 2026-10-28 ~21:05 Bangkok

## คำสั่ง

แก้เฉพาะการจัดการ Preview Object URL บน branch
`ui-redesign` ต่อจาก commit ปัจจุบัน ห้ามแตะอย่างอื่น
ห้าม Merge/Deploy/main

## ปัญหาเดิม

showChip() เดิมสร้าง URL.createObjectURL() ใหม่ทุกครั้ง
ที่เลือกไฟล์ โดยไม่ปล่อย URL เก่า — blob URL ที่ถูก
แทนที่แล้วค้างสะสม (leak)

## วิธีแก้ (commit be85a5f3 บน ui-redesign)

- เพิ่มตัวแปร prevPreviewURL เก็บ URL ของ preview ปัจจุบัน
- เลือกไฟล์ใหม่: สร้าง URL ใหม่ก่อน → เปลี่ยน img.src
  เป็น URL ใหม่ → จำ URL ใหม่เป็น current → แล้วค่อย
  revoke URL เก่า
- ลำดับนี้รับประกันว่า URL ที่ภาพกำลังใช้อยู่ไม่มีวันถูก
  revoke (revoke เกิดหลัง img ย้ายไป URL ใหม่แล้วเท่านั้น)
- ไม่แตะ object URL ของรูป before ในการ์ดผลลัพธ์
  (process()) — ภาพนั้นยังแสดงอยู่ revoke แล้วการ์ดพัง
- revokeObjectURL ปรากฏในไฟล์ครั้งเดียว (preview เท่านั้น)

## ผลทดสอบบนไฟล์ที่แก้แล้ว (ตัวเลขจริง)

- Preview runtime test (node + DOM stub, โค้ด showChip
  จริง, 12 assertions): PASS ทั้งหมด
  - เลือกไฟล์ A → preview = url1, revoked = []
  - เลือกไฟล์ B → preview = url2, revoked = [url1]
  - drag-and-drop C → input.files ถูกแทนที่, preview =
    url3, revoked = [url1, url2]
  - เลือก A ซ้ำ → preview = url4, revoked =
    [url1, url2, url3]
  - invariant ทุกขั้น: preview src ไม่เคยอยู่ใน revoked set
- Guardrail suite: 25/25 OK (กับ index.html ที่แก้แล้ว)
- JS syntax: node --check OK
- Lang-switch runtime test: TH → EN → TH, 35 elements,
  0 mismatch
- ไฟล์ที่ commit ตรงกับไฟล์ที่ทดสอบ (byte-identical)

## สถานะ PR #3 หลังอัปเดต

- https://github.com/Techfrontiers/snapsell-ai/pull/3
- Head: be85a5f34296, ahead 2 behind 0 vs main
- Diff: demo/index.html ไฟล์เดียว (+145/-51)
- server.py / test_guardrail.py blob ตรง main เป๊ะ
- PR: open, draft, unmerged — body อัปเดต + comment
  แจ้งผลแล้ว
- Main: ยัง 2ec9d4ff (ไม่แตะ), ไม่ Deploy
