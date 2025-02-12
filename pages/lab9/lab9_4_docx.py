from docx import Document

def doc_to_paragraphs(doc_path):
    doc = Document(doc_path)
    return [para.text for para in doc.paragraphs]
        
def main():    
    doc_path = './content/little_raccoon_story.docx'   
    paragraphs = doc_to_paragraphs(doc_path)
    for i, para in enumerate(paragraphs):
            print(f"Paragraph {i}: ", para)

if __name__ == "__main__":
    main() 