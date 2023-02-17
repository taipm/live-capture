from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from Config import TELE_TOKEN
import sqlite3

# Mở kết nối đến cơ sở dữ liệu hoặc tạo cơ sở dữ liệu mới nếu chưa tồn tại
conn = sqlite3.connect('quiz.db')

# Tạo bảng `questions`
conn.execute('''CREATE TABLE IF NOT EXISTS questions
             (id INTEGER PRIMARY KEY,
             question TEXT,
             choice1 TEXT,
             choice2 TEXT,
             choice3 TEXT,
             choice4 TEXT,
             answer INTEGER)''')

# Tạo danh sách câu hỏi và đáp án
questions = [
    {
        'question': 'What is the capital of France?',
        'choice1': 'London',
        'choice2': 'Berlin',
        'choice3': 'Paris',
        'choice4': 'Madrid',
        'answer': 3
    },
    {
        'question': 'What is the largest planet in our solar system?',
        'choice1': 'Jupiter',
        'choice2': 'Saturn',
        'choice3': 'Mars',
        'choice4': 'Earth',
        'answer': 1
    },
    {
        'question': 'What is the smallest country in the world?',
        'choice1': 'Monaco',
        'choice2': 'Maldives',
        'choice3': 'Vatican City',
        'choice4': 'San Marino',
        'answer': 3
    }
]

# Lưu các câu hỏi vào cơ sở dữ liệu
for q in questions:
    conn.execute("INSERT INTO questions (question, choice1, choice2, choice3, choice4, answer) VALUES (?, ?, ?, ?, ?, ?)", 
                 (q['question'], q['choice1'], q['choice2'], q['choice3'], q['choice4'], q['answer']))

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

conn = sqlite3.connect('quiz.db')
c = conn.cursor()

# Định nghĩa hàm xử lý lệnh /start
async def start(update:Update, context:CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Chào mừng bạn đến với trắc nghiệm từ vựng tiếng Anh của chúng tôi!")


# Định nghĩa hàm xử lý lệnh /quiz
async def quiz(update:Update, context:CallbackContext):
    # Chọn ngẫu nhiên một câu hỏi từ cơ sở dữ liệu
    # c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    # row = c.fetchone()
    # question = row[1]
    # choices = row[2].split(',')
    # answer = row[3]
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    question = row[1]
    choices = row[2:6]
    answer = row[6]
    conn.close()

    # Lưu đáp án của câu hỏi vào bộ nhớ tạm thời
    context.user_data['answer'] = answer
    
    # Hiển thị câu hỏi và các lựa chọn đáp án cho người dùng
    message = f"{question}\n\n"
    for i, choice in enumerate(choices):
        message += f"{i+1}. {choice}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Define the function to handle text messages
async def echo(update, context:CallbackContext):
    # Check if the user is currently taking a quiz
    context.user_data.setdefault('score', 0)
    context.user_data.setdefault('remaining',3)
    context.user_data.setdefault('total',0)

    if 'answer' in context.user_data:
        # Get the user's choice
        user_choice = int(update.message.text)
        # Get the correct answer from temporary memory and compare with user's choice
        correct_answer = context.user_data['answer']
        if user_choice == int(correct_answer):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Đúng!")
            context.user_data['score'] += 1
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Sai!")
        # Clear temporary memory to prepare for the next question
        del context.user_data['answer']
        # Check if there are more questions left
        if context.user_data['remaining'] > 1:
            context.user_data['remaining'] -= 1
            await quiz(update, context)
        else:
            # Show the user's score
            score = context.user_data['score']
            total = context.user_data['total']
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Kết thúc trắc nghiệm!\nĐiểm của bạn: {score}/{total}")
            # Clear temporary memory to prepare for the next quiz
            del context.user_data['remaining']
            del context.user_data['score']
            del context.user_data['total']
    else:
        # If the user sends a message that is not a number, reply with an error message
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Xin lỗi, tôi không hiểu bạn muốn làm gì.")


# updater.start_polling()
# updater.idle()


def main():
    application = Application.builder().token(TELE_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('quiz', quiz))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.run_polling(timeout=60)


if __name__ == "__main__":
    main()