from env import HUGGINGFACEHUB_API_TOKEN

from huggingface_hub import InferenceClient

def generate_text(prompt: str) -> str:
    client = InferenceClient(
        api_key=HUGGINGFACEHUB_API_TOKEN
    )

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=messages, 
        max_tokens=500
    )

    return completion.choices[0].message['content']
