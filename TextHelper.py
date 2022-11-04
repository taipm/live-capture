def to_standard(text):
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

# text = 'a  b c  d'
# print(text)
# print(to_standard(text=text))