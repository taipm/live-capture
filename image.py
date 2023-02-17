# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Đường dẫn của hình ảnh và bảng dữ liệu
image_path = "/Users/taipm/Documents/GitHub/live-capture/Picture1.jpg"



import cv2
import pytesseract
import re

# Đường dẫn đến file ảnh cần nhận dạng
#img_path = "path/to/image.jpg"

# Đọc ảnh và chuyển sang ảnh xám để dễ dàng nhận dạng
# img = cv2.imread(image_path)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Nhận dạng chữ trong ảnh
# text = pytesseract.image_to_string(gray)
# print(text)
# # x = 0 #Tạo biến để lưu vị trí
# # y = 0

# # Tìm tọa độ của chữ đầu tiên bằng regular expression
# match = re.search(r"\b\w+\b", text)
# if match:
#     word = match.group()
#     x, y = match.start(), 0
#     print(f"Tọa độ của chữ '{word}' là: ({x}, {y})")
# else:
#     print("Không tìm thấy chữ nào trong ảnh")


# Mở hình ảnh và tạo đối tượng vẽ
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Thiết lập font chữ và kích thước
#font = ImageFont.load_default()
#font = ImageFont.truetype("path/to/myfont.ttf", size=16)
font = ImageFont.truetype("Arial.ttf", size=20)

# Vẽ bảng dữ liệu lên hình ảnh
x, y = image.size[0]/2, 100 # Tọa độ góc trái trên của bảng dữ liệu
padding = 10 # Khoảng cách giữa các ô

value = 'xin chào'
text_width, text_height = draw.textsize(value, font)
draw.text((x-text_width/2, y), str(value), font=font)

# Lưu hình ảnh mới
image.save("/Users/taipm/Documents/GitHub/live-capture/Picture2.jpg")


from PIL import Image, ImageDraw

# Load image
image = Image.open(image_path)

# Convert to grayscale
image = image.convert("L")

# Create a draw object
draw = ImageDraw.Draw(image)

# Find the bounding box of the character "T"
bbox = draw.textbbox((0, 0), "B")

# Calculate the position of the character "T" relative to the image
x = bbox[0] + bbox[2] / 2
y = bbox[1] + bbox[3] / 2

# Print the position of the character "T"
print("The position of the character T is ({}, {})".format(x, y))
