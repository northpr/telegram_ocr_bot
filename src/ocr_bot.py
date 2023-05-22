import telebot
import csv
import os
from google.cloud import vision
from receipt_processor import OCRVision, VPayExtractor, TeleHelper, Utils
from config import *
import time
import datetime

#TODO: More error handling
#TODO: Make async function
#TODO: Change database for registration and activated_chatid
#TODO: boto3 for register and activate chatroom

class OCRBot:
    def __init__(self, token, google_app_credentials):
        """
        Instance of the OCRBot class

        Args:
            token (str): API Token from Telegram bot
            google_app_credentials (str): Path to the Vision AI Credential
        """
        self.bot = telebot.TeleBot(token)
        self.authorized_user_ids = []
        self.ocr_activated_chatid = {}
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
        self.bot.message_handler(commands=["status"])(self.handle_status)
        self.bot.message_handler(commands=["login"])(self.handle_login)
        self.bot.message_handler(content_types=["photo"])(self.handle_image)

    def run(self):
        print("RUNNING")
        try:
            self.bot.infinity_polling() # If it has some error it will try to restart
        except Exception as e:
            print("ERROR, API_ERROR_ACCESS")
            time.sleep(1)

    def send_welcome(self, message):
        welcome_msg = """ยินดีต้อนรับ เริ่มการใช้ OCR-Bot
/activate - เริ่มการใช้บอท
/deactivate - ปิดการใช้บอท
/status - เช็คสถานะบอท"""
        self.bot.reply_to(message, welcome_msg)

    def handle_register(self, message):
        """
        Handling register when users type /register.
        1. It will check that the user is already registered or not
        2. If not it needs users (support staff) to fill in the user_id and the function will proceed
        3. Next to get_staff_id_and_password() function
        """
        if message.chat.type == "private":
            user_id = message.from_user.id

            # Check if user_id is already registered
            with open("user_passwords.csv", "r") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if str(user_id) == row[0]:
                        self.bot.reply_to(message, "[BOT ADMIN] คุณได้ทำการลงทะเบียนแล้ว")
                        return
                    
            self.bot.reply_to(message, "[BOT ADMIN] โปรดใส่รหัสพนักงานสำหรับการลงทะเบียน (ตัวอย่าง: SNO-0001)")
            # lambda m: self.get_staff_id_and_password(m) Receive next message 
            # and calls the get_staff_id_and_password() function
            self.bot.register_next_step_handler(message, lambda m: self.get_staff_id_and_password(m))
        else:
            self.bot.reply_to(message, "[BOT ADMIN] การสมัครสามารถทำได้ในแชทส่วนตัวกับบอทเท่านั้น")

    def get_staff_id_and_password(self, message):
        staff_id = message.text
        self.bot.reply_to(message, "[BOT ADMIN] ใส่รหัสผ่านสำหรับการลงทะเบียนใช้บอท")
        # lambda m: self.save_registration(m, staff_id) Receive next message 
        # and calls the `save_registration() method with this message and the previously obtained `staff_id`
        self.bot.register_next_step_handler(message, lambda m: self.save_registration(m, staff_id))

    def save_registration(self, message, staff_id):
        message_info = TeleHelper.extract_message_info(message)
        user_id = message.from_user.id
        password = message.text
        register_date = datetime.datetime.now().strftime("%d-%m-%Y")
        user_list = [str(user_id), staff_id, password, register_date]

        with open("user_passwords.csv", "a", newline="") as csv_file:
            writer_object = csv.writer(csv_file)
            writer_object.writerow(user_list)
        response_msg = f"[BOT] {staff_id}\nการลงทะเบียนเสร็จสมบูรณ์ คุณสามารถล็อกอินโดยการพิมพ์ /login"
        self.bot.reply_to(message, response_msg)
        log_msg = f"REGISTER, {staff_id}, {message_info['user_id']}, {message_info['user_username']}, \
{message_info['user_firstname']}"
        print(log_msg)

    def handle_activate(self, message):
        if not self.is_authorized(message):
            return
        message_info = TeleHelper.extract_message_info(message)
        self.ocr_activated_chatid[message.chat.id] = True
        self.bot.reply_to(message, "[Aquar Team] เริ่มการใช้งานค่ะ 🟢")
        # Providing log on which chat the bot is activated
        user_id = message.from_user.id
        chat_id = message.chat.id
        log_msg = f"ACTIVATE, {message_info['user_id']}, {message_info['chat_id']}, \
{message_info['user_username']}, {message_info['user_firstname']}"
        print(log_msg)

    def handle_deactivate(self, message):
        if not self.is_authorized(message):
            return
        message_info = TeleHelper.extract_message_info(message)
        self.ocr_activated_chatid[message.chat.id] = False
        self.bot.reply_to(message, "[Aquar Team] ปิดการใช้งานค่ะ 🔴")
        log_msg = f"DEACTIVATE, {message_info['user_id']}, {message_info['chat_id']}, \
{message_info['user_username']}, {message_info['user_firstname']}"
        print(log_msg)

    def handle_status(self, message):
        """
        Check if the bot is activated or deactivated on that specific chat

        Args:
            message (_type_): _description_
        """
        if not self.is_authorized(message):
            return
        chat_id = message.chat.id
        status = self.ocr_activated_chatid.get(chat_id, True)

        if status:
            response = "[Aquar Team] ระบบพร้อมทำงานค่ะ 🟢"
        else:
            response = "[Aquar Team] ระบบไม่พร้อมทำงานค่ะ 🔴 รบกวน /activate เพื่อใช้งาน"
        self.bot.reply_to(message, response)

    def handle_login(self, message):
        chat_id = message.chat.id
        if chat_id in self.authorized_user_ids:
            self.bot.reply_to(message, "[BOT ADMIN] คุณได้ล็อกอินอยู่แล้ว")
        elif message.chat.type != "private":
            self.bot.reply_to(message, " [BOT ADMIN] ล็อกอินสามารถทำได้ในแชทส่วนตัวกับบอทเท่านั้น")
        else:
            self.bot.reply_to(message, "[BOT ADMIN] โปรดใส่รหัสผ่านเพื่อล็อกอิน")
            self.bot.register_next_step_handler(message, self.verify_password)
    
    def verify_password(self, message):
        user_id = message.from_user.id
        password = message.text

        with open("user_passwords.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if str(user_id) == row[0] and password == row[2]:
                    self.authorized_user_ids.append(user_id)
                    self.bot.reply_to(message, "ล็อกอินสำเร็จ")
                    return
                
        self.bot.reply_to(message, "[BOT ADMIN] รหัสผ่านผิด โปรดลองอีกครั้ง หรือกด /login")

    def is_authorized(self, message):
        user_id = message.from_user.id
        if user_id not in self.authorized_user_ids:
            self.bot.reply_to(message, "[Aquar Team] โปรดติดต่อทีม Support เพื่อการดูแลค่ะ")
            return False
        return True
    
    def handle_image(self, message):
        """
        Process an image by using Google Vision AI and extracts relavant information,
        and sends the results back to the user.

        Args:
            message (telebot messages): The message from user that is the image.
        """
        if self.ocr_activated_chatid.get(message.chat.id, False):
            try:
                # Getting the information of the message
                message_info = TeleHelper.extract_message_info(message)
                # Download the image
                file_info = self.bot.get_file(message.photo[-1].file_id)
                image_file = self.bot.download_file(file_info.file_path)
                self.bot.reply_to(message, "[Aquar Team] รบกวนรอสักครู่นะคะ ☺️")
                # Performing OCR
                texts = OCRVision.perform_ocr(self.client, image_file)
                text = texts[0].description
                clean_text = VPayExtractor.remove_words(text) # Remove unnesscessary words
                regex_result = VPayExtractor.regex_check(clean_text) # Extract the reference ID and currency values from the text

                if regex_result['mistakes'] >= 2:
                    result_msg = "[BOT ADMIN] โปรดลองอีกครั้ง หรือตรวจสอบว่าเป็นใบเสร็จ"
                else:
                    result_msg = f"[Aquar Team]\n\nเวลาที่ทำรายการ: {regex_result['formatted_ref_id']}\
                        \n\nรหัสอ้างอิง: {regex_result['ref_id']}\
                        \nชื่อผู้ทำรายการ: {regex_result['full_name']}\
                        \nเลขที่บัญชี: {regex_result['acc_number']}\
                        \nจำนวนเงิน: {regex_result['money_amt']}\
                        \n\n>> ตรวจสอบรายการให้สักครู่ค่ะ 😋"

                # Setting up log for Grafana use    
                log_msg = f"RESULT, {message_info['chat_id']}, {message_info['chat_title']}, \
{message_info['user_id']}, {message_info['user_username']}, {message_info['user_firstname']}, \
{regex_result['ref_id']}, {regex_result['money_amt']}, {regex_result['full_name']}, \
{regex_result['acc_number']}, {regex_result['bank_name']}"
                print(log_msg)
                # Send the message back to the user
                self.bot.reply_to(message, result_msg)
            except Exception as e:
                # Error message
                error_msg = f"[Aquar Team] โปรดเช็คให้มั่นใจว่าเป็นใบโอนเงิน"
                self.bot.reply_to(message, error_msg)
                log_msg = f"OCR_ERROR, {message_info['chat_id']}, {message_info['chat_title']}, \
{message_info['user_id']}, {message_info['user_username']}, {message_info['user_firstname']},"
                print(log_msg)

        else:
            self.bot.reply_to(message, "[BOT] คุณไม่สามารถใช้บอทได้ ถ้าย้งไม่เริ่มการใช้งานในแชทนี้")