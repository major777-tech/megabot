# MAJORBOT PRO MULTI LANGUAGE
# PART 1 / STARTER VERSION
# Full advanced version coming next after install test

import os
import telebot
from telebot.types import ReplyKeyboardMarkup
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

users_lang = {}

# ================= WEB =================
@app.route("/")
def home():
    return "MAJORBOT PRO LIVE 🚀"

def run_web():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= LANGUAGE MENU =================
def lang_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🇺🇿 O'zbekcha", "🇺🇸 English")
    kb.row("🇷🇺 Русский")
    return kb

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📥 Downloader", "🎵 MP3")
    kb.row("🌍 Language")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(
        m.chat.id,
        "🌍 Tilni tanlang / Choose language / Выберите язык",
        reply_markup=lang_menu()
    )

# ================= LANGUAGE =================
@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O'zbekcha","🇺🇸 English","🇷🇺 Русский"])
def set_lang(m):
    if "🇺🇿" in m.text:
        users_lang[m.chat.id] = "uz"
        txt = "🔥 Xush kelibsiz MAJORBOT PRO"
    elif "🇺🇸" in m.text:
        users_lang[m.chat.id] = "en"
        txt = "🔥 Welcome to MAJORBOT PRO"
    else:
        users_lang[m.chat.id] = "ru"
        txt = "🔥 Добро пожаловать в MAJORBOT PRO"

    bot.send_message(m.chat.id, txt, reply_markup=main_menu())

# ================= BUTTONS =================
@bot.message_handler(func=lambda m: m.text == "🌍 Language")
def change_lang(m):
    bot.send_message(m.chat.id, "Choose language:", reply_markup=lang_menu())

@bot.message_handler(func=lambda m: m.text == "📥 Downloader")
def down(m):
    bot.send_message(m.chat.id, "📥 Link yuboring / Send link / Отправьте ссылку")

@bot.message_handler(func=lambda m: m.text == "🎵 MP3")
def mp3(m):
    bot.send_message(m.chat.id, "🎵 YouTube link yuboring")

# ================= OTHER =================
@bot.message_handler(func=lambda m: True)
def other(m):
    bot.send_message(m.chat.id, "👇 Link yuboring", reply_markup=main_menu())

# ================= RUN =================
Thread(target=run_web).start()

print("MAJORBOT PRO STARTED")
bot.infinity_polling(skip_pending=True)
