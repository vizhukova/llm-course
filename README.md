# LLM Course

Welcome to the LLM Course project! This README provides an overview of the project, setup instructions, and other relevant information.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

The LLM Course project is designed to provide a comprehensive learning experience for those interested in Large Language Models (LLMs). This course covers various aspects of LLMs, including their architecture, training, and applications.

## Features

- **Lab 3-4**: Image generation from text and from text to image. 
- **Exercise 3**: Language Learning Assistant. 
- **Exercise 4**: Learning Tutor Chatbot. 
- **Lab 5-8**: Prompt Enginnering. 
- **Lab 9-12**: Tokenization and Embedding from different formats (PDF, Image, Docx, xls). 
Working with the Vector DB.
- **Lab 13**: Langchain
- **Lab 14**: RAG based on Langchain

## Installation

To get started with the LLM Course, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/llm-course.git
    ```
2. Navigate to the project directory:
    ```bash
    cd llm-course
    ```
3. Install the required dependencies:
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
4. Go to https://huggingface.co/ and download models into the `/model` folder
    - https://huggingface.co/Salesforce/blip-image-captioning-base
    - https://huggingface.co/nlpconnect/vit-gpt2-image-captioning
    - https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf

## Usage

Fill the .env file with the 
```
OPENAI_API_KEY=""
HUGGINGFACEHUB_API_TOKEN=""
ENV="local" #  'local' if you downloaded all model into folder **/model** OR keep this value empty ''
to use the server version
USER_AGENT = "Mozilla/5.0" # for lab14 - to upload the content from the web
```

To start the course, run the following command:
```bash
python -m streamlit run ./pages/main.py
```

Follow the on-screen instructions to navigate through the course materials.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
