import telebot
import os
from helper import *
import io
from google.cloud import vision
from datetime import datetime

bot = telebot.TeleBot("6129188503:AAH3M2mg3m-H-RnXQPvToLkK6uS9uyYD2RM")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

welcome_msg = """Hi from OCR-HelperBot, here's the command you could use
/activate - activate OCR-Bot
/deactivate - deactivate OCR-Bot"""

ocr_activated = False
authorized_chat_ids = []
password = "password123"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=["activate"])
def handle_activate(message):
    global ocr_activated
    if not is_authorized(message):
        return
    ocr_activated = True
    bot.reply_to(message, "OCRBot is now activated")

@bot.message_handler(commands=["deactivate"])
def handle_deactivate(message):
    global ocr_activated
    if not is_authorized(message):
        return
    ocr_activated = False
    bot.reply_to(message, "OCR-Bot is now deactivated")

@bot.message_handler(commands=["login"])
def handle_login(message):
    global authorized_chat_ids
    chat_id = message.chat.id
    if chat_id in authorized_chat_ids:
        bot.reply_to(message, "You're already logged in.")
    else:
        bot.reply_to(message, "Please enter password to login.")
        bot.register_next_step_handler(message, verify_password)

def verify_password(message):
    global authorized_chat_ids
    if message.text == password:
        authorized_chat_ids.append(message.chat.id)
        bot.reply_to(message, "Password is correct. You're now logged in.")
    else:
        bot.reply_to(message, "Password is incorrect. Please try again.")

def is_authorized(message):
    if message.chat.id not in authorized_chat_ids:
        bot.reply_to(message, "You are not authorized to use this bot.")
        return False
    return True

@bot.message_handler(content_types=["photo"])
def handle_image(message):
    global ocr_activated
    if not is_authorized(message):
        return
    if ocr_activated:
        try: # Need to be here to focus only image file
            # Download the image
            file_info = bot.get_file(message.photo[-1].file_id)
            image_file = bot.download_file(file_info.file_path)
            bot.reply_to(message, "[BOT] Receiving an image")
            
            # Read the image file
            with io.BytesIO(image_file) as image_binary:
                content = image_binary.read()
            image = vision.Image(content=content)

            # Performs OCR on the image file
            response = client.text_detection(image=image)
            texts = response.text_annotations

            # Extract the text from the response
            text = texts[0].description
            clean_text = remove_words(text)

            # Extract the reference ID and currency values from the text
            ref_id, money_amt, full_name, mistakes = regex_check(clean_text)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if mistakes >= 2:
                result_msg = "Please check that it's real receipt"
            else:
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