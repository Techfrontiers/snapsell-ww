มีนา: โปรเจคตัวจริงอยู่ใน snapsell-ai แล้ว — GPT รีวิวจากตรงนั้น อย่าเริ่มใหม่จากเอกสาร brainstorm อย่างเดียว

Repo: https://github.com/Techfrontiers/snapsell-ai
Head หลัง publish (Oct 28): `5a7a4cd88fe6af41ea3b7121af3e8bf515b4a40c`
(ก่อน publish: `f4d16f46a31b`, 18 ไฟล์ → หลัง publish: 45 ไฟล์)

## อะไรอยู่ใน repo แล้วบ้าง

- `demo/server.py` + `demo/index.html` — เส้นทาง live ตัวจริง
  (SAM box → crop → Muse Image → Muse Spark, พร้อมสวิตช์ EN/TH)
- `snapsell/` — skeleton แบบ stub (live branch ยังไม่ต่อ อย่าแก้ตรงนี้)
- `snapsell-test-photos/` — รูปเทสต์ต้นฉบับ 5 รูป (ทำให้
  `snapsell/run.py --all` ใช้งานได้จริง)
- `demo/assets/` — รูป before/after 5 ชุด ที่ `demo/index.html`
  อ้างถึง (ก่อนหน้านี้ assets ไม่อยู่ใน repo ทำให้เดโมใน repo
  เปิดแล้วรูปหาย)
- `live-test/batch_live.py` + `live-test/*.json` + `live-test/README.md`
  — batch runner และหลักฐาน API response ของรูป 1, 2, 3, 5
  (รูป 4 Cielo ไม่มี batch JSON ผลของมันอยู่ใน `demo/assets/`
  เพราะรันผ่าน demo server ไม่ใช่ batch script)

## เรื่อง API — ตรวจสอบแล้ว ไม่มี key ใน git

- ตรวจไฟล์ทุกไฟล์ที่จะ push ด้วย pattern: `api_key` ที่มีค่า,
  `Bearer`, `sk-`, `ghp_`, `github_pat`, `access_token`,
  `refresh_token`, `client_secret` — ผล: ไม่เจอ
- คำว่า token ที่เจอใน JSON เป็นแค่ตัวนับ usage
  (`input_tokens` / `output_tokens`) กับพารามิเตอร์ `max_tokens`
  ไม่ใช่ credential
- โค้ดเรียก Meta API ผ่าน helper ของ connected account บนเครื่อง
  ที่รันเท่านั้น key ไม่เคยอยู่ในไฟล์
- ที่จงใจไม่ push: `__pycache__`, probe intermediates, รูป PNG
  ระหว่างทาง (รัน `batch_live.py` ใหม่ได้), deployment config
  (`op.sydear.space.vhost`)

## GPT ควรอ่านอะไรก่อน

1. `demo/server.py` — เส้นทาง live (นี่คือจุดแก้ Phase 1/2)
2. `brainstorm/phase0-inspection-2026-10-28.md` (repo นี้) —
   ผลตรวจ Phase 0 ที่รอ GPT อนุมัติ
3. `live-test/README.md` — ขอบเขตหลักฐานเทสต์ 5 รูป
