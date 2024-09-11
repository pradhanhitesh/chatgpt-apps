<h1>Text Extraction and Preprocessing with GPT</h1>

This repository contains two Python scripts that work together to extract and preprocess medical report data from PDFs and then preprocess the extracted text using GPT for further analysis. The two primary functionalities include:

1. Text Extraction from PDF Files: Extract subject IDs, impression texts, and Fazekas scores from MRI report PDFs.

2. Text Preprocessing using GPT: Use OpenAI's GPT model to process and format the extracted texts for further use, including classification of findings and extraction of specific fields like location and cause.

<h2>Requirements</h2>
Make sure you have the following dependencies installed:

1. Python 3.8+
2. pandas
3. PyPDF2
4. OpenAI Python SDK
5. pytz
6. json
7. glob
8. shutil

<h2>License</h2>
This project is licensed under the MIT License. See the LICENSE file for more details.