from QuestionClassifier import QuestionClassifier
from OpenAIGenerator import OpenAIGenerator
from pymongo import MongoClient
from translate import Translator

class Question:
    def __init__(self, question):
        self.question = question

        # Phân loại lĩnh vực của câu hỏi
        self.field = QuestionClassifier().classify(question)

        # Khởi tạo đối tượng OpenAIGenerator
        self.generator = OpenAIGenerator(api_key='your_api_key')

        # Khởi tạo kết nối đến cơ sở dữ liệu MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['openai_database']
        self.collection = self.db['openai_collection']

    def generate_answer(self):
        # Tạo câu hỏi dạng tiếng Anh
        question_en = self.translate_text(self.question)

        # Sử dụng OpenAIGenerator để sinh câu trả lời
        answer = self.generator.generate_answer(question_en)

        # Lưu câu hỏi và câu trả lời vào cơ sở dữ liệu
        self.save_to_database(question_en, answer)

        # Trả về câu trả lời
        return answer

    def translate_text(self, text):
        # Hàm dịch đoạn văn bản sang tiếng Anh
        # Được sử dụng để chuyển câu hỏi sang tiếng Anh trước khi đưa vào OpenAIGenerator
        translator = Translator(to_lang='en', from_lang='vi')
        return translator.translate(text)

    def save_to_database(self, question, answer):
        # Lưu câu hỏi và câu trả lời vào cơ sở dữ liệu
        data = {"question": question, "answer": answer}
        self.collection.insert_one(data)
