import telebot
import os
from helper import *
import cv2
import pytesseract
from datetime import datetime

bot = telebot.TeleBot("6129188503:AAH3M2mg3m-H-RnXQPvToLkK6uS9uyYD2RM")

# Define the handler function for the "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the OCR bot! Send me an image to extract the reference ID and currency values.")

# Define the handler function for images
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Download the image
    file_info = bot.get_file(message.photo[-1].file_id)
    image_file = bot.download_file(file_info.file_path)

    # Convert the image to a numpy array
    img = cv2.imdecode(np.frombuffer(image_file, np.uint8), cv2.IMREAD_UNCHANGED)

    # Preprocess the image
    img_processed = img_preprocess(img)

    # Apply OCR to the preprocessed image
    text = pytesseract.image_to_string(img_processed, lang="eng")

    # Extract the reference ID and currency values from the text
    ref_id, money_amt = regex_check(text)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Checking number of list of ref_id and money_amt
    if len(ref_id) == 0:
        ref_id.append("recheck ref_id")
    if len(money_amt) == 0 or (money_amt[0] <= 50 or money_amt[0] >= 500000):
        money_amt.append("recheck money_amt")

    # Create a message to send back to the user
    response = "Reference ID: {}\nMoney Amount: {}\n\nCurrent time: {}".format(ref_id, money_amt, current_time)

    # Send the message back to the user
    bot.reply_to(message, response)

# Run the bot
bot.polling()