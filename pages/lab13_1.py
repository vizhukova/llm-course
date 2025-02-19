import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from env import HUGGINGFACEHUB_API_TOKEN 

def run(key=""):
    model_options = {
        "openai-community/gpt2": {
            "model_id": "https://api-inference.huggingface.co/models/openai-community/gpt2",
            "task": "text-generation",
        },
        "meta-llama/Llama-3.2-1B": {
            "model_id": "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B",
            "task": "text-generation",
        },   

        "mistralai/Mistral-7B-Instruct-v0.2":{
            "model_id": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            "task": "text-generation",
        }
    }
    model_option = st.selectbox("What embedding option you would like to use?", model_options.keys(), key=f"model_selectbox{key}")

    llm = HuggingFaceEndpoint(
        endpoint_url=model_options[model_option]['model_id'],
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        task=model_options[model_option]['task'],
    )

    template = """Provide the names for the {area} company"""
    prompt = PromptTemplate.from_template(template)

    area = st.text_input("Provide are where your company is working", key=f"area{key}")
    if st.button("Generate", key=f"generate{key}"):
        formatted_prompt = prompt.format(area=area)
        answer = llm.invoke(formatted_prompt)
        st.write("**Answer:** ", answer)

def __main__():
    run()

if __name__ == "__main__":
    __main__()