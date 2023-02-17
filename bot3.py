from Config import TELE_TOKEN
import asyncio
import os
import os
import requests
from telegram import InputFile
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that can help you upload images.")

async def upload_image(update, context):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    response = requests.get(file.file_path)
    with open('images/' + file.file_id + '.jpg', 'wb') as f:
        f.write(response.content)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Image has been saved to the 'images' directory.")


def main():
    #updater = Updater(token=TELE_TOKEN, use_context=True)
    application = Application.builder().token(TELE_TOKEN).build()#aUpdater(TELEGRAM_API_KEY, use_context=True)
    dp = application
    #dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.PHOTO, upload_image))
    dp.run_polling()
    #await dp.idle()

if __name__ == '__main__':
    main()

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that can help you upload images.")

# async def upload_image(update, context):
#     file = context.bot.getFile(update.message.photo[-1].file_id)
#     await file.download('images/' + file.file_path.split("/")[-1])
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Image has been saved to the 'images' directory.")

# def main():
#     # updater = Updater(token=TELE_TOKEN, use_context=False)
#     # dp = updater.dispatcher
#     # dp.add_handler(CommandHandler("start", start))
#     # dp.add_handler(MessageHandler(filters.PHOTO, upload_image))
#     # updater.start_polling()
#     # updater.idle()
#     TELEGRAM_API_KEY = TELE_TOKEN #os.environ.get("TELEGRAM_API_KEY", None)
#     if TELEGRAM_API_KEY is None:
#         raise ValueError("TELEGRAM_API_KEY environment variable is not set. Please set it to the Telegram Bot API key.")
    
#     # Create the Updater and pass the bot API key
#     application = Application.builder().token(TELE_TOKEN).build()#aUpdater(TELEGRAM_API_KEY, use_context=True)
    
#     # Get the dispatcher to register handlers
#     dp = application#updater.dispatcher

#     # Add handler for the start command
#     dp.add_handler(CommandHandler("start", start))

#     # Add handler for the add task command
#     dp.add_handler(CommandHandler("start", start))

#     # Add handler for the list tasks command
#     dp.add_handler(MessageHandler(filters.PHOTO, upload_image))

#     # Add handler for the complete task command
#     #dp.add_handler(CommandHandler("complete", complete_task))

#     # Add error handler
#     #dp.add_error_handler(error)

#     # Start the Bot
#     #application.start_polling()
#     application.run_polling()

# if __name__ == '__main__':
#     main()
