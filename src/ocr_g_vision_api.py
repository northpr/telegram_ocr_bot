import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
import cv2
import numpy as np
import re
from helper import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

# Load the image
random_img_path = random_image("img_test")
print(random_img_path)

img_path = random_img_path
specific_img_path = "img_test/ktb/ktb_97.jpg"

# Read the image file
with io.open(specific_img_path, 'rb') as image_file:
    content = image_file.read()

# Construct an image instance
image = types.Image(content=content)

# Performs OCR on the image file
response = client.text_detection(image=image)
texts = response.text_annotations

# Extract the text from the response
text = texts[0].description
print(text, type)
# Extract the reference ID and currency values from the text
ref_id, money_amt = regex_check(text)

# # Checking number of list of ref_id and money_amt
# if len(ref_id) == 0:
#     ref_id.append("recheck ref_id")
# if len(money_amt) == 0 or (money_amt[0] <= 50 or money_amt[0] >= 500000):
#     money_amt.append("recheck money_amt")
    
# Print the extracted numbers
print(ref_id)
print(money_amt)