import cv2
import numpy as np
import pytesseract
import re
from helper import *

# Load the image
random_img_path = random_image("img_test")
print(random_img_path)

img_path = random_img_path
specific_img_path = "img_test/kbank/kbank_69.jpg"

img = cv2.imread(img_path)

# Preprocess the image
img_processed = img_preprocess(img)

# Apply OCR to the preprocessed image
text = pytesseract.image_to_string(img_processed, lang="eng")

# Extract the reference ID and currency values from the text
ref_id, money_amt = regex_check(text)

# Checking number of list of ref_id and money_amt
if len(ref_id) == 0:
    ref_id.append("recheck ref_id")
if len(money_amt) == 0 or (money_amt[0] <= 50 or money_amt[0] >= 500000):
    money_amt.append("recheck money_amt")
    
# Print the extracted numbers
print(ref_id)
print(money_amt)