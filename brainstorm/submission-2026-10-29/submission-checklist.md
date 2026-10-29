# SnapSell AI — Submission Checklist (2026-10-29)

โน้ต: ไฟล์นี้เขียนภาษาไทยไว้ให้ sydear เช็ค ส่วนอีก 3 ไฟล์ในโฟลเดอร์นี้เป็นภาษาอังกฤษ
พร้อมคัดลอกไปกรอกพอร์ทัลจริง (project-description.md, demo-script.md, known-limitations.md)

## กำหนดส่ง (ยืนยันแล้ว)

- ส่งผ่านพอร์ทัล Cerebral Valley ภายใน **4 พ.ย. 2026 21:00 น. ET = 5 พ.ย. 2026 09:00 น. ไทย**
- แทร็ก: **Indie** — โครงการเดียวส่งได้แทร็กเดียวเท่านั้น
- ธีม: **(1) Build for Your World**
- เกณฑ์ตัดสิน: Impact 30% / Use of Meta AI Tooling 25% / Demo 25% / Technical Depth & Execution 20%
- ตัดสิน 4–8 พ.ย., ประกาศผล 9 พ.ย. (ตามหน้า Cerebral Valley)

## UNVERIFIED — อย่าเดา ต้องเช็คตอนกรอกฟอร์มจริง

- ฟิลด์ทั้งหมดของฟอร์มส่งงาน (หน้า submit ไม่ได้เปิดเผยฟิลด์ต่อสาธารณะ ณ 17 ต.ค.)
- พอร์ทัลรับวิดีโอจากโฮสต์ไหนบ้าง (YouTube / อัปโหลดตรง / ลิงก์อื่น)
- ต้องแนบลิงก์ repo หรือ public demo link หรือไม่ (ยังไม่เคยยืนยันจากแหล่งทางการ)
- ภาษาที่ใช้ส่ง (แพ็กเกจนี้เตรียมภาษาอังกฤษไว้เป็นหลัก)

วิธีรับมือ: แพ็กเกจนี้เตรียมข้อความพร้อมแปะไว้ครบทุกฟิลด์ที่น่าจะมี
(title, one-liner, description, demo URL, video URL, repo URL, track, team)
ถึงเวลาส่งก็แค่แปะตามช่องที่มีอยู่จริง ช่องไหนไม่มีก็ข้าม ไม่ต้องแต่งเพิ่ม

## สถานะงาน (ณ 29 ต.ค. 11:30 น.)

| งาน | สถานะ |
|---|---|
| โค้ดหลักบน main (guardrail Phase 1 + gallery) | DONE — main `2ec9d4ff` |
| เว็บแอป UI (PR #4) | DONE, รอคำสั่ง — GPT Final Review: **PASS WITH SCOPE LIMITS**, ไม่ได้อนุมัติ merge/deploy |
| แก้ backend F-2/F-1 (PR #5) | DONE, รอคำสั่ง — GPT Backend Review: **PASS สำหรับขอบเขต F-2/F-1**, ไม่ได้อนุมัติ merge/deploy |
| Final Readiness Audit (SHA-locked) | DONE — ดู `brainstorm/final-readiness-audit-2026-10-29.md` |
| Submission package (โฟลเดอร์นี้) | DONE |
| วิดีโอเดโม | **MANUAL — ยังไม่ได้บันทึก** (ดู demo-script.md) |
| กรอกฟอร์ม + กดส่งบนพอร์ทัล | **MANUAL — รอคนกด** |
| ยืนยันผลการส่ง (confirmation) | MANUAL — เก็บหลักฐานหลังกดส่ง |

## PR #4 / PR #5 — คงสถานะเดิม ห้ามแตะ

- ทั้ง 2 PR ยังเป็น **DRAFT, ไม่ได้ merge, ไม่ได้ deploy**
- รีวิว GPT ทั้ง 2 อันเป็นแบบ COMMENTED (ไม่ใช่ approval) และระบุชัดว่า
  **"No merge or deploy is authorized by this comment"**
- ห้ามเปลี่ยน Draft เป็น Ready for review, ห้าม merge, ห้าม deploy, ห้ามปิด PR
  จนกว่าจะมีคำสั่งแยกต่างหากจากเจ้าของโปรเจกต์

## URL ที่จะส่ง (ใช้ตามนี้ อย่าพูดเกินจริง)

- **ลิงก์หลักให้กรรมการกดดู:** https://snapsell-demo.pages.dev/
  - ความจริงที่ตรวจจาก NexNodo 29 ต.ค.: HTTP 200, 42,425 bytes = เว็บแอปรอบ CDN เก่า
    (รอบ 1, deploy `304fc51e`) + แกลเลอรีภาพนิ่ง
  - **ลิงก์นี้ไม่รองรับ live upload** — หน้าอัปโหลดต้องใช้ server.py รันบนเครื่อง
    (API_BASE ยังเป็น placeholder) ห้ามเขียนในฟอร์มว่า public URL อัปโหลดได้
- **วิดีโอเดโม = หลักฐานหลักของ flow อัปโหลด** (บันทึกตาม demo-script.md)
- **Repo:** https://github.com/Techfrontiers/snapsell-ai
  - PR #4 (UI): https://github.com/Techfrontiers/snapsell-ai/pull/4
  - PR #5 (backend): https://github.com/Techfrontiers/snapsell-ai/pull/5
  - รัน flow อัปโหลดเต็มรูปแบบบนเครื่องตัวเอง: checkout branch `backend-reliability`
    แล้ว `python3 demo/server.py` (โค้ดที่แก้ F-2/F-1 แล้ว) — ไม่ต้อง merge ก็รันได้

## ขั้นตอนที่ต้องทำด้วยมือ (ตามลำดับ)

1. **บันทึกวิดีโอเดโม** ตาม demo-script.md (เครื่องของคน, ใช้โค้ด branch `backend-reliability`,
   รูป Lactasoy ที่มีใน repo อยู่แล้ว) — ถ้ารันแล้วได้ข้อความ fallback ให้หยุด อย่าเอามาใช้
   ให้รันใหม่หรือรายงาน ไม่ใช่แต่งผล
2. **อัปโหลดวิดีโอ** แล้วเอาลิงก์มาใส่ในฟอร์ม (โฮสต์ตามที่พอร์ทัลรับ — UNVERIFIED ดูข้างบน)
3. **กรอกฟอร์ม Cerebral Valley** แปะข้อความจาก project-description.md ตามช่องที่มี
   ทีม: ปัจจุบันคือ solo (Indie) — ถ้าจะเพิ่มเพื่อนร่วมทีม ต้องยืนยันก่อนกดส่ง
4. **กดส่ง + เก็บ confirmation** (แคปหน้าจอ/บันทึกข้อความยืนยัน)
5. ถ้าจะ merge/deploy PR #4/#5 — นั่นเป็นคำสั่งแยกต่างหาก ไม่ใช่ส่วนของการส่งครั้งนี้

## Blocker ที่เหลือจริงๆ (ไม่มีอย่างอื่น)

1. วิดีโอเดโมยังไม่ได้บันทึก (manual step เดียวที่ขวางการส่ง)
2. ฟิลด์ฟอร์มจริงยังไม่เห็น (UNVERIFIED — รู้ตอนเปิดฟอร์ม)
3. PR #4/#5 ยังไม่ merge/deploy (โดยตั้งใจตามคำสั่ง — ไม่ใช่ blocker ของการส่ง
   เพราะส่งได้ด้วย main + draft PR + วิดีโอ แต่ต้องอธิบายสถานะตามจริงในฟอร์ม)
