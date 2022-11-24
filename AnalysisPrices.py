from AnalysisList import AnalysisList

class AnalysisPrice(AnalysisList):
    def __init__(self, lst: list) -> None:
        super().__init__(lst)
    
    def distance(self, from_index):
        value_of_index = self.items[from_index]
        print(value_of_index)
        return self.pct(value_of_index, self.items[0])