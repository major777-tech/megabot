import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Mega Pro Bot Ishlayapti 🚀")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, message.text)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Alive!"

def run():
    bot.infinity_polling()

def web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run).start()

if __name__ == "__main__":
    web()
