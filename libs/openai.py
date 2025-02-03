from env import OPENAI_API_KEY
from openai import OpenAI

def text_to_image(prompt: str) -> str:
    """
    Generates an image based on the given text prompt using the OpenAI DALL-E model.
    Args:
        prompt (str): The text prompt to generate the image from.
    Returns:
        str: The URL of the generated image.
    """

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url