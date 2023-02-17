from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class QuestionClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.topics = ['math', 'history', 'science', 'literature']
        
        self.train_data = pd.DataFrame({
            'question': ['What is the sum of 2 and 2?', 'When was the Declaration of Independence signed?', 'What is the scientific method?', 'Who wrote the novel To Kill a Mockingbird?'],
            'topic': ['math', 'history', 'science', 'literature']
        })
        
        X_train = self.vectorizer.fit_transform(self.train_data['question'])
        y_train = self.train_data['topic']
        self.classifier.fit(X_train, y_train)

    def classify(self, question):
        X_test = self.vectorizer.transform([question])
        y_pred = self.classifier.predict(X_test)[0]
        if y_pred in self.topics:
            return y_pred
        else:
            return 'other'


# Khởi tạo một đối tượng QuestionClassifier
question_classifier = QuestionClassifier()

# Bộ câu hỏi kiểm tra
test_questions = [    "Who discovered gravity?",    "What is the capital of France?",    "What is the square root of 144?",    "Who wrote the novel 'To Kill a Mockingbird'?",    "What is the formula for calculating work done?",    "What is the largest mammal on earth?",    "What year did the United States declare independence from Great Britain?",    "What is the difference between an alligator and a crocodile?",    "Who painted the Mona Lisa?",    "What is the chemical symbol for gold?"]

# Kiểm tra từng câu hỏi thuộc lĩnh vực nào
for question in test_questions:
    field = question_classifier.classify(question)
    print(f"Question: {question}\nField: {field}\n")
