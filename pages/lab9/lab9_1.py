import fitz # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab')

def extract_text_from_pdf(pdf_path):
  doc = fitz.open(pdf_path)
  text = ""
  for page_num in range(doc.page_count):
    page = doc[page_num]
    text += page.get_text()
  doc.close()
  return text

def split_into_sentences(text):
  sentences = sent_tokenize(text)
  return sentences

def main():
    pdf_path = './content/little_bear_story.pdf'
    text = extract_text_from_pdf(pdf_path)
    sentences = split_into_sentences(text)

    for i, sentence in enumerate(sentences, 1):
        print(f"Sentence {i}: {sentence}")

if __name__ == "__main__":
    main() 