#!/bin/bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# For lab9 to be able use the pytesseract
sudo apt-get install tesseract-ocr