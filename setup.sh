#!/bin/bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# for llama-cpp
sudo apt install -y libgomp1 gcc g++ build-essential cmake ninja
pip install --no-cache-dir --force-reinstall llama-cpp-python

pip install -r requirements.txt

# For lab9 to be able use the pytesseract
sudo apt-get install tesseract-ocr


