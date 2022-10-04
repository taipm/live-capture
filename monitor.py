# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def getHtml(url):
    url = Request('https://cafef.vn/chien-luoc-dau-tu-it-ton-kem-cua-ty-phu-warren-buffett-ma-ai-cung-co-the-thu-20221004140509334.chn',
			headers={'User-Agent': 'Mozilla/5.0'})

    # to perform a GET request and load the
    # content of the website and store it in a var
    response = urlopen(url).read()
    return response

print(getHtml(""))

# # setting the URL you want to monitor
# url = Request('https://www.vnwallstreet.com/#/home',
# 			headers={'User-Agent': 'Mozilla/5.0'})

# # to perform a GET request and load the
# # content of the website and store it in a var
# response = urlopen(url).read()

# # to create the initial hash
# currentHash = hashlib.sha224(response).hexdigest()
# print("running")
# time.sleep(10)
# while True:
# 	try:
# 		# perform the get request and store it in a var
# 		response = urlopen(url).read()
# 		first_text = response.
# 		# create a hash
# 		currentHash = hashlib.sha224(response).hexdigest()
		
# 		# wait for 30 seconds
# 		time.sleep(30)
		
# 		# perform the get request
# 		response = urlopen(url).read()
		
# 		# create a new hash
# 		newHash = hashlib.sha224(response).hexdigest()

# 		# check if new hash is same as the previous hash
# 		if newHash == currentHash:
# 			continue

# 		# if something changed in the hashes
# 		else:
# 			# notify
# 			print("something changed")

# 			# again read the website
# 			response = urlopen(url).read()

# 			# create a hash
# 			currentHash = hashlib.sha224(response).hexdigest()

# 			# wait for 30 seconds
# 			time.sleep(30)
# 			continue
			
# 	# To handle exceptions
# 	except Exception as e:
# 		print("error")
