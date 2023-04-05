import telebot
import os
import csv
from helper import *
import io
from google.cloud import vision

bot = telebot.TeleBot("6129188503:AAH3M2mg3m-H-RnXQPvToLkK6uS9uyYD2RM")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'g_credential.json' # Getting JSON file from Google Cloud
client = vision.ImageAnnotatorClient()

welcome_msg = """ยินดีต้อนรับ เริ่มการใช้ OCR-Bot
/activate - เริ่มการใช้บอท
/deactivate - ปิดการใช้บอท"""

ocr_activated = False
authorized_user_ids = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=["register"])
def handle_register(message):
    if message.chat.type == "private":
        bot.reply_to(message, "[BOT] ใส่รหัสผ่านสำหรับการลงทะเบียนใช้บอท")
        bot.register_next_step_handler(message, save_registration)
    else:
        bot.reply_to(message, "[BOT] การสมัครสามารถทำได้ในแชทส่วนตัวกับบอทเท่านั้น")

def save_registration(message):
    user_id = message.from_user.id
    password = message.text
    user_list = [str(user_id), password]

    with open("user_passwords.csv", "a", newline="") as csv_file:
        writer_object = csv.writer(csv_file)
        writer_object.writerow(user_list)
    
    bot.reply_to(message, "[BOT] การลงทะเบียนเสร็จสมบูรณ์. คุณสามารถล็อกอินโดยการพิมพ์ /login")

@bot.message_handler(commands=["activate"])
def handle_activate(message):
    global ocr_activated
    if not is_authorized(message):
        return
    ocr_activated = True
    bot.reply_to(message, "[BOT] เริ่มการใช้งาน OCR-Bot")

@bot.message_handler(commands=["deactivate"])
def handle_deactivate(message):
    global ocr_activated
    if not is_authorized(message):
        return
    ocr_activated = False
    bot.reply_to(message, "[BOT] ปิดการใช้งาน OCR-Bot")

@bot.message_handler(commands=["login"])
def handle_login(message):
    global authorized_user_ids
    chat_id = message.chat.id
    if chat_id in authorized_user_ids:
        bot.reply_to(message, "[BOT] คุณได้ล็อกอินอยู่แล้ว")
    else:
        bot.reply_to(message, "[BOT] โปรดใส่รหัสผ่านเพื่อล็อกอิน")
        bot.register_next_step_handler(message, verify_password)


def verify_password(message):
    global authorized_user_ids
    user_id = message.from_user.id
    password = message.text

    with open("user_passwords.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if str(user_id) == row[0] and password == row[1]:
                authorized_user_ids.append(user_id)
                bot.reply_to(message, "ล็อกอินสำเร็จ")
                return
            
    bot.reply_to(message, "[BOT] รหัสผ่านผิด โปรดลองอีกครั้ง")

def is_authorized(message):
    user_id = message.from_user.id
    if message.chat.type == "private" and user_id not in authorized_user_ids:
        bot.reply_to(message, "[BOT] คุณไม่มีสิทธิ์จะใช้งานบอทนี้ได้")
        return False
    elif message.chat.type == "group" and not ocr_activated:
        bot.reply_to(message, "[BOT] OCR-Bot is not activated in this group")
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
            bot.reply_to(message, "[BOT] ได้รับรูปภาพ")
            
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
            regex_result = regex_check(clean_text)

            if regex_result['mistakes'] >= 2:
                result_msg = "[BOT] โปรดลองอีกครั้ง หรือตรวจว่าเป็นใบเสร็จ"
            else:
                result_msg = f"[BOT]\n\nReference ID: {regex_result['ref_id']}\
                    \nMoney Amount: {regex_result['money_amt']}\
                    \nSender Name: {regex_result['full_name']}\
                    \nCurrent time: {regex_result['current_time']}"
                
            print(result_msg)
            print("============\n")
            # Send the message back to the user
            bot.reply_to(message, result_msg)
        except Exception as e:
            # Error message
            error_msg = f"[BOT ERROR] Error performing OCR: {str(e)}"
            bot.reply_to(message, error_msg)
            print(error_msg)

# Run the bot
print("Start running the bot")
print("===========\n")
bot.polling()