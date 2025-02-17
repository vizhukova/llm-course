import os
import uuid
import streamlit as st
from lab9.lab9_2_pdf import pdf_to_words
from lab9.lab9_3_image import image_to_words
from lab9.lab9_4_docx import doc_to_paragraphs
from lab9.lab9_5_xls import extract_data_from_excel
from lab10.lab10_1_word_embedding import embed_sentences as embed_sentences_with_nltk
from lab10.lab10_2_sentence_transformer import embed_sentences as embed_sentences_with_hugging_face
from lab10.lab10_3_openai_embedding import embed_sentences as embed_sentences_with_openai
from lab11_12 import button_add_display, button_search_display, ChromaStorage, FAISSStorage

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

embed_with_nltk, embed_with_hf, embed_with_openai = embed_options = ("NLTK", "Hugging Face", "OpenAI")

def tab_content(
        title:str = "No Title", 
        uploader_title:str = "No Uploader Title", 
        uploader_type:list = [],
        to_text_function:callable = None,
        segment_name: str = "Sentence",
        show_embedded: bool = True,
        is_image_content: bool = False,
        ):
    
    embed_function = ''
    if embed_option == embed_with_nltk:
        embed_function = embed_sentences_with_nltk
    elif embed_option == embed_with_openai:
        embed_function = embed_sentences_with_openai
    else:
        embed_function = embed_sentences_with_hugging_face
    
    st.title(title)

    uploaded_file = st.file_uploader(uploader_title, type=uploader_type)

    if uploaded_file:
        # Generating a unique filename
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Saving the file locally
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if is_image_content: 
            st.image(file_path)

        sentences = to_text_function(file_path)

        embedding_tab, vector_db_tab = st.tabs(["Embeddings", "Vector DB"])

        if show_embedded:
            with vector_db_tab:
                chroma_db, faiss = vector_db_options = ("ChromaDB", "FAISS")
                vector_db_option = st.selectbox("What Vector DB would you like to use?", vector_db_options, key=f"vector_db_selectbox_{title}")
                vector_db_storage =  ChromaStorage(name=title) if vector_db_option == chroma_db else FAISSStorage(name=title)
    
                st.subheader("You can:")
                st.write("1.Add the embedding to the Vector DB to be able search by this values later: ")
                button_add_display(vector_db_storage, sentences, file_path, origin_file_name=uploaded_file.name)
                st.write("2.Search the similarity of the embedding with the existing data in the Vector DB: ")
                button_search_display(vector_db_storage, is_image_content=is_image_content, query_texts=sentences)

        with embedding_tab:
            st.header('Result: ')
            for i, sentence in enumerate(sentences):
                st.write(f"**{segment_name}_{i}:** {sentence}")
                if show_embedded:
                    st.write("**Embeded**:")
                    embeded = embed_function([sentence])
                    if 'error' in embeded:
                        st.error(embeded['error'])
                        break
                    else:
                        st.write(embeded)

with st.expander("See explanation"):
    st.markdown('''
        Tokenize the text from PDF, Image, Docx, and XLS files. With the usage of:
        * **PDF:** fitz or PyMuPDF
        * **Image:** Pytesseract
        * **Docx:** Python-docx
        * **XLS:** openpyxl or Pandas

        Embed the tokenized text using:
        * **NLTK**
        * **Hugging Face**
            - sentence-transformers/all-MiniLM-L6-v2
            - sentence-transformers/paraphrase-multilingual-mpnet-base-v2
        * **OpenAI**
            * text-embedding-ada-002
        
        VectorDB usage:
        * **ChromaDB**
        * **FAISS**    
    ''')

st.title("Tokenization")
embed_option = st.selectbox("What embedding option you would like to use?", embed_options, key="embed_selectbox")

pdf_tab, image_tab, docx_tab, xls_tab = st.tabs(["PDF", "Image", "Docx", "XLS"])

with pdf_tab: 
    tab_content(title="PDF File Tokenization", 
                uploader_title="Upload a PDF file", 
                uploader_type=["pdf"],
                to_text_function=pdf_to_words,
                segment_name="Word")

with image_tab:
    tab_content(title="Image File Tokenization", 
                uploader_title="Upload an Image file", 
                uploader_type=["png", "jpg", "jpeg"],
                to_text_function=image_to_words,
                segment_name="Word",
                is_image_content=True)

with docx_tab:
    tab_content(title="Docx File Tokenization",
                uploader_title="Upload a Docx file",
                uploader_type=["docx"],
                to_text_function=doc_to_paragraphs)

with xls_tab:
    tab_content(title="XLS File Tokenization",
                uploader_title="Upload an XLS file",
                uploader_type=["xls", "xlsx"],
                to_text_function=extract_data_from_excel,
                segment_name="Row",
                show_embedded=False)
