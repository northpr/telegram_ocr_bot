import numpy as np
import os
import re
import random
from datetime import datetime

def remove_words(ocr_result: str)-> str:
    remove_words = ["จ่ายบิลสําเร็จ", "วีเพย์", "VPAY","เลขที่รายการ", "ผู้รับเงินสามารถสแกนคิวอาร์โค้ด"
                    "ธ.กสิกรไทย", "ธ.กสิกรไทย", "จํานวน:", "จำนวน:", "จำนวนเงิน", "ค่าธรรมเนียม:",
                    "สแกนตรวจสอบสลิป", "จาก", "ไปยัง", "จํานวนเงิน", "จ่ายบิลสำเร็จ", "๒ ", "๒"
                    "รหัสอ้างอิง", "กรุงไทย", "วันเดือนปีที่ทํารายการ", "ค่าธรรมเนียม", "วันเดือนปีที่ทำรายการ"]
    pattern = "|".join(remove_words)
    clean_text = re.sub(pattern, "", ocr_result)
    return clean_text

def regex_check(ocr_results: str)->dict:
    """For checking `ref_id` and `money_amt` from OCR results by using regular expression

    Args:
        ocr_results (str): Results from OCR which now using Pytesseract

    Returns:
        list: Will return to dict after regex
    """
    ref_id, money_amt, full_name = [], [], []
    mistakes = 0

    # Checking ref_id
    ref_id = [int(x) for x in re.findall(r'20\d{16}', ocr_results)]
    if len(ref_id) == 0: # if nothing match
        ref_id.append("Please manually check ref_id again")
        mistakes += 1
    # Checking the money amout
    money_amt = re.findall(r'\b\d{1,3}(?:,\d{3})*\.\d{2}\b', ocr_results)
    money_amt = [float(f.replace(",", "")) for f in money_amt]
    if len(money_amt) == 0: # if nothing match
        money_amt.append("Please manually check money_amt again")
        mistakes += 1

    # Checking the full_name case
    pattern_with_space = r'(นาย ?[\u0E00-\u0E7F ]+|นางสาว ?[\u0E00-\u0E7F ]+|น\.ส\. ?[\u0E00-\u0E7F ]+|นาง ?[\u0E00-\u0E7F ]+)'
    full_name = re.findall(pattern_with_space, ocr_results)
    if not full_name: # if full name don't have any result
        pattern_without_space = r'(นาย[\u0E00-\u0E7F]+|นางสาว[\u0E00-\u0E7F]+|น\.ส\.[\u0E00-\u0E7F]+|นาง[\u0E00-\u0E7F]+)'
        full_name = re.findall(pattern_without_space, ocr_results)

    if len(full_name) == 0: # if nothing match
        full_name.append("Please manually check full_name again")
        mistakes += 1

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"ref_id": ref_id[0],
            "money_amt": money_amt[0],
            "full_name": full_name[0],
            "mistakes": mistakes,
            "current_time": current_time}