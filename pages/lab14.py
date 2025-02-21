import os
import uuid
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

with st.expander("See explanation"):
    st.markdown('''
    Implementation of the RAG with the usage of the Langchain for the
    - PDF files
    - Web URLs
    ''')

# Use Hugging Face Inference API
llm = HuggingFaceEndpoint(
    endpoint_url="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    max_length=512,
    temperature=0.7,
    max_new_tokens=250,
)

def data_processing(documents: list, key: str = '', document_name: str = ''):
    # Split Documents into Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Embed Documents with Hugging Face
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.from_documents(chunks, embedding_model)

    # Create a RAG Chain
    retriever = vector_db.as_retriever()
    rag_chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | (lambda inputs: f"Context: {inputs['context']}\n\nQuestion: {inputs['question']}")
        | llm
    )

    # Query the RAG System
    query = st.text_input(
        f"Ask the question based on the uploaded document({document_name})", 
        key=f"question_{key}"
    )
    if query:
        response = rag_chain.invoke(query)
        st.markdown(f"**Response:** {response}")

if 'web_documents' not in st.session_state:
    st.session_state.web_document_name = ""
    st.session_state.web_documents = []
if 'pdf_documents' not in st.session_state:
    st.session_state.pdf_document_name = ""
    st.session_state.pdf_documents = []

pdf_tab, web_tab = st.tabs(["Pdf", "Web"])
with pdf_tab:
    uploaded_file = st.file_uploader("Pdf uploader: ", type="pdf")
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        # Saving the file locally
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        pdf_loader = PyPDFLoader(file_path)
        st.session_state.pdf_document_name = uploaded_file.name
        st.session_state.pdf_documents = pdf_loader.load()
        data_processing(st.session_state.pdf_documents, key='pdf', document_name=st.session_state.pdf_document_name)

with web_tab:
    web_input = st.text_input("Web URL: ")
    if st.button("RAG it"):
        loader = WebBaseLoader(web_input)
        st.session_state.web_document_name = web_input
        st.session_state.web_documents = loader.load()
    if st.session_state.web_documents:
        data_processing(st.session_state.web_documents, key='web', document_name=st.session_state.web_document_name)