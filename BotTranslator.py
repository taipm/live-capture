from translate import Translator
import langdetect

class BotTranslator:
    def __init__(self, inputText) -> None:
        self.inputText = inputText
        self.src_lang = langdetect.detect(self.inputText)
        self.length = len(self.inputText)
        self.length_limit = 500
        self.transText = self.translate()

    def translate(self):
        if(self.length > self.length_limit):
            return 'Quá dài. Vui lòng chia nhỏ đoạn văn'
        else:
            print(f'{self.inputText} : {self.src_lang}')
            text = ''
            if self.src_lang == 'vi':
                translator = Translator(to_lang="en",from_lang='vi')
                text = translator.translate(self.inputText)
            else:
                translator = Translator(to_lang="vi")
                text = translator.translate(self.inputText)
            print(f"Src: {translator.from_lang} (Dest: {translator.to_lang}) --> {self.inputText} ({text})")
            return text