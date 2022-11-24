import json
from TextHelper import toStandard
from MongoDb import MongoDb, ObjectDb
from dataclasses import dataclass

class NoteDb(MongoDb):
    def __init__(self) -> None:
        super().__init__(name='Notes')
    
class Note(ObjectDb):
    def __init__(self, text) -> None:
        super().__init__()
        self.text = toStandard(text)
    
    def __str__(self) -> str:
        return super().__str__()

    def to_json(self):
        return json.dumps(self,default=lambda o: o.__dict__)

def Test():
    db = NoteDb()
    note = Note(text='Đây là note thứ 2')
    db.addItem(note.to_json())
    print(db.getAll())
    print(db.getItemsOfToday())

#Test()