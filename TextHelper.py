def toStandard(text):
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    while '\n\n' in text:
        text = text.replace('\n\n', '\n')
    return text




