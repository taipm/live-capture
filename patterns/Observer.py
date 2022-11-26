from abc import ABC, abstractmethod

'''
https://python.plainenglish.io/design-patterns-in-python-observer-pattern-3d65307ab46a
'''
class IObservable(ABC):
    
    @abstractmethod
    def subscribe(self, observer):
        """subscription"""
    
    @abstractmethod
    def unsubscribe(self, observer):
        """unsubscription"""
        
    @abstractmethod
    def update(self, message):
        """update method"""
        
class Reuters(IObservable):
    
    def __init__(self):
        self._subscribers = set()
    
    def subscribe(self, observer):
        self._subscribers.add(observer)
        return
    
    def unsubscribe(self, observer):
        self._subscribers.remove(observer)
        return
    
    def update(self, message):
        for observer in self._subscribers:
            observer.update(message)
            
class IObserver(ABC):
    
    @abstractmethod
    def update(self, message):
        """"""
        
class Cnn(IObserver):
    
    def update(self, message):
        print("Breaking News: ", message)
        return

class Fox(IObserver):
    
    def update(self, message):
        print("The Ultimate Breaking News: ", message)
        
class Archiever(IObserver):
    
    def __init__(self):
        self.db = []
    
    def update(self, message):
        self._add_archieve(message)
        print(f"{message} is added to database.")
        
    def _add_archieve(self,message):
        self.db.append(message)
        return

R = Reuters()
C = Cnn()
F = Fox()
A = Archiever()
R.subscribe(C)
R.subscribe(F)
R.subscribe(A)
R.update("Zelon Tusk bought Boeing")