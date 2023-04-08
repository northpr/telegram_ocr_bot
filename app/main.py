from ocr_bot import OCRBot
from config import TELEBOT_TOKEN, GOOGLE_APPLICATION_CREDENTIALS

def main():
    bot = OCRBot(TELEBOT_TOKEN, GOOGLE_APPLICATION_CREDENTIALS)
    bot.run()

if __name__ == "__main__":
    main()