# ==========================================
# MAJORBOT PRO CLEAN FINAL
# TikTok / Instagram / YouTube Downloader
# Render Ready
# ==========================================

import os
import telebot
import yt_dlp
from telebot.types import ReplyKeyboardMarkup
from flask import Flask
from threading import Thread

# TOKEN
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# ================= WEB =================
@app.route('/')
def home():
    return "MAJORBOT PRO LIVE 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= MENU =================
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📥 Downloader", "ℹ️ Help")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🔥 <b>MAJORBOT PRO</b>\n\n"
        "📥 TikTok / Instagram / YouTube link yuboring.",
        reply_markup=menu()
    )

# ================= HELP =================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_cmd(m):
    bot.send_message(
        m.chat.id,
        "📌 Link yuboring:\n"
        "• TikTok\n"
        "• Instagram\n"
        "• YouTube"
    )

@bot.message_handler(func=lambda m: m.text == "📥 Downloader")
def down_btn(m):
    bot.send_message(m.chat.id, "📥 Link yuboring.")

# ================= DOWNLOAD =================
@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def download(m):
    chat_id = m.chat.id
    url = m.text.strip()

    wait = bot.send_message(chat_id, "⏳ Yuklanmoqda...")

    filename = f"{chat_id}.mp4"

    try:
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": filename,
            "quiet": True,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, "rb") as video:
            bot.send_video(chat_id, video, caption="✅ Tayyor")

        os.remove(filename)
        bot.delete_message(chat_id, wait.message_id)

    except Exception as e:
        bot.edit_message_text(
            "❌ Yuklab bo‘lmadi.\nBoshqa link yuboring.",
            chat_id,
            wait.message_id
        )

# ================= OTHER =================
@bot.message_handler(func=lambda m: True)
def other(m):
    bot.send_message(
        m.chat.id,
        "👇 Menyudan tanlang yoki link yuboring.",
        reply_markup=menu()
    )

# ================= RUN =================
Thread(target=run_web).start()

print("MAJORBOT PRO STARTED 🚀")
bot.infinity_polling(skip_pending=True)
