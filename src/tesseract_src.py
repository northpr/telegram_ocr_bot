import cv2
import numpy as np
import pytesseract
import re
from helper import img_preprocess

# Load the image
img_path = "data_test/kbank_62.jpg"
img = cv2.imread(img_path)

# Preprocess the image
img_bin = img_preprocess(img)

# Apply OCR to the preprocessed image
text = pytesseract.image_to_string(img_bin, lang="eng")

# Extract the reference ID and currency values from the text
ref_id_lst, money_amt = [], []
ref_id_lst = [int(x) for x in re.findall(r'\d{18}', text)]
money_amt_lst = [float(x) for x in re.findall(r'\d+\.\d{2}', text)]

# Print the extracted numbers
print(ref_id_lst)
print(money_amt_lst)