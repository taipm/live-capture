import pytesseract
from PIL import Image

def getTextFromImage(fileName):
    text = pytesseract.image_to_string(Image.open(fileName),lang='vie')
    print(text)
    return text

text = getTextFromImage("1.png")
print(text)