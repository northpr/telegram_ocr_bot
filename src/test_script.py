from receipt_processor import VPayExtractor
import re

ocr_results = "Krungthai\nกรุงไทย\n\nรหัสอ้างอิง\n2023022487937713\nน.ส.ชลาลัย มณฑาสวิน\nกรุงไทย\nXXX-X-XX320-3\n\n(010556213625103)\nวันเดือนปีที่ทํา\nรายการ\nวันเดือนปีที่ทํา\nรายการ\n\n\nวันที่ทำรายการ\n2023022423194\n99720\n2023022423194\n95592\n1,000.00 บาท\n0.00 บาท\n24 ก.พ. 2556 -\n23:20"
clean_text = VPayExtractor.remove_words(ocr_results)
clean_text_list = clean_text.split("\n")
numbers = [re.findall(r'20\d{8,}', s) for s in clean_text_list]
print(numbers)