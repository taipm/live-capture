from translate import Translator

class BotTranslator:
    def __init__(self, inputText) -> None:
        self.inputText = inputText        
        self.transText = self.translate()
        self.length = len(self.inputText)
        self.length_limit = 500

    def translate(self):
        if(self.length > self.length_limit):
            return 'Quá dài. Vui lòng chia nhỏ đoạn văn'
        else:
            translator = Translator(to_lang="en",from_lang='vi')
            text = translator.translate(self.inputText)
            return text
    
    def detectLang(self):
        pass



# t = BotTranslator(inputText="Xin chào")
# print(t.transText)
