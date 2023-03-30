import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
import cv2
import numpy as np
import re
from helper import *
from datetime import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

# Load the image
random_img_path = random_image("img_test")
print(random_img_path)

img_path = random_img_path
specific_img_path = "img_test/ktb/ktb_97.jpg"

# Read the image file
with io.open(img_path, 'rb') as image_file:
    content = image_file.read()

# Construct an image instance
image = types.Image(content=content)

# Performs OCR on the image file
response = client.text_detection(image=image)
texts = response.text_annotations

# Extract the text from the response
text = texts[0].description
clean_text = remove_words(text)

# Extract the reference ID and currency values from the text
ref_id, money_amt, full_name = regex_check(clean_text)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
# Print the extracted numbers
response = f"Reference ID: {ref_id}\nMoney Amount: {money_amt}\nSender Name: {full_name}\n\nCurrent time: {current_time}"
print(response)