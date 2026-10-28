มีนา: Gallery Edit Diff — 2 จุดที่ GPT อนุมัติ (รอตรวจ ยังไม่ merge)

Branch: `gallery-attribution` (สร้างจาก main `1e44b1df`)
Commit: `fe8857a2f193` (1 commit บน branch)
Compare: main...gallery-attribution = ahead 1, behind 0
ไฟล์ที่เปลี่ยน: `demo/index.html` เพียงไฟล์เดียว (+6/-3)
Main ไม่ถูกแตะ (head ยัง `1e44b1df6dbb`) — ไม่ Deploy
ไม่มี PR สำหรับ branch นี้ในรอบนี้ (เปิด PR ได้เมื่อทีมสั่ง merge)

## จุดที่ 1 — Lactasoy d3 เพิ่มคำอ้างอิง (3 ตำแหน่ง)

TH (static card + I18N th dict — ข้อความเดียวกัน 2 ที่):
- เดิม: `…ปริมาตรสุทธิ 500 มล. ให้โปรตีนและกรดอะมิโนจำเป็น…`
- ใหม่: `…ปริมาตรสุทธิ 500 มล. บนกล่องระบุว่าให้โปรตีนและกรดอะมิโนจำเป็น…`
- ตำแหน่งบน branch (ไฟล์ `demo/index.html`):
  - บรรทัด 112: `<div class="detail" data-i18n="d3">…</div>`
    (static card)
  - บรรทัด 159: `d3: '…'` (I18N th dict)

EN (I18N en dict — 1 ตำแหน่ง):
- เดิม: `…Net volume 500 ml. Provides protein and essential amino acids…`
- ใหม่: `…Net volume 500 ml. The carton states: provides protein and essential amino acids…`
- ตำแหน่งบน branch: บรรทัด 192: `d3: '…'` (I18N en dict)

ข้อความอื่นของ d3 (สูตร/รส/ถิ่นกำเนิด/ปริมาตร/พลังงาน/
อิ่มท้อง/เต็มกล่อง) ไม่ถูกแตะ — เปลี่ยนแค่การแทรกคำอ้างอิง
หน้า "ให้โปรตีน / Provides protein" ตามที่ audit เสนอ

## จุดที่ 2 — Note ใต้หัวข้อ Gallery (3 ตำแหน่ง)

- Element ใหม่หลัง `<h2 data-i18n="galleryTitle">` (บรรทัด 83):
  - บรรทัด 84 บน branch:
    `<div class="note" data-i18n="galleryNote" style="color:#66707e;font-size:13px;margin:8px 0 4px">การ์ดตัวอย่างเป็นผลลัพธ์จากระบบรุ่นก่อน guardrail ข้อความอ้างอิงจากฉลากที่เห็นในรูปต้นฉบับ</div>`
  - style inline (ตัวเทา ตัวเล็ก) เพื่อให้แสดงเป็น note โดยไม่ต้อง
    แตะ CSS (นอกขอบเขต)
- I18N key ใหม่ 2 ที่:
  - บรรทัด 151 (th dict): `galleryNote: 'การ์ดตัวอย่างเป็นผลลัพธ์จากระบบรุ่นก่อน guardrail ข้อความอ้างอิงจากฉลากที่เห็นในรูปต้นฉบับ',`
  - บรรทัด 184 (en dict): `galleryNote: 'Sample cards are outputs from the pre-guardrail system; claims quote the labels visible in the original photos.',`
- setLang เดิมเติม `data-i18n` element จาก dict อยู่แล้ว
  (TH static text กับ th dict ตรงกัน EN สลับตามภาษา) —
  ไม่ได้แก้ logic ภาษา

## Diff เต็ม (main → gallery-attribution)

```
83a84
>     <div class="note" data-i18n="galleryNote" style="color:#66707e;font-size:13px;margin:8px 0 4px">การ์ดตัวอย่างเป็นผลลัพธ์จากระบบรุ่นก่อน guardrail ข้อความอ้างอิงจากฉลากที่เห็นในรูปต้นฉบับ</div>
111c112
<     <div class="detail" data-i18n="d3">…ปริมาตรสุทธิ 500 มล. ให้โปรตีนและกรดอะมิโนจำเป็น…</div>
---
>     <div class="detail" data-i18n="d3">…ปริมาตรสุทธิ 500 มล. บนกล่องระบุว่าให้โปรตีนและกรดอะมิโนจำเป็น…</div>
149a151
> galleryNote: 'การ์ดตัวอย่างเป็นผลลัพธ์จากระบบรุ่นก่อน guardrail ข้อความอ้างอิงจากฉลากที่เห็นในรูปต้นฉบับ',
157c159
<     d3: '…ปริมาตรสุทธิ 500 มล. ให้โปรตีนและกรดอะมิโนจำเป็น…',
---
>     d3: '…ปริมาตรสุทธิ 500 มล. บนกล่องระบุว่าให้โปรตีนและกรดอะมิโนจำเป็น…',
181a184
> galleryNote: 'Sample cards are outputs from the pre-guardrail system; claims quote the labels visible in the original photos.',
189c192
<     d3: '…Net volume 500 ml. Provides protein and essential amino acids…',
---
>     d3: '…Net volume 500 ml. The carton states: provides protein and essential amino acids…',
```

(ย่อด้วย … ตรงส่วนที่ไม่เปลี่ยน — diff จริงที่ตรวจมีแค่
บรรทัดข้างบน 9 marker lines ไม่มีการเปลี่ยนบรรทัดอื่น)

## ตรวจว่าไม่มีอะไรนอกขอบเขต

- Diff ทั้งไฟล์มีแค่บรรทัดของ 2 จุดข้างบน (note div 1 บรรทัด
  + galleryNote dict 2 บรรทัด + d3 3 ตำแหน่ง)
- การ์ดอื่น (t1/d1, t2/d2, t4/d4, t5/d5) และ title t3
  ไม่เปลี่ยนแม้แต่ตัวอักษรเดียว (ยืนยันจาก diff)
- ไม่แตะไฟล์อื่น: ไม่มี server.py, test, CSS, JS logic,
  ไม่มี snapsell/ stub, ไม่มี config
- ไม่ Deploy: branch นี้ยังไม่ขึ้น live ที่ใด — Pages ที่เห็น
  ยังเป็นเวอร์ชันเก่าจนกว่าจะมีคำสั่ง deploy แยก
- Main head ยัง `1e44b1df6dbb` (ตรวจหลัง push แล้ว)

## รอ GPT/ทีม

- ถ้าตรวจผ่าน: เปิด PR จาก `gallery-attribution` → main
  แล้ว merge ตามกระบวนการ (หรือสั่งให้มีนาเปิด PR ให้)
- ถ้าติง: แก้ต่อบน branch เดิม ไม่แตะ main
