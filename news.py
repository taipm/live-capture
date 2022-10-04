from cgitb import text
from time import sleep
from selenium import webdriver
from PIL import Image
from logging import error
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome(executable_path = '/Users/taipm/Documents/GitHub/live-capture/drivers/chromedriver')

while True:
    url = "https://www.vnwallstreet.com/#/home"
    driver.get(url)
    sleep(10)
    #wait the ready state to be complete
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )

    text = driver.find_element_by_class_name("article-container-box").text
    print(text)
    sleep(60*1)
