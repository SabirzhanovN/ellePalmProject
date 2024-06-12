import telepot
import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
my_id = os.getenv('MY_CHAT_ID')
telegramBot = telepot.Bot(token)


def send_message_bot(text):
    telegramBot.sendMessage(my_id, text)