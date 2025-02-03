from env import MODEL_GPT_2_URL

import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

def image_to_text(raw_image: Image) -> str:
    print('raw_image: ', raw_image)
    """
    Generates a caption for a given image.
    Args:
        raw_image (Image): The path to the raw image file.
    Returns:
        str: The generated caption for the image.
    """
    
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_GPT_2_URL)
    feature_extractor = ViTImageProcessor.from_pretrained(MODEL_GPT_2_URL)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_GPT_2_URL)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    pixel_values = feature_extractor(images=[raw_image], return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

    return preds[0].strip()