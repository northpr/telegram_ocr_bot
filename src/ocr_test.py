import io
import os
from google.cloud import vision
from helper import *
from datetime import datetime
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="OCR image processing")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--random", action="store_true", help="Select a random image")
    group.add_argument("-p", "--path", type=str, help="Specify the path of the image")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress the output")
    return parser.parse_args()

def main():
    args = parse_args()
    print("TEST VERSION\n")
    client = vision.ImageAnnotatorClient()
    #  Argparse
    if args.random:
        img_path = find_img(rand_dir="img_test")
    else:
        img_path = find_img(rand_dir="img_path", spec_img_path=args.path)
    if not img_path:
        print("Image not found. Please check the specified path.")
        return

    # Read the image file
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()
    texts = perform_ocr(client, content)
    # Extract the text from the response
    text = texts[0].description
    clean_text = remove_words(text)
    regex_result = regex_check(clean_text)
    
    # Print the extracted numbers
    response = f"[Aquar Team]\n\nเวลาที่ทำรายการ: {format_ref_id_time(regex_result['ref_id'])}\
                            \n\nรหัสอ้างอิง: {regex_result['ref_id']}\
                            \nชื่อผู้ทำรายการ: {regex_result['full_name']}\
                            \nเลขที่บัญชี: {regex_result['acc_number']}\
                            \nจำนวนเงิน: {'{:,.2f}'.format(regex_result['money_amt'])}\
                            \n\n>> ตรวจสอบรายการให้สักครู่ค่ะ 😋"
    if args.quiet:
        print(f"Img path: {img_path}")
        print(response)
    else:
        print(f"Img path: {img_path}")
        print(f"\nDirty text: \n{text}")
        print("\n==============\n")
        print(f"Clean text: \n{clean_text}")
        print("\n==============\n")
        print(response)

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
    main()