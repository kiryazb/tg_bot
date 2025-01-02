from telebot import TeleBot


TELEGRAM_TOKEN = ''  # Добавьте токен в код (не делайте так в реальных проектах!)
CHAT_ID = ''  # Укажите chat_id

bot = TeleBot(token=TELEGRAM_TOKEN)


def send_message(message):
    ...
    bot.send_message(CHAT_ID, message)

# Вызовите функцию здесь
send_message('тест')