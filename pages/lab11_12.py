import os
import re
import streamlit as st
from uuid import uuid4
import chromadb
import faiss
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

FAISS_PATH = "./faiss_db"
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

class VectorDBStorage():
    def __init__(self, name:str):
        print(f'{name} initialized')
        self.collection_name = re.sub(r'\s+', '_', name.strip()).lower()

    @property
    def get_name(self):
        return self.collection_name

    def add_data(self, documents:list[str], document_url:str = ""):
        print('collection_name: ', self.collection_name)
        print('documents: ', documents)

    def search_similarity(self, query_texts:list[str], n_results:int = 2):
        print('collection_name: ', self.collection_name)
        print('query_texts: ', query_texts)

class ChromaStorage(VectorDBStorage):
    def __init__(self, name:str):
        super().__init__(name)
        self.collection = chroma_client.get_or_create_collection(name=self.collection_name)

    def add_data(self, documents:list[str], document_url:str = ""):
        super().add_data(documents, document_url)

        ids = []
        metadatas = []

        for document in documents:
            ids.append(str(uuid4()))
            metadatas.append({"document_url": document_url})

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def search_similarity(self, query_texts:list[str], n_results:int = 2):
        super().search_similarity(query_texts, n_results)
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )

        print('Similarity search results chroma:', results)

        return [{
            "document_url": metadata['document_url'],
            "document": results['documents'][0][i]
        } for i, metadata in enumerate(results['metadatas'][0])]

class FAISSStorage(VectorDBStorage):
    def __init__(self, name: str):
        super().__init__(name)

        self.FAISS_INDEX_PATH = f"./{FAISS_PATH}/faiss_index_{self.collection_name}"
        self.collection = self.load_or_create_faiss_index()    

    def load_or_create_faiss_index(self):
        if os.path.exists(f"{self.FAISS_INDEX_PATH}/index.faiss") and os.path.exists(f"{self.FAISS_INDEX_PATH}/index.pkl"):
            print("Loading existing FAISS index...")
            collection = FAISS.load_local(
                self.FAISS_INDEX_PATH,  
                embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print("Creating new FAISS index...")
            dimension = len(embeddings.embed_query("hello world"))  # Get embedding size
            index = faiss.IndexFlatL2(dimension)

            collection = FAISS(
                embedding_function=embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )

        return collection

    def save_index(self):
        os.makedirs(self.FAISS_INDEX_PATH, exist_ok=True)  
        self.collection.save_local(self.FAISS_INDEX_PATH)
        print("FAISS index saved successfully!")

    def add_data(self, documents: list[str], document_url: str = ""):
        super().add_data(documents, document_url)
        ids = [str(uuid4()) for _ in documents]
        doc_objects = [Document(page_content=doc, metadata={"document_url": document_url}) for doc in documents]

        self.collection.add_documents(documents=doc_objects, ids=ids)
        self.save_index()
        print(f"Added {len(documents)} documents to FAISS index '{self.collection_name}'")

    def search_similarity(self, query_texts: list[str], n_results: int = 2):
        super().search_similarity(query_texts, n_results)
        query_text = " ".join([txt for txt in query_texts])
        
        results = self.collection.similarity_search(
            query_text,
            k=n_results,
        )

        print('Similarity search results faiss:', results)

        return [{
            "document_url": res.metadata['document_url'],
            "document": res.page_content
        } for res in results]
    
def main():
    data = [
        "Apple", 
        "Orange",
        "King",
        "Queen"
    ]

    chroma_collection = ChromaStorage(name="Genai dataset")
    chroma_collection.add_data(data)
    chroma_results = chroma_collection.search_similarity(["animal"])
    print("Chroma result: ", chroma_results)

    faiss_collection = FAISSStorage(name="Genai dataset")
    faiss_collection.add_data(data)
    faiss_results = faiss_collection.search_similarity(["animal"])
    print("FAISS result: ", faiss_results)
    

if __name__ == "__main__":
    main()

# Streamlit part

def button_add_display(vector_db_storage: VectorDBStorage, documents:list[str], document_url:str, origin_file_name: str):
    if st.button("Add to the Dataset", key=f"add_to_db_{vector_db_storage.get_name}"):
        vector_db_storage.add_data(documents, document_url)
        st.success(f"Data Added from {origin_file_name}")

def button_search_display(vector_db_storage: VectorDBStorage, is_image_content:bool=False, query_texts: list[str]=[]):
    results = None
    n_results = st.slider("How much top result you want to see?", 1, 5, 2, key=f"n_results_{vector_db_storage.get_name}")
    
    if is_image_content:
        st.write("2.1.Search similarity by the uploaded image: ")
        if st.button("Search similar images", key=f"search_to_db_{vector_db_storage.get_name}_img"):
            results = vector_db_storage.search_similarity(query_texts, n_results)
    
    st.write("2.2.Search similarity by the provided text: ")
    query_text = st.text_input("Search text", key=f"search_text_{vector_db_storage.get_name}")
    if st.button("Search similarity", key=f"search_to_db_{vector_db_storage.get_name}"):
        results = vector_db_storage.search_similarity([query_text], n_results)

    if results:
        st.header("Found similarity:")
        
        if is_image_content:
            st.subheader("Images:")
            for res in results:
                if res['document_url']:
                    st.image(res['document_url'], caption=res['document'])
                else:
                    st.write(f"(No image url) caption: {res['document']}")

        st.subheader("Results:")
        st.write(results)
    elif results != None and not results:
        st.warning("Nothing has been found.")