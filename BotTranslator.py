from translate import Translator
import langdetect

class BotTranslator:
    def __init__(self, inputText) -> None:
        self.inputText = inputText        
        self.length = len(self.inputText)
        self.length_limit = 500
        self.transText = self.translate()

    def translate(self):
        if(self.length > self.length_limit):
            return 'Quá dài. Vui lòng chia nhỏ đoạn văn'
        src_lang = langdetect.detect(self.inputText)
        text = ''
        if src_lang == 'vi':
            translator = Translator(to_lang="en",from_lang='vi')
            text = translator.translate(self.inputText)
        elif src_lang == 'en':
            translator = Translator(to_lang="vi",from_lang='en')
            text = translator.translate(self.inputText)
        else:
            print(f'src_lang: {src_lang} - Chưa dịch')
        return text