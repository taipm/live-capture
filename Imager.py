import os
import pytesseract
from PIL import Image

from watcher import get_last_image

def getTextFromImage(filePath):
    print(filePath)
    fileName = os.path.basename(filePath)
    print(fileName)
    text = pytesseract.image_to_string(Image.open(fileName),lang='vie')
    print(text)
    return text

# text = getTextFromImage("luong.png")
# print(text)

last_img = get_last_image(".")
print(last_img)
text = getTextFromImage(last_img)
print(text)


text = getTextFromImage('file_11.jpg')
print(text)
