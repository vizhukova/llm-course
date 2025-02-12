import fitz # PyMuPDF
import re

def pdf_to_words(pdf_path):
  words = []
  with fitz.open(pdf_path) as pdf_document:
    for page_number in range(pdf_document.page_count):
      page = pdf_document[page_number]
      text = page.get_text()
      words.extend(re.findall(r'\b\w+\b', text))
  return words

def main():
  pdf_path = './content/little_bear_story.pdf'
  result = pdf_to_words(pdf_path)
  print(len(result), result)

if __name__ == "__main__":
    main() 