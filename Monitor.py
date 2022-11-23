from pathlib import Path
from time import sleep
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from Config import *
from DateHelper import *
from apscheduler.schedulers.background import BlockingScheduler
import telegram
from IntradayData import AnalysisIntradayData
from TextCommand import *
from datetime import datetime

#https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html
class StockTime:
    def __init__(self) -> None:
        self.currentTime = datetime.now()
        
    @property
    def startTime(self):
        start_hour = 9
        start_minute = 0
        start_second = 0        
        year = TODAY.year
        month = TODAY.month
        day = TODAY.day
        return datetime(year,month,day,start_hour,start_minute,start_second)
    
    @property
    def endTime(self):
        end_hour = 15
        end_minute = 0
        end_second = 0
        year = TODAY.year
        month = TODAY.month
        day = TODAY.day
        return datetime(year,month,day,end_hour,end_minute,end_second)

    @property
    def endOfMorningTime(self):
        end_hour = 11
        end_minute = 30
        end_second = 0
        year = TODAY.year
        month = TODAY.month
        day = TODAY.day
        return datetime(year,month,day,end_hour,end_minute,end_second)
    
    @property
    def startOfAfternoonTime(self):
        start_hour = 13
        start_minute = 00
        start_second = 0
        year = TODAY.year
        month = TODAY.month
        day = TODAY.day
        return datetime(year,month,day,start_hour,start_minute,start_second)
    

    def isTradingTime(self):        
        print(self.currentTime)
        if (self.currentTime >= self.startTime and self.currentTime <= self.endOfMorningTime) or (self.currentTime >= self.startOfAfternoonTime and self.currentTime <= self.endTime):
            print('Trong giờ')
            return True
        else:
            print('Ngoài giờ')
            return False

    def __str__(self) -> str:
        return f'Start: {self.startTime} - End: {self.endTime} : Now: {self.currentTime} : {self.isTradingTime()}'
class Monitor:
    def __init__(self) -> None:        
        self.updater = Updater(TELE_TOKEN, use_context=True)
        self.sched = BlockingScheduler()        
    
    def start(self):        
        self.sched.start()
        

    def stop(self):
        self.sched.shutdown()

    def notify_ending(self, message):
        bot = telegram.Bot(token=TELE_TOKEN)
        rs = bot.sendMessage(chat_id=CHAT_ID, text=message)
        print(rs)
        
    def get_intraday(self,symbol):
        output = AnalysisIntradayData(symbol=symbol).GetSummary()
        return output

    def scheduled_job(self):
        #self.sched.add_job(self.scheduled_job, 'cron', day_of_week='mon-sat', hour='23', minute='22-24', second='30')
        self.sched.add_job(self.scheduled_job, 'cron', day_of_week='mon-sat', hour='13-15', minute='0-59', second='00')
        self.state = StockTime()
        if self.state.isTradingTime():
            text = self.get_intraday(symbol='HAX')
            self.notify_ending(message=text)
        #self.sched.scheduled_job(self.prompt, 'interval', day_of_week='mon-sat', hour=24,seconds=2)
     
m = Monitor()
m.scheduled_job()
m.start()

# def Test_StockTime():
#     t = StockTime()
#     print(t)

# Test_StockTime()