import telebot
import os
from helper import *
import cv2
import io
from google.cloud import vision
import pytesseract
from datetime import datetime

# TODO: More error handling

# TODO: Change to config.ini
bot = telebot.TeleBot("6129188503:AAH3M2mg3m-H-RnXQPvToLkK6uS9uyYD2RM")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

welcome_msg = """Hi from OCR-HelperBot, here's the command you could use
/reader - starting to use OCRBot
/tutorial - for reading how to use this bot"""

# Define the handler function for the "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, welcome_msg)

#TODO: Could activate and deactivate OCR bot by using command such as /deactivate
@bot.message_handler(commands=["reader"])
def handle(message):
    # Reply text to users
    bot.reply_to(message, "[BOT] Send me an image to read")
    bot.register_next_step_handler(message, handle_image)

# Define the handler function for images
def handle_image(message):
    try:
        # Download the image
        file_info = bot.get_file(message.photo[-1].file_id)
        image_file = bot.download_file(file_info.file_path)
        bot.reply_to(message, "[BOT] Receiving an image")
        
        # Read the image file
        with io.BytesIO(image_file) as image_binary:
            content = image_binary.read()
        
        # Construct an image instance
        image = vision.Image(content=content)
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
        result_msg = f"[RESULT]\n\nReference ID: {ref_id}\nMoney Amount: {money_amt}\nSender Name: {full_name}\nCurrent time: {current_time}"
        print(result_msg)
        print("============\n")
        # Send the message back to the user
        bot.reply_to(message, result_msg)
    except Exception as e:
        # Error message
        error_msg = f"Error performing OCR: {str(e)}"
        bot.reply_to(message, error_msg)
        print(error_msg)

# Run the bot
print("Start running the bot")
print("===========\n")
bot.polling()