#https://docs.python-telegram-bot.org/en/stable/examples.echobot.html
from time import sleep
from telegram.ext import Updater, CallbackContext, CommandHandler,MessageHandler,Application
from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from Config import *
from DateHelper import *
from BotAnswer import BotAnswer
from Messages import *
from Notes import NoteDb
from StockChart import plot_candlestick_chart
from TelegramBot import TelegramBot
from db import *
from TextCommand import *
from BotTranslator import BotTranslator
from Viewers import ViewOrders
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

def start(update:Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")

def help(update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/VND - Trả về thông tin cổ phiếu VND (phục vụ giao dịch)
	/#BDS (#CK, #BANKS, ...) - Trả về thông tin các nhóm ngành
	/! - Dịch
	/!VND(100,10)
	/!VND(-100,10)
	/? - Wolframe Alpha
	""")

async def plot_graph(update:Update, context: ContextTypes.DEFAULT_TYPE):
	today = datetime.datetime.now()
	today_str = today.strftime("%Y-%m-%d")
	input_text = toStandard(update.message.text)
	if len(input_text) == 3:
		buf = plot_candlestick_chart(symbol=input_text.upper(),start_date='2022-06-01',end_date=today_str)   
		await update.effective_chat.send_photo(photo=buf)
	else:
		await update.message.reply_text(f"{input_text} is not stock symbol")


def unknown(update:Update, context: CallbackContext):
    update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)

def unknown_text(update:Update, context: CallbackContext):	
	bot = TelegramBot(update=update,context=context)

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
		stocks = getStocksByCommand(command=command)		
		file_path =botAnswer.answer_stocks(stocks=stocks)
		update.message.reply_text(file_path)
		
	elif(input_text.upper() == '#LS'):
		view = ViewOrders()
		update.message.reply_text(text=view.to_tele_view())
		
	elif input_text.upper() == '#TODAY':
		print(f'Đang xử lý lệnh: {input_text.upper()}')
		view = ViewOrders()
		update.message.reply_text(view.getTodayOrders().to_markdown())

	elif input_text.upper() == '#NOTES':
		db = NoteDb()
		update.message.reply_text(db.getAll().to_markdown())

	elif input_text.startswith('!'):
		if('(' in input_text and ')' in input_text):
			command = StockCommand(input_text[1:])			
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
			
			bot.reply(message = textOf_answer)			
		except:
			rs = parseTextCommand(input_text)			
			if rs == "":
				update.message.reply_text(
					"Sorry I can't recognize you , you said '%s'" % update.message.text)
			else:
				update.message.reply_text(rs)

def main():	
	application = Application.builder().token(TELE_TOKEN).build()
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("help", help))	
	# on non command i.e message - echo the message on Telegram
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, plot_graph))

	application.run_polling(timeout=60)
	
	#application.run_polling(allowed_updates=Update.ALL_TYPES)
	#updater.run_polling(timeout=60)

if __name__ == "__main__":
    main()

