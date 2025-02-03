from env import LOCAL

import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from libs.openai import text_to_image as dalle_text_to_image
from libs.gpt2 import image_to_text as gpt2_image_to_text
from libs.salesforce import image_to_text as salesforce_image_to_text

with st.expander("See explanation"):
    st.markdown('''
        **Lab 3-4:**
             **Downloading Model :**     
                Step 1: Search for an Image to Text Model on Hugging Face  
                Visit the Hugging Face Model Hub at https://huggingface.co/models and search for an Image to  
                Text model. For this example, we are using the nlpconnect/vit-gpt2-image-captioning model,  
                but feel free to choose a similar one.  
                Step 2: Download the Model using the Git Repository  
                Clone the Git repository associated with the selected model. You can find the repository link on  
                the Hugging Face model page.  
                Step 3: Check Model Functionality with Sample Code  
                Navigate to the cloned repository and follow the provided instructions for running a sample  
                code. This ensures that the model is downloaded correctly and functions as expected.  
                Step 4: Model is Up and Running  
                Once you have successfully run the sample code and verified that the model is working, you can  
                proceed to the app integration  
                **App Integration :**  
                    Step 1: Choose a Frontend Library  
                    Decide on a frontend library for your application. Options include Streamlit, React JS, or  
                    Angular.  
                    Step 2: Build the Frontend  
                    Create the frontend for your application using the chosen library.  
                    Step 3: Upload Images and Generate Captions  
                    Implement a feature to allow users to upload images. Use the previously downloaded model to  
                    generate captions for the uploaded images.  
                    Step 4: Display Uploaded Image and Generated Caption  
                    Display the uploaded image along with the generated caption on the frontend.  
                    Step 5: Optimize for Most Appropriate Captions  
                    Experiment with different pre-trained models to find the one that generates the most  
                    appropriate captions for the uploaded images. You can replace the model in the code  
                    accordingly.  
    ''')

salesforce, gpt2 = model_options = ("Salesforce/blip-image-captioning-base", "nlpconnect/vit-gpt2-image-captioning")
image_generator_tab, text_to_image_tab = st.tabs(["Image Generator", "Text to Image"])

def display_image(image_url, caption="Generated Image", request_based = True):
    if request_based:
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
    else:
        img = Image.open(image_url)
    st.image(img, caption=caption, use_container_width=True)

def display_tab_content(image_url: str, raw_image: Image, request_based:bool = True, model_option: str = salesforce):
    result = []

    if LOCAL:
        st.write("The local (downloaded) model has been used")
    else:
        st.write("The model from Hugging Face's server has been used")

    display_image(image_url, caption="Input Image", request_based=request_based)

    if model_option == salesforce:
        res = salesforce_image_to_text(raw_image)
        result.append(f"**Conditional image captioning:** {res['conditional']}")
        result.append(f"**Unconditional image captioning:** {res['unconditional']}")

    elif model_option == gpt2:
        result.append(f"**Unconditional image captioning:** {gpt2_image_to_text(raw_image)}")
    
    for img_caption in result:
        st.write(img_caption)

with image_generator_tab:
    st.title("Image Generator")
    st.markdown("""
        This app allows you to generate images based on a text prompt.
        Enter your prompt below and click the 'Generate Image' button to start.
    """)

    prompt = st.text_input("Enter your prompt:", "")

    if st.button("Generate Image"):
        if prompt:
            image_url = dalle_text_to_image(prompt)
            try:
                display_image(image_url, caption="Generated Image", request_based=True)
                st.write(image_url)
            except Exception as e:
                st.error(f"Error generating image: {e}")
        else:
            st.error("Please enter a prompt to generate an image.")

with text_to_image_tab:
    img_tab_url = None
    img_tab_upload_url = None

    st.title("Text to Image")

    model_option = st.selectbox("What model would you like to use?", model_options)

    sub_tab_url, sub_tab_upload = st.tabs(["Upload by url", "Upload by file"])

    with sub_tab_url:
        img_tab_url = st.text_input("Enter your image url:", "")
        if st.button("Generate text by url"):
            if  img_tab_url:
                try:
                    raw_image = Image.open(requests.get(img_tab_url, stream=True).raw).convert('RGB')
                    display_tab_content(img_tab_url, raw_image, request_based=True, model_option=model_option)
                except Exception as e:
                    st.error(f"Error generating text: {e}")
            else:
                st.error("Please enter an image url.")

    with sub_tab_upload:
        img_tab_upload_url = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
        if st.button("Generate text by upload"):
            if  img_tab_upload_url:
                try:
                    raw_image = Image.open(img_tab_upload_url).convert('RGB')
                    display_tab_content(img_tab_upload_url, raw_image, request_based=False, model_option=model_option)
                except Exception as e:
                    st.error(f"Error generating text: {e}")
            else:
                st.error("Please upload an image.")


    