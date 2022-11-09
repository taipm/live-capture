from pathlib import Path
from time import sleep
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from FinanceStock import FinanceStock
from DateHelper import*
from apscheduler.schedulers.background import BlockingScheduler
import telegram
from BotAnswer import BotAnswer
from Reports import get_stocks_by_suc_manh
from TextCommand import *
from BotTranslator import BotTranslator
from Viewers import ViewOrders

TELE_TOKEN = '5505330729:AAGxQSLBn-J22Aj9gPD30CT0ah13LPlwhBo'
CHAT_ID = '1133501778'

#updater = Updater(TELE_TOKEN, use_context=True)
updater = Updater(TELE_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/VND - Trả về thông tin cổ phiếu VND (phục vụ giao dịch)
	/#BDS (#CK, #BANKS, ...) - Trả về thông tin các nhóm ngành
	/! - Dịch
	/? - Wolframe Alpha
	/geeks - To get the GeeksforGeeks URL""")

def geeks_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"GeeksforGeeks URL => https://www.geeksforgeeks.org/")


def news_handler(update: Update, context: CallbackContext):
	try:
		text = ""#getNews_wallstreet()
		update.message.reply_text(text=text)
	except:
		update.message.reply_text("Không được đọc chữ")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
	input_text = toStandard(update.message.text)
	botAnswer = BotAnswer(input_text)

	if(input_text.upper() == 'BANKS'):
		text_command = db.get_banks_symbols_command()
		botAnswer = BotAnswer(text_command)
		file_path = botAnswer.answer_stocks()
		update.message.reply_text(file_path)
	
	elif(input_text.upper() == 'CK'):
		text_command = db.get_securities_symbols()
		botAnswer = BotAnswer(text_command)
		file_path = botAnswer.answer_stocks()
		update.message.reply_text(file_path)

	elif(input_text.upper() == 'VN30'):
		text_command = db.get_banks_symbols()
		botAnswer = BotAnswer(text_command)
		file_path = botAnswer.answer_stocks()
		update.message.reply_text(file_path)

	elif('?' in input_text):
		answer = Alpha(input_text[1:].strip()).answerText
		update.message.reply_text(answer)

	elif('#today' in input_text):
		print('Đang tìm cổ phiếu theo sức mạnh')
		df = get_stocks_by_suc_manh(input_text[1:].strip())
		update.message.reply_text(df.to_markdown(),parse_mode='Markdown')

	elif('(' in input_text and ')' in input_text):
		#Is Buy/Sell stock
		print('Đang kiểm tra và xử lý lệnh mua/bán')
		command = None
		if(input_text.startswith('!')):		
			command = StockCommand(input_text[1:])
			command.order.save_to_db()			
		else:
			command = StockCommand(input_text)
			print(command.command)
		update.message.reply_text(command.order.to_string(),parse_mode='Markdown')

	elif('!' in input_text):		
		answer = BotTranslator(inputText = input_text[1:].strip()).transText
		update.message.reply_text(answer)

	elif((len(input_text) > 3) and (',' in input_text) and ('(') not in input_text):
		file_path = botAnswer.answer_stocks()
		update.message.reply_text(file_path)

	elif(input_text.lower() == '#ls'):
		view = ViewOrders()
		update.message.reply_text(text=view.df_view.to_markdown())
	else:
		try:
			print('Đang xử lý')
			textOf_answer = botAnswer.answer()
			print(textOf_answer)
			#update.message.reply_text(textOf_answer)
			update.message.reply_text(TextBuilder(textOf_answer).text_markdown, parse_mode="Markdown")
		except:
			rs = parseTextCommand(input_text)
			
			if rs == "":
				update.message.reply_text(
					"Sorry I can't recognize you , you said '%s'" % update.message.text)
			else:
				update.message.reply_text(rs)

def notify_ending(message):
	
	bot = telegram.Bot(token=TELE_TOKEN)
	rs = bot.sendMessage(chat_id=CHAT_ID, text=message)
	print(rs)

# notify_ending(message="Hello, teo")
# # Creates a default Background Scheduler


# def prompt():
# 	notify_ending(message="Tự động đây")
 
# prompt()



def main():
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('help', help))
	updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
	updater.dispatcher.add_handler(CommandHandler('news', news_handler))		
	updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands
	# Filters out unknown messages.
	updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
	
	#updater.start_polling(timeout=600)
	#updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
	#updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
	updater.start_polling(timeout=60)

	#sched = BlockingScheduler()
	#sched.add_job(prompt,'interval', seconds=15) 
	#sched.start()

main()

