#pip install llama-cpp-python
import streamlit as st
from llama_cpp import Llama
import os

model_path = 'model/llama-2-7b-chat.Q2_K.gguf'
print(os.path.exists(model_path))
llama=Llama(model_path=model_path)


def generate_output(prompt, max_tokens, temperature, top_p):
    output= llama(prompt, temperature=0.75,
    max_tokens=2000,
    top_p=1)
    return output['choices'][0]['text'] 


def main():
    with st.expander("See explanation"):
        st.markdown('''
            Experiment usage of the GGUF model locally for prompt engineering.
            https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf
        ''')

    st.title("Day 7: Prompt Enginnering")
    prompt = st.text_area("Enter your prompt here:")

    max_tokens=st.slider("Max Tokens", min_value=1,max_value= 100,value=50)
    temperature=st.slider("Temperature", 0.0, 1.0, 0.1,step=0.1)
    top_p=st.slider("Top P", 0.0, 1.0, 0.9,step=0.1)
    print(max_tokens)
    if st.button("Generate Output"):
        st.spinner("Generating...")
        result=generate_output(prompt, max_tokens, temperature, top_p)
        st.success("Output Generated!")
        st.write("Generated output")
        st.write(result)
        
main()