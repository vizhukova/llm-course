import os

LOCAL = os.getenv("ENV") == "local"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
HUGGING_FACE_TOKEN = os.environ["HUGGING_FACE_TOKEN"]

MODEL_GPT_2_URL = './model/vit-gpt2-image-captioning' if LOCAL else 'nlpconnect/vit-gpt2-image-captioning'
MODEL_SALESFORCE_URL = './model/blip-image-captioning-base' if LOCAL else 'Salesforce/blip-image-captioning-base'