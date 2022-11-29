import telegram
from Config import CHAT_ID, TELE_TOKEN
from TextBuilder import TextBuilder
from vnstocklib.StockChart import StockChart
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

'''
https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/
'''
class TelegramBot:
    def __init__(self, update:Update, context:CallbackContext) -> None:
        self.bot = telegram.Bot(token=TELE_TOKEN)
        self.update = update
        self.context = context
        self.imageUrl = f'https://vip.cophieu68.vn/imagechart/sma50/'

    def notify(self, userId,  message):
        chatId = userId
        self.bot.sendMessage(chat_id=chatId, text=message)

    def sendImageFromUrl(self, userId, symbol):
        message = f'{self.imageUrl}{symbol.lower()}.png'
        self.bot.sendMessage(chat_id=userId, text= message)
    
    def sendImageFromUrl(self, userId, img_url:str):
        self.bot.sendMessage(chat_id=userId, text= img_url)

    def reply(self, message):
        self.update.message.reply_text(f"{message}")        

#t = TelegramBot()
#t.notify(userId=CHAT_ID, message= 'Hello')
#t.sendImageFromUrl(userId=CHAT_ID, symbol='VND')

# chart = StockChart(symbol='VND')
# url = chart.imageUrl
# t.sendImageFromUrl(userId=CHAT_ID,img_url=url)