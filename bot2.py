
from telegram.ext import Updater, CallbackContext, CommandHandler,MessageHandler,Application
from Config import *
from DateHelper import *
from db import *
from TextCommand import *
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
from pymongo import MongoClient
from DateHelper import NOW, isToday
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

# logger = logging.getLogger(__name__)

client = MongoClient("mongodb+srv://taipm:OAMOHMEC8CPUHoz2@cluster0.nskndlz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = client["TradingBook"]
task_collection = db["tasks"]


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Xin chào! Tôi có thể giúp gì cho bạn?")

async def add_task(task):    
    try:
        task_data = {"task": task}
        task_id = task_collection.insert_one(task_data)
        return task_id.inserted_id
    except Exception as e:
        print(f"An error occurred: {e}")


async def add_task_handler(update, context):
    task = " ".join(context.args)
    task_id = await add_task(task)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Đã thêm công việc '{task}' với ID là {task_id}.")

# Lấy tất cả các task từ database
async def get_all_tasks():
    all_tasks = [task["task"] for task in task_collection.find({})]
    return all_tasks

# Define the list tasks command
async def list_tasks(update, context):
    tasks = await get_all_tasks()
    print(tasks)
    if len(tasks) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Danh sách công việc trống.")
    else:
        message = "Danh sách công việc:\n"
        for i, task in enumerate(tasks):
            message += f"{i + 1}. {task}\n"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the complete task command
# async def complete_task(update, context):
#     try:
#         task_index = int(context.args[0]) - 1
#         task = tasks.pop(task_index)
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Đã hoàn thành công việc '{task}'.")
#     except (IndexError, ValueError):
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Vui lòng nhập số hợp lệ để hoàn thành công việc.")

# async def error(update, context):
#     """Log Errors caused by Updates."""
#     await logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Get the Bot API key
    TELEGRAM_API_KEY = TELE_TOKEN #os.environ.get("TELEGRAM_API_KEY", None)
    if TELEGRAM_API_KEY is None:
        raise ValueError("TELEGRAM_API_KEY environment variable is not set. Please set it to the Telegram Bot API key.")
    
    # Create the Updater and pass the bot API key
    application = Application.builder().token(TELE_TOKEN).build()#aUpdater(TELEGRAM_API_KEY, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = application#updater.dispatcher

    # Add handler for the start command
    dp.add_handler(CommandHandler("start", start))

    # Add handler for the add task command
    dp.add_handler(CommandHandler("add", add_task_handler))

    # Add handler for the list tasks command
    dp.add_handler(CommandHandler("list", list_tasks))

    # Add handler for the complete task command
    #dp.add_handler(CommandHandler("complete", complete_task))

    # Add error handler
    #dp.add_error_handler(error)

    # Start the Bot
    #application.start_polling()
    application.run_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #application.idle()

if __name__ == "__main__":
    main()

