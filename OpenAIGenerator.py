import pandas as pd
import openai
import spacy
from translate import Translator

def get_engine(question):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(question)
    if any(token.text.lower() in ['classify', 'categorize', 'group'] for token in doc):
        return "text-davinci-002"
    elif any(token.text.lower() in ['summarize', 'brief', 'short'] for token in doc):
        return "text-davinci-002"
    elif any(token.text.lower() in ['translate', 'conversion'] for token in doc):
        return "text-davinci-002"
    elif any(token.text.lower() in ['solve', 'calculate', 'compute'] for token in doc):
        return "text-davinci-003"
    elif any(token.text.lower() in ['create', 'build', 'design', 'generate'] for token in doc):
        return "davinci-codex"
    else:
        return "text-davinci-002"
        
class OpenAIGenerator:
    def __init__(self, api_key, mongo):
        self.api_key = api_key
        self.mongo = mongo

    def generate_answer(self, question):
        translator = Translator(to_lang='en',from_lang='vi')
        text = question
        question_en = translator.translate(text)
        print(question_en)
        engine = get_engine(question_en)

        openai.api_key = self.api_key
        completions = openai.Completion.create(
            engine=engine,
            prompt=question,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text

        # Save the query results to MongoDB
        result = {'engine': engine, 'question': question, 'answer': message}
        self.mongo.insert(result)

        result_df = pd.DataFrame(result, index=[0])
        return result_df