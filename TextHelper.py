def to_standard(text):
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    while '\n\n' in text:
        text = text.replace('\n\n', '\n')
    return text

#def to_markdown(text):

# text = 'a  b c  d'
# print(text)
# print(to_standard(text=text))
Punctuations = ['.',',',';','!',':','?']
class Word:
        def __init__(self, word, index) -> None:
            self.text = word
            self.index = index
        @property
        def is_punctuation(self):
            if self.text in Punctuations:
                return True
            else:
                return False
        @property
        def is_number(self):
            if (self.text.isnumeric()):
                return True
            else:
                return False
        def to_string(self):
            return f'{self.text} [{self.index}] Number: {self.is_number} Punctuation: {self.is_punctuation}'
class TextBuilder:
    def __init__(self, text) -> None:
        self.text = to_standard(text=text)
        self.len = len(self.words)
        self.start = self.words[0]
        self.end = self.words[self.len-1]
        self.text_markdown = self.to_markdown_v2()

    @property
    def words(self):
        items = self.text.split(' ')
        words = []
        i = 0
        for item in items:
            words.append(Word(item,i))
            i+=1
        return words

    def to_string(self):
        for word in self.words:
            print(word.to_string())
    
    def to_markdown_v2(self):
        output = ''
        for word in self.words:
            if word.is_number:
                word.text = f'*{word.text}*'
            output += f'{word.text} '
        print(output)
        return output.strip()


# b = TextBuilder('Hello, how are you ?. Thanks. I"m 20 years old')
# print(b.text_markdown)
# b.to_string()
