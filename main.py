from selenium import webdriver
from PIL import Image
driver = webdriver.Chrome(executable_path = '/Users/taipm/Documents/GitHub/live-capture/drivers/chromedriver')
url = "https://www.google.com/"
driver.get(url)
driver.save_screenshot('ss.png')
screenshot = Image.open('ss.png')
screenshot.show()


# #coding=utf-8                                                                                                                                                                              
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


# options = webdriver.ChromeOptions()
# options.headless = True
# driver = webdriver.Chrome(options=options)

# URL = 'https://pythonbasics.org'

# driver.get(URL)

# S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
# driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
# driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')

# driver.quit()