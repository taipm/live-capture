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
import zoneinfo
from datetime import datetime

NYC = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")
#https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html

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
        self.sched.add_job(self.scheduled_job, 'cron', hour='23', minute='22-24', second='30')
        text = self.get_intraday(symbol='HAX')
        self.notify_ending(message=text)
        #self.sched.scheduled_job(self.prompt, 'interval', day_of_week='mon-sat', hour=24,seconds=2)
     
m = Monitor()
m.scheduled_job()
m.start()