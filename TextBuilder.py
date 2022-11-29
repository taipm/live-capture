from TextHelper import toStandard

class Word:
    Punctuations = ['.',',',';','!',':','?']
    def __init__(self, word, index) -> object:
            self.text = word
            self.index = index
    @property
    def is_punctuation(self):
            if self.text in self.Punctuations:
                return True
            else:
                return False
    @property
    def is_number(self):
            if (self.text.isnumeric()):
                return True
            else:
                return False
    def __str__(self):
            return f'{self.text} [{self.index}] Number: {self.is_number} Punctuation: {self.is_punctuation}'

class TextBuilder:
    def __init__(self, text) -> None:
        self.text = toStandard(text=text)
        self.words = self.getWords()
        self.len = len(self.words)
        self.start = self.words[0]
        self.end = self.words[self.len-1]
        self.text_markdown = self.to_markdown_v2()
    
    def getWords(self):
        items = self.text.split(' ')
        words = []
        i = 0
        for item in items:
            words.append(Word(item,i))
            i+=1
        return words
    
    def __str__(self) -> str:         
        output = ''
        for word in self.words:
            output += ' ' + word.text
        return output
    
    def to_markdown_v2(self):
        output = ''
        for word in self.words:
            if word.is_number:
                word.text = f'*{word.text}*'
            output += f'{word.text} '
        print(output)
        return output.strip()