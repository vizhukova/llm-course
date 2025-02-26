import os
import uuid
import fitz  # PyMuPDF
import streamlit as st
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

with st.expander("See explanation"):
    st.markdown('''
    In today's IT landscape, the volume of technical issues can be overwhelming. Imagine
    a system where users can upload PDF documents detailing common IT problems.
    Your task is to develop a system that extracts issue headings from these PDFs,
    converts them into embeddings, and stores both the embeddings and the respective
    documents in a database. Additionally, implement a function for similarity search,
    allowing users to find documents related to a specific IT issue.
    ''')

# Use Hugging Face Inference API
llm = HuggingFaceEndpoint(
    endpoint_url="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    max_length=512,
    temperature=0.7,
    max_new_tokens=250,
)

def extract_headings_from_pdf(pdf_path):
    """Extract headings (bold/large font) from a PDF document."""
    doc = fitz.open(pdf_path)
    headings = []

    for page in doc:
        blocks = page.get_text("blocks")  # Extract text in block format
        for block in blocks:
            text = block[4].strip()
            font_size = page.get_text("dict")['blocks'][0]['lines'][0]['spans'][0]['size']
            if font_size > 10:  # Adjust threshold for font size
                headings.append(text)

    return list(filter(lambda x: x and x.strip(), headings))

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

to_document = lambda pdf_path: [Document(heading, metadata={'document_url': pdf_path}) for heading in extract_headings_from_pdf(pdf_path)]
# Split Documents into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents([
    *to_document("content/PDF1.pdf"),
    *to_document("content/PDF2.pdf"),
    *to_document("content/PDF3.pdf"),
])

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
query = st.text_input("Ask the question")
if query:
    response = rag_chain.invoke(query)
    st.markdown(f"**Response:** {response}")

    results = vector_db.similarity_search(
        query,
        k=3,
    )
    st.markdown("### The possible resolutions:")
    st.markdown("\n".join([f"- In [{result.metadata['document_url']}]({result.metadata['document_url']}) ({result.page_content})" for result in results]))
