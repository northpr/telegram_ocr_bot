import telebot

class TeleHelper():
    @staticmethod
    def extract_message_info(message):
        """
        Receive the message from the Telegram sender and getting information

        Args:
            message (_type_): Message from the sender

        Returns:
            _type_: Dict
        """
        message_info = {
            "chat_id" : message.chat.id,
            "chat_title": message.chat.title,
            "user_id": message.from_user.id,
            "user_username": message.from_user.username,
            "user_firstname": message.from_user.first_name
        }
        return message_info
    
    @staticmethod
    def response_result_msg(regex_result:str, mistakes:bool=False)-> str:
        """
        For result response msg

        Args:
            regex_result (str): Result form regex which is in dictionary
            mistakes (bool, optional): Number of mistakes from the extraction. Defaults to False.

        Returns:
            _type_: _description_
        """
        if mistakes:
            result_msg = "[BOT ADMIN] โปรดลองอีกครั้ง หรือตรวจสอบว่าเป็นใบเสร็จ"
        else:
            result_msg = f"[Aquar Team]\n\nเวลาที่ทำรายการ: {regex_result['formatted_ref_id']}\
                        \n\nรหัสอ้างอิง: {regex_result['ref_id']}\
                        \nรหัสรายการ: {regex_result['trans_id']}\
                        \nชื่อผู้ทำรายการ: {regex_result['full_name']}\
                        \nเลขที่บัญชี: {regex_result['acc_number']}\
                        \nจำนวนเงิน: {regex_result['money_amt']}\
                        \n\n>> ตรวจสอบรายการให้สักครู่ค่ะ 😋"
            
        return result_msg