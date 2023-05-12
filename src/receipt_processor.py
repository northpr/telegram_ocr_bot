import io
import re
from datetime import datetime
from typing import List, Dict, Tuple, Union
from google.cloud import vision

class OCRVision():
    @staticmethod
    def perform_ocr(client, image_file) -> str:
        """
        Perform OCR on the given image file

        Args:
            client (_type_): _description_
            image_file (_type_): _description_

        Returns:
            str: Text for OCR the image
        """
        with io.BytesIO(image_file) as image_bin:
            content = image_bin.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts
    
class VPayExtractor():
    @staticmethod
    def remove_words(ocr_result: str)-> str:
        """
        Remove the words to make the word extraction easier

        Args:
            ocr_result (str): Text from perform_ocr.

        Returns:
            str: Text after removing unwanted words
        """
        remove_words = ["จ่ายบิลสําเร็จ", "วีเพย์", "VPAY","เลขที่รายการ", "ผู้รับเงินสามารถสแกนคิวอาร์โค้ด",
                        "จํานวน:", "จำนวน:", "จำนวนเงิน", "ค่าธรรมเนียม:",
                        "สแกนตรวจสอบสลิป", "จาก", "ไปยัง", "จํานวนเงิน", "จ่ายบิลสำเร็จ", "๒ ", "๒"
                        "รหัสอ้างอิง", "วันเดือนปีที่ทํารายการ", "ค่าธรรมเนียม", "วันเดือนปีที่ทำรายการ"]
        pattern = "|".join(remove_words)
        clean_text = re.sub(pattern, "", ocr_result)
        return clean_text
    
    @staticmethod
    def extract_ref_id(ocr_results: str) -> Union[str ,bool]:
        # Checking ref_id
        ref_id = [int(x) for x in re.findall(r'20\d{16}', ocr_results)]
        if len(ref_id) == 0:
            try:
                # Try merging lines if normal regex search is not work
                lines = ocr_results.split("\n")
                for i, line in enumerate(lines[0:-1]):
                    next_line = lines[i+1]
                    merged_line = line+next_line
                    ref_id = [int(x) for x in re.findall(r'20\d{10,16}', merged_line)]
                    if len(ref_id) > 0:
                        break
            except IndexError:
                pass
        return ref_id[0] if len(ref_id) > 0 else False
    
    # @staticmethod
    # def test_extract_ref_id(ocr_results: str):
    #     ref_id = [int(x) for x in re.findall(r'20\d{16}', ocr_results)]
    #     if len(ref_id) == 0:
    #         try:
    #             lines = ocr_results.split("\n")
    #             for i, line in enumerate(lines[0:1]):

    
    @staticmethod
    def extract_money(ocr_results: str) -> Union[str ,bool]:
        money_amt = re.findall(r'\b\d{1,3}(?:,\d{3})*\.\d{2}\b', ocr_results)
        money_amt = [float(f.replace(",", "")) for f in money_amt]
        return money_amt[0] if len(money_amt) > 0 else False
    
    @staticmethod
    def extract_full_name(ocr_results: str) -> Union[str ,bool]:
        pattern = r'(นาย ?(?:[\u0E00-\u0E7F ]+)|นางสาว ?(?:[\u0E00-\u0E7F ]+)|น\.ส\. ?(?:[\u0E00-\u0E7F ]+)|นาง ?(?:[\u0E00-\u0E7F ]+))'
        full_name = re.findall(pattern, ocr_results)
        return full_name[0] if len(full_name) > 0 else False
    
    @staticmethod
    def extract_acc_num(ocr_results: str) -> Union[str ,bool]:
        pattern_acc_number = r'(?:[Xx]{3}|(?:0202|0203))[-\w\d]+'
        account_numbers = re.findall(pattern_acc_number, ocr_results)
        return account_numbers[0] if len(account_numbers) > 0 else False
    
    @staticmethod
    def extract_bank_name(ocr_results: str) -> str:
        bank_keywords = {
            "kbank": r"(กสิกรไทย|ธ\.กสิกรไทย)",
            "scb": r"(SCB|scb\.)",
            "gsb": r"(gsb|GSB|ธนาคารออมสิน)",
            "ktb": r"(Krungthai|กรุงไทย)"
        }
        for bank_name, pattern in bank_keywords.items():
            if re.search(pattern, ocr_results):
                return bank_name
        return "unknown"
    
    @staticmethod
    def extract_trans_id(ocr_results: str, bank_name: str) -> str:
        trans_id = None
        if bank_name == "ktb":
            matches = re.findall(r'\b\d{16}\b', ocr_results)
        elif bank_name == "kbank":
            matches = re.findall(r'\b[A-Za-z0-9]{20}\b', ocr_results)
        else:
            # The transaction ID should have a minimum length of 20 characters
            matches = re.findall(r'\b[A-Za-z0-9]{20,}\b', ocr_results)
        
        if not matches:
            lines = ocr_results.split("\n")
            try:
                for i, line in enumerate(lines):
                    next_line = lines[i+1]
                    merged_line = line+next_line
                    if bank_name == "ktb":
                        matches = re.findall(r'\b\d{16}\b', merged_line)
                    elif bank_name == "kbank":
                        matches = re.findall(r'\b[A-Za-z0-9]{20}\b', merged_line)
                    else:
                        matches = re.findall(r'\b[A-Za-z0-9]{21,}\b', merged_line)
            except IndexError:
                return False
        trans_id = matches[0] if matches else False

        return trans_id

    @staticmethod
    def regex_check(ocr_results: str)-> Dict[str, Union[str, int, float, bool]]:
        ref_id = VPayExtractor.extract_ref_id(ocr_results)
        money_amt = VPayExtractor.extract_money(ocr_results)
        full_name = VPayExtractor.extract_full_name(ocr_results)
        acc_number = VPayExtractor.extract_acc_num(ocr_results)
        bank_name = VPayExtractor.extract_bank_name(ocr_results)
        trans_id = VPayExtractor.extract_trans_id(ocr_results, bank_name)
        mistakes = sum(1 for x in [ref_id, money_amt, full_name, acc_number] if x is False)
        current_time = datetime.now().strftime("%Y%m%d%H%M")
        return {
        "ref_id": ref_id if ref_id is not False else "โปรดตรวจสอบอีกครั้ง",
        "money_amt":  '{:,.2f}'.format(money_amt) if money_amt is not False else "โปรดตรวจสอบอีกครั้ง",
        "full_name": full_name if full_name is not False else "โปรดตรวจสอบอีกครั้ง",
        "acc_number": acc_number if acc_number is not False else "โปรดตรวจสอบอีกครั้ง",
        "bank_name": bank_name,
        "trans_id": trans_id if trans_id is not False else "โปรดตรวจสอบอีกครั้ง",
        "mistakes": mistakes,
        "current_time": current_time
            }

class TeleHelper():
    @staticmethod
    def extract_message_info(message):
        message_info = {
            "chat_id" : message.chat.id,
            "chat_title": message.chat.title,
            "user_id": message.from_user.id,
            "user_username": message.from_user.username,
            "user_firstname": message.from_user.first_name
        }
        return message_info