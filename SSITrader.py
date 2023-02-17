from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class SSITrader:
    def __init__(self, userName:str,pwd:str) -> None:
        self.name = 'SSI-Trader'
        self.userName = '069909'#userName
        self.pwd = 'P@$$w0rdPMT123'#pwd
        self.url = 'https://webtrading.ssi.com.vn/Logon'
        self.driver = webdriver.Chrome("drivers/chromedriver")# head to github login page
        self.sleep_time = 10

    def login(self):
        # Github credentials
        username = self.userName
        password = self.pwd

        # initialize the Chrome driver
        
        self.driver.get("https://webtrading.ssi.com.vn/Logon")
        # find username/email field and send the username itself to the input field
        self.driver.find_element_by_id("name").send_keys(username)
        self.sleep()
        # find password input field and insert password as well
        self.driver.find_element_by_id("txtPassword").send_keys(password)
        self.sleep()
        # click login button
        self.driver.find_element_by_id("btnLogin").click()
        self.sleep()
        #self.gotoAssets()
        self.excute_buy_command()
        self.sleep()
        
    def gotoAssets(self):
        url = 'https://webtrading.ssi.com.vn/#Portfolio_ListProperties'
        self.driver.get(url=url)
        self.sleep()
        e = self.driver.find_element_by_id('trbankBalance')
        balance = e.text
        print(f'Balance: {balance}')
        self.sleep()
        self.logout()

    def logout(self):
        print(f'Exiting ...')
        self.sleep()
        self.driver.close()

    def excute_buy_command(self):
        id_btn_buy = 'PlaceOrderBuy'
        url = 'https://webtrading.ssi.com.vn/#Portfolio_ListProperties'
        if self.driver.current_url != url:
            self.driver.get(url=url)
        self.sleep()
        e = self.driver.find_element_by_id('trbankBalance')
        balance = float(e.text.split(' ')[1].replace('.',''))
        if balance > 0:
            print(f'Balance: {balance}')
            btn_buy = self.driver.find_element_by_id(id_=id_btn_buy).click()
            self.sleep()
            txt_symbol = self.driver.find_element_by_id(id_='txtStockSymbol')
            txt_symbol.send_keys('VND')
            self.sleep()
            txt_volume = self.driver.find_element_by_id(id_='txtOrderUnits')
            txt_volume.send_keys(100)
            self.sleep()
            txt_volume = self.driver.find_element_by_id(id_='txtOrderPrice')
            txt_volume.send_keys('MP')
            #txtSecureCode
            self.sleep()
            txt_volume = self.driver.find_element_by_id(id_='txtSecureCode')
            txt_volume.send_keys('P@$$w0rdPMT')
            self.sleep()
            #btnOrder
            btnOrder = self.driver.find_element_by_id(id_='btnOrder').click()
            self.sleep()

            btnOK = self.driver.find_element_by_id(id_='popup_ok').click()
            self.sleep()
            #POPUP
            #popup_content
            #popup_ok
            #popup_panel

            self.sleep()
            self.logout()

    def sleep(self):
        sleep(randint(self.sleep_time,self.sleep_time+5))

    def Sell(self):
        pass

    def getOrders(self):
        pass


s = SSITrader(userName='',pwd='')
s.login()