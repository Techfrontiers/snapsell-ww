มีนา: Gallery Edit Diff รอบ 2 — ปรับ Lactasoy d3 ให้ชัดว่าทั้ง 3 ข้อความมาจากฉลาก (รอตรวจ ยังไม่เปิด PR)

Branch เดิม: `gallery-attribution` (commit ใหม่ `bbef11a2f193`,
รวม 2 commits บน branch)
Compare: main...gallery-attribution = ahead 2, behind 0
ไฟล์ที่เปลี่ยน: `demo/index.html` เพียงไฟล์เดียว (+6/-3 เท่าเดิม
เพราะรอบนี้แก้เนื้อความในบรรทัดเดิม ไม่เพิ่ม/ลบบรรทัด)
Main ไม่ถูกแตะ (head ยัง `1e44b1df6dbb`) — ไม่เปิด PR,
ไม่ Deploy, ไม่แก้การ์ดอื่นหรือไฟล์อื่น

## ปัญหาที่ GPT ติงใน diff รอบแรก

คำอ้างอิง "บนกล่องระบุว่า / The carton states:" ในรอบแรก
ครอบคลุมประโยคโปรตีนชัด แต่ประโยคพลังงานกับความอิ่ม
ตามมาเป็นวลีลอย ๆ อ่านแล้วเหมือนคำบรรยายปกติ ไม่ชัดว่า
เป็นข้อความจากฉลากด้วย

## วิธีแก้รอบนี้ (เปลี่ยนแค่ d3 3 ตำแหน่ง)

TH — รวม 3 ข้อความเป็น ว่า-clause เดียว (ธรรมชาติ + ตรงคำบนกล่อง):
- เดิม (รอบแรก): `…บนกล่องระบุว่าให้โปรตีนและกรดอะมิโนจำเป็น
  เหมาะสำหรับผู้ที่ต้องการพลังงานในการดำเนินชีวิตประจำวัน
  ช่วยให้อิ่มท้องในชั่วโมงเร่งด่วน…`
- ใหม่: `…บนกล่องระบุว่าให้โปรตีนและกรดอะมิโนจำเป็น
  เหมาะสำหรับผู้ที่ต้องการพลังงานในการดำเนินชีวิตประจำวัน
  และให้ความอิ่มท้องในชั่วโมงเร่งด่วน…`
- ที่เปลี่ยนจริงมีแค่ `ช่วยให้อิ่มท้อง` → `และให้ความอิ่มท้อง`
  (คำว่า "และ" ดึงความอิ่มเข้า ว่า-clause เดียวกัน;
  "ให้ความอิ่มท้อง" คือคำเดียวกับที่พิมพ์บนกล่อง)
- ผล: โปรตีน/กรดอะมิโน (1) + พลังงาน (2) + ความอิ่ม (3)
  อยู่ใต้ "บนกล่องระบุว่า" ทั้งหมดในประโยคเดียว
- ตำแหน่ง: static card บรรทัด 112, I18N th dict บรรทัด 159
  (ข้อความเดียวกัน 2 ที่ เปลี่ยนครบทั้ง 2 ที่)

EN — เปลี่ยนเป็น "The carton says it…" + กริยาขนานกัน 3 ตัว:
- เดิม (รอบแรก): `…The carton states: provides protein and
  essential amino acids, good for people who need energy
  through the day and something filling in a rush…`
- ใหม่: `…The carton says it provides protein and essential
  amino acids, suits people who need energy in everyday living,
  and fills up an empty stomach in a hurry…`
- ผล: provides (โปรตีน) / suits…energy (พลังงาน) /
  fills up… (ความอิ่ม) เป็นกริยาขนานกันภายใต้ "The carton
  says it" ตัวเดียว — ชัดว่าทั้ง 3 มาจากกล่อง
- วลีใกล้เคียงคำบนกล่องภาษาอังกฤษ ("suitable for someone
  needs energy in everyday living", "Fills up your empty
  stomach when you are in a hurry") ปรับไวยากรณ์ให้อ่าน
  ธรรมชาติ ไม่ได้เพิ่มการรับรองเกินกว่าข้อความบนกล่อง
- ตำแหน่ง: I18N en dict บรรทัด 192

ส่วนที่เหลือของ d3 ไม่เปลี่ยน: สูตรต้นตำรับ, รสชาติอร่อย
ดื่มง่าย (puffery), ผลิตภัณฑ์ของประเทศไทย, ปริมาตรสุทธิ
500 มล., และสโลแกน "อิ่มอร่อยเต็มกล่องสำหรับคุณและทุกคน
ในครอบครัว / a full box for you and the whole family"
(สโลแกนนี้ก็อยู่บนกล่องเช่นกัน แต่ GPT ระบุ 3 ข้อความหลัก
ข้างบน — สโลแกนจึงคงไว้ตามเดิม ไม่ได้เอาเข้า ว่า-clause
และไม่ได้ลบออก)

## Diff รอบ 2 (branch เก่า → branch ใหม่ — มีแค่ d3)

```
112c112 (static d3 TH)
< …ช่วยให้อิ่มท้องในชั่วโมงเร่งด่วน…
---
> …และให้ความอิ่มท้องในชั่วโมงเร่งด่วน…
159c159 (th dict d3 — เปลี่ยนเดียวกัน)
192c192 (en dict d3)
< …The carton states: provides protein and essential amino acids, good for people who need energy through the day and something filling in a rush…
---
> …The carton says it provides protein and essential amino acids, suits people who need energy in everyday living, and fills up an empty stomach in a hurry…
```

## Diff รวม main → branch (หลังรอบ 2)

เหมือนรอบแรกทุกประการยกเว้นเนื้อความ d3 3 บรรทัดข้างบน:
note div บรรทัด 84, galleryNote th บรรทัด 151 / en บรรทัด 184,
d3 static บรรทัด 112 / th บรรทัด 159 / en บรรทัด 192 —
การ์ดอื่น (t1/d1, t2/d2, t4/d4, t5/d5) และ title t3 ไม่เปลี่ยน
ไฟล์อื่นไม่มี — ตรวจจาก compare แล้ว: demo/index.html
ไฟล์เดียว +6/-3

## รอ GPT ตรวจ

- ถ้าผ่าน: เปิด PR จาก `gallery-attribution` → main แล้ว
  merge ตามกระบวนการ (หรือสั่งให้มีนาเปิด PR ให้)
- ถ้าติงอีก: แก้ต่อบน branch เดิม ไม่แตะ main ไม่ Deploy
