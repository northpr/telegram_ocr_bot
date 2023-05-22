## receipt_processor.py
`OCRVison` - is responsible for performing OCR operations. All methods are static, meaning they can be called directly on the class without creating an instance of the class.

`VPayExtractor` - is responsible for extraction of different fields from OCR results. Like OCRVison, all methods in this class are static as well.

`TeleHelper` - is responsible for extracting message information from a Telegram message. All methods in this class are static.


## utils.py

`Utils` - provides various helper functions such as formatting a reference ID and time, converting to Unix timestamp, and finding an image. All methods in this class are static.