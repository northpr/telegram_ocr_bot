from receipt_helper import VPayExtractor
ocr_results = "จ่ายบิล\nสําเร็จ\nรหัสอ้างอิง\n20230210616461\n01\nKrungthai\nกรุงไทย\n() นางนงค์นุช มีกลิ่นหอม\nกรุงไทย\nXXX-X-XX651-6\nวีเพย์\n(010556213625103)\nวันเดือนปีที่ 2023021017\nรายการ\n05204474\nวันเดือนปีที่ทำ 2023021017\nรายการ\n05204642\nจํานวนเงิน\nค่าธรรมเนียม\nวันที่ทํารายการ\n300.00 บาท\n0.00 บาท\n10 ก.พ.\n2566- 17:05"
clean_text = VPayExtractor.remove_words(ocr_results)
print(clean_text.split("\n"))