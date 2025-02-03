from env import MODEL_SALESFORCE_URL

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def image_to_text(raw_image: Image) -> str:
    """
    Generates a caption for a given image.
    Args:
        raw_image (Image): The path to the raw image file.
    Returns:
        str: The generated caption for the image.
    """
    result = {}
    processor = BlipProcessor.from_pretrained(MODEL_SALESFORCE_URL)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_SALESFORCE_URL)

    # conditional image captioning
    text = "a photography of"
    inputs = processor(raw_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    result['conditional'] = processor.decode(out[0], skip_special_tokens=True)

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    result['unconditional'] = processor.decode(out[0], skip_special_tokens=True)

    return result
