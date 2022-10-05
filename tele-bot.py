import telegram
import random

TELE_TOKEN = '5505330729:AAG4HHefzja4rMp81XNmeGv5YdQe8t0nSUo'
CHAT_ID = '5505330729'

# def send_test_message():
#     try:
#         random_number = random.randint(0, 1000)
#         telegram_notify = telegram.Bot(TELE_TOKEN)
#         message = "`Số random là {}`".format(random_number) 
    
#         telegram_notify.send_message(chat_id=CHAT_ID, text=message,
#                                 parse_mode='Markdown')
#     except Exception as ex:
#         print(ex)

# send_test_message()

def send():
    bot = telegram.Bot(token=TELE_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text='USP-Python has started up!')

send()