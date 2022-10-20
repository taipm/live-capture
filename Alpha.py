from Parameters import *
from wolframalpha import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

client = Client(ALPHA_APP_ID)


intput = "2+3"
res = client.query(input=intput)

# Includes only text from the response
answer = next(res.results).text
  
print(answer)
