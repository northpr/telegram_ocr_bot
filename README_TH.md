เลือกภาษาที่คุณต้องการ:

[🇬🇧 English](README_EN.md) [🇹🇭 ภาษาไทย](README_TH.md)

# 🤖 Telegram OCRBot สำหรับใบเสร็จธนาคาร
ตัวคลังข้อมูลนี้ประกอบด้วยรหัสต้นฉบับสำหรับ Telegram OCRBot, หุ่นยนต์ที่สามารถสกัดข้อความจากรูปภาพใบเสร็จธนาคารที่แชร์บน Telegram หุ่นยนต์ถูกออกแบบเพื่อประมวลผลใบเสร็จจากธนาคารหลายแห่ง โดยเฉพาะในภาษาไทย และตอบกลับลูกค้าในแอป Telegram

เป้าหมายหลักของโครงการนี้คือการให้บริการ OCR ที่รวดเร็ว แม่นยำ และประหยัดค่าใช้จ่าย ซึ่งสามารถจัดการกับความไม่สม่ำเสมอของขนาดภาพและประเภทของใบเสร็จที่แตกต่างกัน

## วิธีการ
nbs = notebooks
src = รหัสต้นฉบับ
app = แอปสำหรับ Dockerize

# 👓 ภาพรวม
โครงการได้ผ่านการปรับปรุงหลายรอบเพื่อให้ได้ผลลัพธ์ที่ดีที่สุด วิธีที่ใช้ในปัจจุบันคือการใช้ Google Vision สำหรับ OCR ซึ่งสนับสนุนภาษาไทย และใช้ Regular Expression ในการสกัดข้อมูลที่เกี่ยวข้องจากผล OCR วิธีนี้ประหยัดค่าใช้จ่าย รวดเร็ว และมีความแม่นยำที่พอใช้

# 🛣️คุณสมบัติ
- สนับสนุนรูปแบบภาพหลายรูปแบบ (JPEG, PNG, เป็นต้น)
- ประมวลผลใบเสร็จจากธนาคารหลายแห่ง (kbank, scb, ktb)
- จัดการข้อความที่มีการวางแนวและขนาดตัวอักษรที่แตกต่างกัน
- ให้ผลลัพธ์ OCR ที่แม่นยำโดยใช้ Google Vision
- ใช้ Regular Expression ในการสกัดข้อมูลที่เกี่ยวข้อง
- วิธีการที่รวดเร็วและประหยัดค่าใช้จ่าย

# 📕 ภาษาและเครื่องมือ
- Python
- OpenCV
- Tesseract OCR
- Pytesseract
- HuggingFace
- Google Vision API
- Regular Expressions
- Docker

# 🔄แนวทาง
## วิธีที่ 1: OpenCV + Pytesseract
ในวิธีการนี้ OpenCV ถูกใช้ในการค้นหาพิกัดของพื้นที่ข้อความภายในภาพ หลังจากนั้นคัดลอกรูปภาพและใช้ Pytesseract ในการประมวลผล OCR บนส่วนที่คัดลอก โดยระบุภาษาและพื้นที่ในการคัดลอกและ OCR กระบวนการนี้ให้ความแม่นยำที่ดี

## วิธีที่ 2: โดนัทโดย HuggingFace
Donut เป็นโมเดลการเรียนรู้เชิงลึกที่พัฒนาโดย HuggingFace วิธีการนี้มุ่งเน้นใช้ประโยชน์จากการเรียนรู้เชิงลึกเพื่อเพิ่มประสิทธิภาพในการทำ OCR โมเดล Donut ได้รับการทดสอบบนชุดข้อมูล SROIE และให้ผลลัพธ์ที่ยอดเยี่ยม อย่างไรก็ตาม การใช้งานโมเดลนี้ต้องใช้ความรู้เกี่ยวกับ PyTorch และ HuggingFace และโมเดลไม่สนับสนุนภาษาไทย

## วิธีที่ 3: LayoutLM โดย HuggingFace
LayoutLM เป็นอีกหนึ่งโมเดลการเรียนรู้เชิงลึกที่พัฒนาโดย HuggingFace วิธีการนี้มุ่งหาความแม่นยำสูงโดยการฝึกฝนโมเดลด้วยชุดข้อมูลภาพที่มีป้ายชื่อขนาดใหญ่ อย่างไรก็ตาม โมเดลนี้มีความซับซ้อนในการใช้งานและต้องใช้เวลาในการฝึกฝนมาก นอกจากนี้ยังมีความท้าทายในด้านการปรับปรุงต้นทุนและการใช้งาน

## วิธีที่ 4: Google Vision + Regular Expression (ปัจจุบัน)
วิธีการปัจจุบันคือการใช้ Google Vision API ในการประมวลผล OCR บนภาพใบเสร็จทั้งหมด โดย API นี้สนับสนุนภาษาไทยและให้ความแม่นยำที่ดี หลังจาก OCR จากนั้นใช้ Regular Expression ในการสกัดข้อมูลที่เกี่ยวข้องจากผล OCR วิธีนี้ง่าย รวดเร็ว และประหยัดค่าใช้จ่าย

