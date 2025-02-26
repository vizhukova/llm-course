from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain

# Load the document
loader = WebBaseLoader("https://blog.langchain.dev/langchain-v0-1-0/") 
docs = loader.load()

# split the document into paragraphs
text_splitter = RecursiveCharacterTextSplitter()
# print(docs)
documents = text_splitter.split_documents(docs)

# emebed the documents
embeddings = HuggingFaceEmbeddings()

# Stor to faiss
vectorstore = FAISS.from_documents(documents, embeddings)

# print(vectorstore.similarity_search("What is Langchain?",k=2))

template = """"Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-3.5-turbo")

document_chain = create_stuff_documents_chain(llm,prompt)

retriever = vectorstore.as_retriever()
retrieval_chain = create_retrieval_chain(retriever,document_chain)
response = retrieval_chain.invoke({"input": "what is new in langchain 0.1.0"})
print(response['answer'])