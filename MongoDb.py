#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json
import pandas as pd
from pymongo import MongoClient
from DateHelper import NOW, isToday
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class ObjectDb:
    def __init__(self) -> None:
        self.time = str(NOW)

    def __str__(self) -> str:
        return self.time

class MongoDb:
    def __init__(self, name) -> None:
        client = MongoClient("mongodb+srv://taipm:mNIZQSFNRm4XMLhs@cluster0.nskndlz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        self.db = client['TradingBook']
        self.name = name
        self.collection = self.db.get_collection(name=name)

    def addItem(self, item):
        self.collection.insert_one(json.loads(item))

    def getAll(self):
        items = self.collection.find()        
        df =  pd.DataFrame(list(items))
        return df

    def getItemsOfToday(self):
        df = self.getAll()
        df = df[df['time'].map(lambda x: isToday(x)==True)]
        df = df.sort_values(by=['time'])
        return df

    def __str__(self):
        return f'TradingBook\n - {self.name}'


def Test():
    db = MongoDb(name='Notes')
    print(db)
    print(db.getAll())
    print(db.getItemsOfToday())

#Test()