import io
import os
import re
import random
from datetime import datetime
from google.cloud import vision

def perform_ocr(client, image_file):
    with io.BytesIO(image_file) as image_bin:
        content = image_bin.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def remove_words(ocr_result: str)-> str:
    remove_words = ["จ่ายบิลสําเร็จ", "วีเพย์", "VPAY","เลขที่รายการ", "ผู้รับเงินสามารถสแกนคิวอาร์โค้ด",
                    "จํานวน:", "จำนวน:", "จำนวนเงิน", "ค่าธรรมเนียม:",
                    "สแกนตรวจสอบสลิป", "จาก", "ไปยัง", "จํานวนเงิน", "จ่ายบิลสำเร็จ", "๒ ", "๒"
                    "รหัสอ้างอิง", "วันเดือนปีที่ทํารายการ", "ค่าธรรมเนียม", "วันเดือนปีที่ทำรายการ"]
    pattern = "|".join(remove_words)
    clean_text = re.sub(pattern, "", ocr_result)
    return clean_text

def extract_ref_id(ocr_results: str):
    # Checking ref_id
    ref_id = [int(x) for x in re.findall(r'20\d{16}', ocr_results)]
    if len(ref_id) == 0:
        # Try merging lines if normal regex search is not work
        lines = ocr_results.split("\n")
        for i, line in enumerate(lines):
            next_line = lines[i+1]
            merged_line = line+next_line
            ref_id = [int(x) for x in re.findall(r'20\d{16}', merged_line)]
            if len(ref_id) > 0:
                break
    return ref_id[0] if len(ref_id) > 0 else False

def extract_money(ocr_results: str):
    money_amt = re.findall(r'\b\d{1,3}(?:,\d{3})*\.\d{2}\b', ocr_results)
    money_amt = [float(f.replace(",", "")) for f in money_amt]
    return money_amt[0] if len(money_amt) > 0 else False

def extract_full_name(ocr_results: str):
    pattern = r'(นาย ?(?:[\u0E00-\u0E7F ]+)|นางสาว ?(?:[\u0E00-\u0E7F ]+)|น\.ส\. ?(?:[\u0E00-\u0E7F ]+)|นาง ?(?:[\u0E00-\u0E7F ]+))'
    full_name = re.findall(pattern, ocr_results)

    return full_name[0] if len(full_name) > 0 else False

def extract_acc_num(ocr_results: str):
    pattern_acc_number = r'(?:[Xx]{3}|(?:0202|0203))[-\w\d]+'
    account_numbers = re.findall(pattern_acc_number, ocr_results)
    return account_numbers[0] if len(account_numbers) > 0 else False

def extract_bank_name(ocr_results: str) -> str:
    bank_keywords = {
        "kbank": r"(กสิกรไทย|ธ\.กสิกรไทย)",
        "scb": r"(SCB|scb\.)",
        "gsb": r"(gsb|GSB)",
        "ktb": r"(Krungthai|กรุงไทย)"
    }

    for bank_name, pattern in bank_keywords.items():
        if re.search(pattern, ocr_results):
            return bank_name

    return "unknown"


def format_ref_id_time(ref_id: int) -> str:
    try:
        ref_id_str = str(ref_id)
        year = ref_id_str[0:4]
        month = ref_id_str[4:6]
        day = ref_id_str[6:8]
        hour = ref_id_str[8:10]
        minute = ref_id_str[10:12]

        formatted_date_time = f"{hour}:{minute} {day}/{month}/{year}"
        return formatted_date_time
    except:
        return "โปรดตรวจสอบด้วยตัวเองอีกครั้ง"

def regex_check(ocr_results: str)->dict:
    ref_id = extract_ref_id(ocr_results)
    money_amt = extract_money(ocr_results)
    full_name = extract_full_name(ocr_results)
    acc_number = extract_acc_num(ocr_results)
    bank_name = extract_bank_name(ocr_results)

    mistakes = sum(1 for x in [ref_id, money_amt, full_name, acc_number] if x is False)
    current_time = datetime.now().strftime("%Y%m%d%H%M")

    return {
    "ref_id": ref_id if ref_id is not False else "โปรดตรวจสอบด้วยตัวเองอีกครั้ง",
    "money_amt":  money_amt if money_amt is not False else "โปรดตรวจสอบด้วยตัวเองอีกครั้ง",
    "full_name": full_name if full_name is not False else "โปรดตรวจสอบด้วยตัวเองอีกครั้ง",
    "acc_number": acc_number if acc_number is not False else "โปรดตรวจสอบด้วยตัวเองอีกครั้ง",
    "bank_name": bank_name,
    "mistakes": mistakes,
    "current_time": current_time
        }

def extract_message_info(message):
    message_info = {
        "chat_id" : message.chat.id,
        "chat_title": message.chat.title,
        "user_id": message.from_user.id,
        "user_username": message.from_user.username,
        "user_firstname": message.from_user.first_name
    }
    return message_info

def to_unix_timestamp(timestamp_str: str) -> int:
    """
    This function takes the input string, converts it to a datetime object using 
    the specified format, and then converts the datetime object to a Unix timestamp.
    You can use this Unix timestamp in Grafana for proper time representation.

    Args:
        timestamp_str (str): timestamp like 202304272135, 202302210940572991

    Returns:
        int: Timestamp in Unix
    """
    if not timestamp_str:
        return -1
    
    try: 
        timestamp_str = timestamp_str[:12]
        timestamp_dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M")
        unix_timestamp = int(timestamp_dt.timestamp())
        return unix_timestamp
    except ValueError:
        return -1

### JUST FOR LOCAL USE NOT IMPORTANT ###

def find_img(rand_dir: str, spec_img_path=None)-> str:
    """
    Getting an image randomly or by specific path.

    Args:
        directory (str): directory
        specific_image_path (_type_, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    if spec_img_path:
        return spec_img_path
    # Search for all .jpg files in the specified directory and its subdirectories
    image_files = []
    for root, dirs, files in os.walk(rand_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                image_files.append(os.path.join(root, file))

    # If there are no image files, return None
    if not image_files:
        return None

    # Pick a random image file from the list of image files found, and return its path
    random_image_path = random.choice(image_files)
    return random_image_path

