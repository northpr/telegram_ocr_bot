import io
import os
from google.cloud import vision
from receipt_processor import OCRVision, VPayExtractor
from tele_msg import TeleHelper
from utils import Utils
from datetime import datetime
import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser(description="OCR image processing")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--random", action="store_true", help="Select a random image")
    group.add_argument("-p", "--path", type=str, help="Specify the path of the image")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress the output")
    parser.add_argument("-n", "--number", type=int, default=1, help="Specify the number of images to process")
    return parser.parse_args()

def main():
    args = parse_args()
    client = vision.ImageAnnotatorClient()
    for i in range(0, args.number):
        if args.random:
            img_path, img_name = Utils.find_img(rand_dir="../data/img")
        else:
            img_path, img_name = Utils.find_img(rand_dir="img_path", spec_img_path=args.path)
        if not img_path:
            print("Image not found. Please check the specified path.")
            return

        # Read the image file
        with io.open(img_path, 'rb') as image_file:
            content = image_file.read()
        print(f"PATH: {img_path}")
        texts = OCRVision.perform_ocr(client, content)
        # Extract the text and from the response
        text = texts[0].description
        clean_text = VPayExtractor.remove_words(text)
        regex_result = VPayExtractor.regex_check(clean_text)
        log_msg = f"{i}, {img_name} ,{regex_result['ref_id']}, {regex_result['trans_id']}, \
{regex_result['money_amt']}, {regex_result['full_name']}, {regex_result['acc_number']}, {regex_result['bank_name']}"
        # Write the extracted data to a CSV file
        with open('../data/log.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['img_name','ref_id', 'trans_id', 'money_amt', 'full_name', 'acc_number', 'bank_name'])
            writer.writerow([img_name, regex_result['ref_id'], regex_result['trans_id'], regex_result['money_amt'],
                            regex_result['full_name'], regex_result['acc_number'], regex_result['bank_name']])
        # Print the extracted numbers
        result_msg = TeleHelper.response_result_msg(regex_result=regex_result, mistakes=regex_result['mistakes'] >= 2)

        if args.quiet:
            print(log_msg)
        else:
            print(f"\nDirty text: \n{text}")
            print("\n---------------\n")
            print(f"Clean text: \n{clean_text}")
            print("\n---------------\n")
            print(result_msg)
            print("\n---------------\n")
            print(log_msg)

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
    main()