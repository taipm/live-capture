#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from pymongo import MongoClient
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class MongoDb:
    def __init__(self) -> None:
        client = MongoClient("mongodb+srv://taipm:mNIZQSFNRm4XMLhs@cluster0.nskndlz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        self.db = client['TradingBook']
        self.collections = self.db.list_collection_names()

    def to_string(self):        
        print(f'{self.db.name}')
        print(f'{self.collections}')