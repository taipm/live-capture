from TextHelper import toStandard


class DbObject:
    def __init__(self) -> None:
        pass

class Note(DbObject):
    def __init__(self, text) -> None:
        super().__init__()
        self.text = toStandard(text)

    def save(self):
        pass
    
