import cv2
import pytesseract
from helper import *
from datetime import datetime

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
clean_text = remove_words(text)

# Extract the reference ID and currency values from the text
ref_id, money_amt, full_name = regex_check(clean_text)

# Checking number of list of ref_id and money_amt
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
# Print the extracted numbers
response = f"Reference ID: {ref_id}\nMoney Amount: {money_amt}\nSender Name: {full_name}\n\nCurrent time: {current_time}"
print(response)