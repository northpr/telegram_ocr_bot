import io
import os
from google.cloud import vision
from helper import *
from datetime import datetime

print("TEST VERSION\n")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

# Load the image
random_img_path = random_image("img_test")
specific_img_path = "img_test/gsb/gsb_2.jpg"

# Read the image file
with io.open(random_img_path, 'rb') as image_file:
    content = image_file.read()

# Construct an image instance
image = vision.Image(content=content)

# Performs OCR on the image file
response = client.text_detection(image=image)
texts = response.text_annotations

# Extract the text from the response
text = texts[0].description
print(f"Img path: {random_img_path}")
print(f"\nDirty text: \n{text}")
print("\n==============\n")
clean_text = remove_words(text)
print(f"Clean text: \n{clean_text}")
print("\n==============\n")


# Extract the reference ID and currency values from the text
regex_result = regex_check(clean_text)

    
# Print the extracted numbers
response = f"[Aquar Team]\n\nเวลาที่ทำรายการ: {format_ref_id_time(regex_result['ref_id'])}\
                        \n\nรหัสอ้างอิง: {regex_result['ref_id']}\
                        \nชื่อผู้ทำรายการ: {regex_result['full_name']}\
                        \nเลขที่บัญชี: {regex_result['acc_number']}\
                        \nจำนวนเงิน: {'{:,.2f}'.format(regex_result['money_amt'])}\
                        \n\n>> ตรวจสอบรายการให้สักครู่ค่ะ 😋"
print(response)