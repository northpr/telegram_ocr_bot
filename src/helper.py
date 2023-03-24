import matplotlib.pyplot as plt
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


def regex_check(ocr_results: str)->list:
    """For checking `ref_id` and `money_amt` from OCR results by using regular expression

    Args:
        ocr_results (str): Results from OCR which now using Pytesseract

    Returns:
        list: Will return to list after regex
    """
    ref_id, money_amt = [], []

    ref_id = [int(x) for x in re.findall(r'20\d{16}', ocr_results)]

    money_amt = re.findall(r'\b\d{1,3}(?:,\d{3})*\.\d{2}\b', ocr_results)
    money_amt = [float(f.replace(",", "")) for f in money_amt]

    return ref_id, money_amt