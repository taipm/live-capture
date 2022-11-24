from translate import Translator

class BotTranslator:
    def __init__(self, inputText) -> None:
        self.inputText = inputText        
        self.length = len(self.inputText)
        self.length_limit = 500
        self.transText = self.translate()

    def translate(self):
        if(self.length > self.length_limit):
            return 'Quá dài. Vui lòng chia nhỏ đoạn văn'
        else:
            translator = Translator(to_lang="en",from_lang='vi')
            text = translator.translate(self.inputText)
            if text.lower() == self.inputText.lower():
                translator = Translator(to_lang="vi",from_lang='en')
                text = translator.translate(self.inputText)
            return text