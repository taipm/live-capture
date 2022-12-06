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
    
    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

class MongoDb:
    def __init__(self, name) -> None:
        client = MongoClient("mongodb+srv://taipm:mNIZQSFNRm4XMLhs@cluster0.nskndlz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        self.db = client['TradingBook']
        self.name = name
        self.collection = self.db.get_collection(name=name)

    def addItem(self, item:ObjectDb):
        print(f'addItem: {item}')
        self.collection.insert_one(json.loads(item.to_json()))

    def getAll(self):
        items = self.collection.find()        
        df =  pd.DataFrame(list(items))
        return df

    def deleteAll(self):
        self.collection.delete_many({})

    def getItemsOfToday(self):
        df = self.getAll()
        if not df.empty:
            df = df[df['time'].map(lambda x: isToday(x)==True)]
            df = df.sort_values(by=['time'])
        return df
    def deleteItemsOfToday(self):
        items = self.getItemsOfToday()
        for i in range(0, len(items)):
            item = items.iloc[i]
            del_query = {'time':item['time']}
            self.collection.delete_one(del_query)
            
    def __str__(self):
        return f'TradingBook\n - {self.name}'