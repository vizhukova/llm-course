import re
import streamlit as st
import chromadb
chroma_client = chromadb.Client()

class VectorDBStorage():
    def __init__(self, name:str):
        self.len = 0
        re_name = re.sub(r'\s+', '_', name.strip()).lower()
        self.collection = chroma_client.get_or_create_collection(name=re_name)

    @property
    def get_name(self):
        return self.collection.name

    def add_data(self, documents:list[str], document_url:str = ""):
        print(self.collection)
        ids = []
        metadatas = []

        for i, _ in enumerate(documents):
            ids.append(f"id{i + self.len}")
            metadatas.append({"document_url": document_url})

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        self.len += len(documents)

    def search_similarity(self, query_texts:list[str], n_results:int = 2):
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )

def main():
    collection = VectorDBStorage(name="Genai dataset")
    collection.add_data([
        "Apple", 
        "Orange",
        "King",
        "Queen"
    ])
    results = collection.search_similarity(["emotional"])
    print(results)

if __name__ == "__main__":
    main()

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
            for i, metadata in enumerate(results['metadatas'][0]):
                st.image(metadata['document_url'], caption=results['documents'][0][i])

        st.subheader("Results:")
        st.write(results)
