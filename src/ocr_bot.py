import telebot
import os
from helper import *
import cv2

bot = telebot.TeleBot("6129188503:AAH3M2mg3m-H-RnXQPvToLkK6uS9uyYD2RM")

@bot.message_handler(commands=['reader']) # Command to start OCR
def handle_ocr_image(message):
    # Reply to the user with a message and ask for an image
    bot.reply_to(message, "Send me an image to perform OCR on.")
    
    # Set the bot's next step to wait for an image
    bot.register_next_step_handler(message, handle_image_receiver)

def handle_image_receiver(message):
    # Check that message is image
    if not message.photo:
        bot.reply_to(message, "That's not an image, Please send again")
        return
    
    # Download image to temp file
    img_file = bot.get_file(message.photo[-1].file_id)
    img_path = os.path.join("/tmp", f"{message.chat.id}.jpg")
    img_file.download(img_path)

    try:
        import pytesseract
        text = pytesseract.image_to_string(img_path)
        bot.reply_to(message, f"OCR result:\n\n{text}")
    except Exception as e:
        bot.reply_to(message, f"Error performing OCR: {str(e)}")
    
    os.remove(img_path)

bot.polling()