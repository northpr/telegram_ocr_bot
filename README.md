# 🤖 Telegram OCRBot for Bank Receipts
This repository contains the source code for the Telegram OCRBot, a powerful bot that can extract text from bank receipt images shared on Telegram. The bot is designed to process receipts from multiple banks, primarily in the Thai language, and respond to the customers on the Telegram app.

The main goal of this project is to provide a fast, accurate, and cost-effective OCR solution that can handle inconsistencies in image sizes and varying types of receipts.
## How to
nbs = notebooks\
src = source codes\
app = app for Dockerize

# 👓 Overview
The project has undergone several iterations to achieve the best possible results. The current approach is to use Google Vision for OCR, which supports the Thai language, and Regular Expression for extracting relevant information from the OCR results. This method is cost-effective, fast, and offers reasonable accuracy.

# 🛣️ Features
- Supports multiple image formats (JPEG, PNG, etc.)
- Processes receipts from multiple banks (kbank, scb, ktb)
- Handles various text orientations and sizes
- Provides accurate OCR results using Google Vision
- Uses Regular Expression for extracting relevant information
- Fast and cost-effective solution

# 📕 Languages and Tools
- Python
- OpenCV
- Tesseract OCR
- Pytesseract
- HuggingFace
- Google Vision API
- Regular Expressions
- Docker

# 🔄 Approaches
## Approach 1: OpenCV + Pytesseract
In this approach, OpenCV was used to find the coordinates of the text regions within the image. Once the coordinates were determined, the image was cropped, and Pytesseract was used to perform OCR on the cropped sections. By specifying the language and the areas to crop, the OCR process yielded good accuracy.

## Approach 2: Donut by HuggingFace
Donut is a deep learning model developed by HuggingFace. This approach aimed to leverage the power of deep learning to improve OCR accuracy. The Donut model was tested on the SROIE dataset, and it produced excellent results. However, implementing the model required knowledge of PyTorch and HuggingFace, and the model did not support the Thai language.

## Approach 3: LayoutLM by HuggingFace
LayoutLM is another deep learning model developed by HuggingFace. This approach aimed to achieve high accuracy by training the model on a large dataset of labeled images. However, the model was difficult to implement and required a considerable amount of time to train. Additionally, cost optimization and deployment presented challenges.

## Approach 4: Google Vision + Regular Expression (Current)
The current approach involves using the Google Vision API to perform OCR on the entire receipt image. The API supports the Thai language and provides a good level of accuracy. After OCR, Regular Expression is used to extract relevant information from the OCR results. This approach is simple, fast, and cost-effective.

## Approaches Comparison

| Approach | Description | Pros | Cons |
| -------- | ----------- | ---- | ---- |
| 1 | OpenCV + Pytesseract | - Good accuracy when specifying language and area to crop and OCR | - Inconsistencies in image size and receipt types require multiple parameters |
| 2 | Donut by HuggingFace | - Excellent results on SROIE dataset | - Requires knowledge of PyTorch and HuggingFace <br> - Does not support Thai language |
| 3 | LayoutLM by HuggingFace | - High accuracy with sufficient labeled data | - Complex implementation <br> - Time-consuming to train <br> - Cost optimization and deployment challenges |
| 4 (Current) | Google Vision + Regular Expression | - Fast and cost-effective <br> - Supports Thai language <br> - Simple but effective | - Accuracy may suffer in certain cases (e.g., multi-line text) |