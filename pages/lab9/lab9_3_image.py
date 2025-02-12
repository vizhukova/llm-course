import nltk
from nltk.tokenize import word_tokenize
from PIL import Image
import pytesseract

def image_to_words(image_url):
    image_to_string = pytesseract.image_to_string(Image.open(image_url))
    return word_tokenize(image_to_string)

def main():
    image = './content/image_with_text.png'
    # image = './content/image_with_text_2.jpg' # returns nothing
    # image = './content/image_with_text_3.jpg' # returns nothing
    print(image_to_words(image))

if __name__ == "__main__":
    main() 