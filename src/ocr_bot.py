import telebot
import io
import csv
import os
from google.cloud import vision
from helper import remove_words, regex_check
from config import *
import datetime

#TODO: Improve CSV file handling for database
#TODO: Seperate state for each user (ocr_activated)
#TODO: More error handling
#TODO: Make async function

class OCRBot:
    def __init__(self, token, google_app_credentials):
        """
        Instance of the OCRBot class

        Args:
            token (str): API Token from Telegram bot
            google_app_credentials (str): Path to the Vision AI Credential
        """
        self.bot = telebot.TeleBot(token)
        self.ocr_activated = False
        self.authorized_user_ids = []
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_app_credentials
        self.client = vision.ImageAnnotatorClient()

        # Register handlers
        self.register_handlers()

    def register_handlers(self):
        """
        Telegram handlers function for different commands and message type
        """
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=["register"])(self.handle_register)
        self.bot.message_handler(commands=["activate"])(self.handle_activate)
        self.bot.message_handler(commands=["deactivate"])(self.handle_deactivate)
        self.bot.message_handler(commands=["login"])(self.handle_login)
        self.bot.message_handler(content_types=["photo"])(self.handle_image)

    def run(self):
        print("Start running the bot, please wait for 30 seconds")
        print("==============\n")
        self.bot.infinity_polling() # If it has some error it will try to restart

    #TODO: add more command guide...
    def send_welcome(self, message):
        welcome_msg = """ยินดีต้อนรับ เริ่มการใช้ OCR-Bot
/activate - เริ่มการใช้บอท
/deactivate - ปิดการใช้บอท"""
        self.bot.reply_to(message, welcome_msg)

    def handle_register(self, message):
        if message.chat.type == "private":
            user_id = message.from_user.id

            # Check if user_id is already registered
            with open("user_passwords.csv", "r") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if str(user_id) == row[0]:
                        self.bot.reply_to(message, "[BOT] คุณได้ทำการลงทะเบียนแล้ว")
                        return
                    
            self.bot.reply_to(message, "[BOT] ใส่รหัสผ่านสำหรับการลงทะเบียนใช้บอท")
            self.bot.register_next_step_handler(message, self.save_registration)
        else:
            self.bot.reply_to(message, "[BOT] การสมัครสามารถทำได้ในแชทส่วนตัวกับบอทเท่านั้น")

    def save_registration(self, message):
        user_id = message.from_user.id
        password = message.text
        register_date = datetime.datetime.now().strftime("%d-%m-%Y")
        user_list = [str(user_id), password, register_date]

        with open("user_passwords.csv", "a", newline="") as csv_file:
            writer_object = csv.writer(csv_file)
            writer_object.writerow(user_list)
        self.bot.reply_to(message, "[BOT] การลงทะเบียนเสร็จสมบูรณ์ คุณสามารถล็อกอินโดยการพิมพ์ /login")

    def handle_activate(self, message):
        if not self.is_authorized(message):
            return
        self.ocr_activated = True
        self.bot.reply_to(message, "[BOT] เริ่มการใช้งาน OCR-Bot")

    def handle_deactivate(self, message):
        if not self.is_authorized(message):
            return
        self.ocr_activated = False
        self.bot.reply_to(message, "[BOT] ปิดการใช้งาน OCR-Bot")

    def handle_login(self, message):
        chat_id = message.chat.id
        if chat_id in self.authorized_user_ids:
            self.bot.reply_to(message, "[BOT] คุณได้ล็อกอินอยู่แล้ว")
        else:
            self.bot.reply_to(message, "[BOT] โปรดใส่รหัสผ่านเพื่อล็อกอิน")
            self.bot.register_next_step_handler(message, self.verify_password)
    
    def verify_password(self, message):
        user_id = message.from_user.id
        password = message.text

        with open("user_passwords.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if str(user_id) == row[0] and password == row[1]:
                    self.authorized_user_ids.append(user_id)
                    self.bot.reply_to(message, "ล็อกอินสำเร็จ")
                    return
                
        self.bot.reply_to(message, "[BOT] รหัสผ่านผิด โปรดลองอีกครั้ง")

    #TODO: Fixing bot activation even not a user still could login
    def is_authorized(self, message):
        user_id = message.from_user.id
        if message.chat.type == "private" and user_id not in self.authorized_user_ids:
            self.bot.reply_to(message, "[BOT] คุณไม่มีสิทธิ์จะใช้งานบอทนี้ได้")
            return False
        elif message.chat.type == "group" and not self.ocr_activated:
            self.bot.reply_to(message, "[BOT] OCR-Bot is not activated in this group")
            return False
        return True
    
    def handle_image(self, message):
        """
        Process an image by using Google Vision AI and extracts relavant information,
        and sends the results back to the user.

        Args:
            message (telebot messages): The message from user that is the image.
        """
        if not self.is_authorized(message):
            return
        if self.ocr_activated:
            try:
                # Download the image
                file_info = self.bot.get_file(message.photo[-1].file_id)
                image_file = self.bot.download_file(file_info.file_path)
                self.bot.reply_to(message, "[BOT] ได้รับรูปภาพ")

                # Read the image file
                with io.BytesIO(image_file) as image_binary:
                    content = image_binary.read()
                image = vision.Image(content=content)

                # Performs OCR on the image file
                response = self.client.text_detection(image=image)
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
                self.bot.reply_to(message, result_msg)
            except Exception as e:
                # Error message
                error_msg = f"[BOT ERROR] Error performing OCR: {str(e)}"
                self.bot.reply_to(message, error_msg)
                print(error_msg)



        
    