from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import numpy as np

nltk.download('punkt')

def embed_sentences(sentences: list[str]):

    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]

    # print(tokenized_sentences)

    model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)

    embeddings = []
    for sentence in tokenized_sentences:
        word_embedding = model.wv[sentence]

        embeddings.append(np.array2string(word_embedding, separator=',', precision=6, suppress_small=True))

    return embeddings

def main():
    sentences = [
        "virat kohli" , "ronaldo" , "cricket" , "football"
    ]

    embedded = embed_sentences(sentences)
    for i, sentence in enumerate(embedded, 1):
        print(f"Sentence {i}: {sentence}")

if __name__ == "__main__":
    main() 