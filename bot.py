import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
from flask import Flask, Response

app = Flask(__name__)

TOKEN = os.getenv('BOT_TOKEN', '7991521182:AAEkhXGYjVve_C1zCFz0b1z_YH8FJmSOPnY')
CHANNEL_LINK = "https://t.me/+mZ-efTXP6LgzMWNk"

bot = telebot.TeleBot(TOKEN)

# Dictionary to store message IDs for deletion
user_messages = {}

@app.route('/')
def health_check():
    return Response("Bot is running", status=200)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create inline button
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Join Channel", url=CHANNEL_LINK))
    
    # Send message with button
    sent_msg = bot.send_message(message.chat.id, "Click the button below to join the channel:", reply_markup=markup)
    
    # Store message IDs for deletion
    user_messages[message.chat.id] = [message.message_id, sent_msg.message_id]
    
    # Schedule deletion after 5 minutes
    threading.Thread(target=delete_after_delay, args=(message.chat.id, 300)).start()

def delete_after_delay(chat_id, delay):
    time.sleep(delay)
    if chat_id in user_messages:
        for msg_id in user_messages[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception as e:
                print(f"Error deleting message: {e}")
        del user_messages[chat_id]

if __name__ == '__main__':
    # Run Flask app in a separate thread
    threading.Thread(target=app.run, kwargs={'host':'0.0.0.0','port':5000}).start()
    # Start Telegram bot
    bot.polling(none_stop=True)