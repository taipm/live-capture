import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open('2.png'),lang='vie')
print(text)