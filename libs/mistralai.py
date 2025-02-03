from env import HUGGING_FACE_TOKEN
from huggingface_hub import InferenceClient

def generate_text(prompt: str) -> str:
    client = InferenceClient(
        api_key=HUGGING_FACE_TOKEN
    )

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",  
        messages=messages,
        max_tokens=500
    )

    return completion.choices[0].message['content']
