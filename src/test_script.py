from receipt_processor import VPayExtractor
import re

ocr_results = "Krungthai\nกรุงไทย\n จ\nรหัสอ้างอิง\n20230215803654\n21\nนายทาน เกิดชะนะ\nกรุงไทย\nXXX-X-XX171-5\n\n(010556213625103)\n\n202302152129006808\n\n202302152129009288\nA\n300.00 บาท\n\n\n0.00 บาท\nวันที่ทำรายการ 15 ก.พ. 2556 -\n21:29"
clean_text = VPayExtractor.remove_words(ocr_results)
# print(clean_text)
clean_text = VPayExtractor.extract_trans_id(clean_text,"ktb")
print(clean_text)