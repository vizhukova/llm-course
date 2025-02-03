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
        model="meta-llama/Llama-3.3-70B-Instruct",  
        messages=messages,
        max_tokens=500
    )

    return completion.choices[0].message['content']
