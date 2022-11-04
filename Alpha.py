from Parameters import *
from wolframalpha import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

client = Client(ALPHA_APP_ID)

class Alpha:
    def __init__(self, query) -> None:
        self.query = query.strip()
        self.result = self.answer()

    def answer(self):        
        res = client.query(input=self.query)
        return next(res.results).text

# Includes only text from the response
#answer = next(res.results).text
  
#print(answer)
# a = Alpha("1+1")
# print(a.result)