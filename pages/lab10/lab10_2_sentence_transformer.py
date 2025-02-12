from sentence_transformers import SentenceTransformer
from env import HUGGING_FACE_TOKEN

def embed_sentences(sentences: list[str]):
    try:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', token=HUGGING_FACE_TOKEN)
        # model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2', token=HUGGING_FACE_TOKEN)
        embeddings = model.encode(sentences)
        return embeddings
    except Exception as e:
        return {"error": str(e)}

def main():
    sentences = ["This is an example sentence", "Each sentence is converted"]
    embeddings = embed_sentences(sentences)

    for sentence, embedding in zip(sentences, embeddings):
        embedding_array_string = '[' + ','.join(map(str, embedding)) + ']'
        ##print(f"Sentence: {sentence}")
        ##print(f"Embedding: {embedding_array_string}")
        print(embedding_array_string)

if __name__ == "__main__":
    main() 