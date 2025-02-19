import streamlit as st
import lab13_1
import lab13_2

with st.expander("See explanation"):
    st.markdown('''
    Usage of the Langchain
    1. **HuggingFaceEndpoint** (For Remote API Calls)
    - HuggingFaceEndpoint is used to interact with remote Hugging Face models hosted via the Hugging Face Inference API.

    ✅ Best for:
    - Using models hosted on Hugging Face Hub (i.e., api-inference.huggingface.co).
    - Avoiding the need to install models locally.
    - Leveraging server-side inference without requiring a GPU.
    ❌ Limitations:
    - Slower (because it makes API calls over the internet).
    - Can break if the Hugging Face API changes (as you saw with the deprecation warnings).
    - Some models may have rate limits or require Hugging Face Pro. 

    2. **HuggingFacePipeline** (For Local Model Execution)
    - HuggingFacePipeline is used to run models locally using transformers.pipeline(). Instead of calling an API, it loads the model on your machine.

    ✅ Best for:
    - Running models locally (without API calls).
    - Avoiding API rate limits or server downtime.
    Using custom fine-tuned models that aren't available via an API.
    ❌ Limitations:
    - Requires downloading and loading the model locally.
    - Needs a GPU or a strong CPU for optimal performance.
    ''')

lab_13_1_tab, lab_13_2_tab = st.tabs(["HuggingFaceEndpoint", "HuggingFacePipeline"])

with lab_13_1_tab:
    st.write("HuggingFaceEndpoint")
    lab13_1.run(key='lab_13_1_tab')

with lab_13_2_tab:
    st.write("HuggingFacePipeline")
    lab13_2.run(key='lab_13_2_tab')