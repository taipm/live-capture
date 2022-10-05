from pprint import pprint
from time import sleep
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from Imager import getTextFromImage
from watcher import get_last_image


TELE_TOKEN = '5505330729:AAG4HHefzja4rMp81XNmeGv5YdQe8t0nSUo'
CHAT_ID = '5505330729'

#updater = Updater(TELE_TOKEN, use_context=True)
updater = Updater(TELE_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/youtube - To get the youtube URL
	/linkedin - To get the LinkedIn profile URL
	/gmail - To get gmail URL
	/geeks - To get the GeeksforGeeks URL""")


def gmail_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Your gmail link here (I am not\
		giving mine one for security reasons)")


def youtube_url(update: Update, context: CallbackContext):
	update.message.reply_text("Youtube Link =>\
	https://www.youtube.com/")


def linkedIn_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"LinkedIn URL => \
		https://www.linkedin.com/in/dwaipayan-bandyopadhyay-007a/")


def geeks_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"GeeksforGeeks URL => https://www.geeksforgeeks.org/")


def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)
 
def image_handler(update: Update, context: CallbackContext):
    print('image')
    update.message.reply_text("Image received")
    file = update.message.photo[0].file_id    
    obj = context.bot.get_file(file)
    
    obj.download()
    sleep(1)
    last_file = get_last_image()
    text_of_img = getTextFromImage(fileName=last_file)
    sleep(10)
    print(text_of_img)
    update.message.reply_text(text_of_img)

def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('youtube', youtube_url))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('linkedin', linkedIn_url))
updater.dispatcher.add_handler(CommandHandler('gmail', gmail_url))
updater.dispatcher.add_handler(CommandHandler('geeks', geeks_url))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
	Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
#updater.start_polling(timeout=600)
updater.start_polling(timeout=60)
