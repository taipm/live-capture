
import pandas as pd
import openai
import spacy
from translate import Translator
from pymongo import MongoClient
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from OpenAIGenerator import OpenAIGenerator

# db = client["TradingBook"]
# task_collection = db["tasks"]

class MongoDB:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb+srv://taipm:OAMOHMEC8CPUHoz2@cluster0.nskndlz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        result_id = self.collection.insert_one(data).inserted_id
        print("Result saved with id:", result_id)

    def find(self, query):
        return list(self.collection.find(query))




# Define the MongoDB connection details
mongo = MongoDB('OpenAI', 'results')

# Create an instance of the OpenAIGenerator class
api_key = "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"
generator = OpenAIGenerator(api_key, mongo)

question = "What is the meaning of life?"
answer = generator.generate_answer(question)

# Print the answer
print(answer)

# Find all results in the MongoDB collection
results = mongo.find({})
for result in results:
    print(result)
