from env import OPENAI_API_KEY
from openai import OpenAI

def embed_sentences(sentences: list[str]):
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    embeddings = []
    for sentence in sentences:
      embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=sentence,
        encoding_format="float"
      )
      embeddings.append(embedding.data[0].embedding)
    
    return embeddings

def main(): 
   sentences = ["This is an example sentence", "Each sentence is converted"]
   print(embed_sentences(sentences))

if __name__ == "__main__":
    main() 