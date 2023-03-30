import numpy as np
import cv2
import os
import re
import random

def img_preprocess(img:np): 
    """Preprocess image to make letters clearer while removing background

    Args:
        img (np): Image file

    Returns:
        img_bin (np): Binary image with clearer letters and removed background
    """
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to obtain a binary mask of the black letters
    _, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the binary mask to obtain a mask of the background
    img_bg = cv2.bitwise_not(img_bin)

    # Apply color thresholding to the image to remove the background
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([179, 255, 150])
    img_mask = cv2.inRange(img_hsv, lower, upper)

    # Apply the background mask to the color thresholded image
    img_masked = cv2.bitwise_and(img_mask, img_mask, mask=img_bg)

    # Invert the binary mask again to obtain the final binary image
    img_bin_final = cv2.bitwise_not(img_masked)

    # Apply erosion to remove small details and noise from the background
    kernel = np.ones((2, 2), np.uint8)
    img_erode = cv2.erode(img_bin_final, kernel, iterations=1)

    return img_erode

def random_image(directory, subdirectory_name=None):
    # If a subdirectory name is specified, get the path to that subdirectory
    if subdirectory_name:
        subdirectory_path = os.path.join(directory, subdirectory_name)

        # If the specified subdirectory doesn't exist, return None
        if not os.path.isdir(subdirectory_path):
            return None
    else:
        subdirectory_path = directory

    # Get a list of all image files in the specified subdirectory and its subdirectories
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    image_files = []
    for root, dirs, files in os.walk(subdirectory_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(root, file))

    # If there are no image files, return None
    if not image_files:
        return None

    # Pick a random image file from the specified subdirectory and its subdirectories, and return its path
    random_image_path = random.choice(image_files)
    return random_image_path

def remove_words(ocr_result: str)-> str:
    remove_words = ["จ่ายบิลสําเร็จ", "วีเพย์", "VPAY","เลขที่รายการ", "ผู้รับเงินสามารถสแกนคิวอาร์โค้ด"
                    "ธ.กสิกรไทย", "ธ.กสิกรไทย", "จํานวน:", "จำนวน:", "จำนวนเงิน", "ค่าธรรมเนียม",
                    "สแกนตรวจสอบสลิป", "จาก", "ไปยัง", "จํานวนเงิน", "จ่ายบิลสำเร็จ", "๒ ", "๒"
                    "รหัสอ้างอิง", "กรุงไทย", "วันเดือนปีที่ทํารายการ", "ค่าธรรมเนียม", "วันเดือนปีที่ทำรายการ"]
    pattern = "|".join(remove_words)
    clean_text = re.sub(pattern, "", ocr_result)
    return clean_text

def regex_check(ocr_results: str)->list:
    """For checking `ref_id` and `money_amt` from OCR results by using regular expression

    Args:
        ocr_results (str): Results from OCR which now using Pytesseract

    Returns:
        list: Will return to list after regex
    """
    ref_id, money_amt, full_name = [], [], []

    # Checking ref_id
    ref_id = [int(x) for x in re.findall(r'20\d{16}', ocr_results)]
    if len(ref_id) == 0: # if nothing match
        ref_id.append("Please check ref_id again")
    # Checking the money amout
    money_amt = re.findall(r'\b\d{1,3}(?:,\d{3})*\.\d{2}\b', ocr_results)
    money_amt = [float(f.replace(",", "")) for f in money_amt]
    if len(money_amt) == 0: # if nothing match
        money_amt.append("Please check money_amt again")

    # Checking the full_name case
    pattern_with_space = r'(นาย ?[\u0E00-\u0E7F ]+|นางสาว ?[\u0E00-\u0E7F ]+|น\.ส\. ?[\u0E00-\u0E7F ]+|นาง ?[\u0E00-\u0E7F ]+)'
    full_name = re.findall(pattern_with_space, ocr_results)
    if not full_name: # if full name don't have any result
        pattern_without_space = r'(นาย[\u0E00-\u0E7F]+|นางสาว[\u0E00-\u0E7F]+|น\.ส\.[\u0E00-\u0E7F]+|นาง[\u0E00-\u0E7F]+)'
        full_name = re.findall(pattern_without_space, ocr_results)

    if len(full_name) == 0: # if nothing match
        full_name.append("Please check full_name again")

    return ref_id[0], money_amt[0], full_name[0]