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
from BotAnswer import BotAnswer
from Messages import *
from Notes import NoteDb
from Reports import get_stocks_by_suc_manh
from TextBuilder import TextBuilder
from TextCommand import *
from BotTranslator import BotTranslator
from Viewers import ViewOrders

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
	/!VND(100,10)
	/!VND(-100,10)
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
	
	msg_historyOrders = HistoryOrderMessage(input_text=input_text)
	if msg_historyOrders.isValid:		
		answer = msg_historyOrders.process()
		update.message.reply_text(answer)
		return
	
	msg_Alpha = AlphaMessage(input_text=input_text)
	if msg_Alpha.isValid:
		alpha = Alpha(input_text[1:].strip())
		answer = alpha.answerText
		update.message.reply_text(answer)
		alpha.addToNotes()
		return

	validCommands = ['BANKS','CK','VN30','BDS','ALL']
	if (input_text.upper() in validCommands):
		command = input_text.upper()
		stocks = db.getStocksByCommand(command=command)
		
		file_path =botAnswer.answer_stocks(stocks=stocks)
		update.message.reply_text(file_path)
		
	elif(input_text.upper() == '#LS'):
		view = ViewOrders()
		update.message.reply_text(text=view.to_tele_view())
		
	elif input_text.upper() == '#TODAY':
		print('Đang tìm cổ phiếu theo sức mạnh')
		df = get_stocks_by_suc_manh(input_text[1:].strip())
		update.message.reply_text(df.to_markdown(),parse_mode='Markdown')
	elif input_text.upper() == '#NOTES':
		print('Đang tìm cổ phiếu theo sức mạnh')
		db = NoteDb()
		update.message.reply_text(db.getAll().to_markdown())
	elif input_text.startswith('!'):
		if('(' in input_text and ')' in input_text):
			command = StockCommand(input_text[1:])
			print(command.to_string())
			command.order.save_to_db()
			update.message.reply_text(command.order.to_string(),parse_mode='Markdown')
		else:
			answer = BotTranslator(inputText = input_text[1:].strip()).transText
			update.message.reply_text(answer)
	
	elif((len(input_text) > 3) and (',' in input_text) and ('(') not in input_text):
		file_path = botAnswer.answer_stocks()
		update.message.reply_text(file_path)
	else:
		try:
			print('Đang xử lý')
			textOf_answer = botAnswer.answer()
			print(textOf_answer)			
			update.message.reply_text(TextBuilder(textOf_answer).text_markdown, parse_mode="Markdown")
		except:
			rs = parseTextCommand(input_text)			
			if rs == "":
				update.message.reply_text(
					"Sorry I can't recognize you , you said '%s'" % update.message.text)
			else:
				update.message.reply_text(rs)

def main():
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('help', help))
	updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
	updater.dispatcher.add_handler(CommandHandler('news', news_handler))		
	updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands
	# Filters out unknown messages.
	updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))	
	updater.start_polling(timeout=60)

main()

