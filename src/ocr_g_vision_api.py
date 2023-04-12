import io
import os
from google.cloud import vision
from helper import *
from datetime import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

# Load the image
random_img_path = random_image("img_test")
print(random_img_path)

img_path = random_img_path
specific_img_path = "img_test/ktb/ktb_64.jpg"

# Read the image file
with io.open(specific_img_path, 'rb') as image_file:
    content = image_file.read()

# Construct an image instance
image = vision.Image(content=content)

# Performs OCR on the image file
response = client.text_detection(image=image)
texts = response.text_annotations

# Extract the text from the response
text = texts[0].description
print(text)
clean_text = remove_words(text)

# Extract the reference ID and currency values from the text
regex_result = regex_check(clean_text)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
# Print the extracted numbers
response = f"[BOT]\n\nรหัสอ้างอิง: {regex_result['ref_id']}\
                        \nจำนวนเงิน: {regex_result['money_amt']}\
                        \nผู้ฝาก: {regex_result['full_name']}\
                        \nเวลาที่ทำรายการ: {regex_result['current_time']}"
print(response)