# ==========================================
# MAJORBOT PRO (Telebot)
# TikTok / Instagram / YouTube Downloader
# Render / Railway / VPS Ready
# ==========================================

import os
import telebot
import yt_dlp
from telebot.types import ReplyKeyboardMarkup
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# ================= WEB =================
@app.route('/')
def home():
    return "MAJORBOT PRO LIVE 🚀"

# ================= MENU =================
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📥 Downloader", "🎵 MP3")
    kb.row("ℹ️ Yordam")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(
        m.chat.id,
        "🔥 <b>MAJORBOT PRO</b>\n\n"
        "📥 TikTok / Instagram / YouTube link yuboring.\n"
        "⚡ Fast & Premium Downloader",
        reply_markup=menu()
    )

# ================= BUTTONS =================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def help_btn(m):
    bot.send_message(
        m.chat.id,
        "📌 Bot ishlatish:\n"
        "1. TikTok link yuboring\n"
        "2. Instagram reel yuboring\n"
        "3. YouTube link yuboring\n"
        "4. Video yoki MP3 olasiz"
    )

@bot.message_handler(func=lambda m: m.text == "📥 Downloader")
def down_btn(m):
    bot.send_message(m.chat.id, "📥 Link yuboring.")

@bot.message_handler(func=lambda m: m.text == "🎵 MP3")
def mp3_btn(m):
    bot.send_message(m.chat.id, "🎵 YouTube link yuboring, MP3 beraman.")

# ================= LINK HANDLER =================
@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def download(m):
    chat = m.chat.id
    url = m.text.strip().split("?")[0]

    wait = bot.send_message(chat, "⏳ Yuklanmoqda...")

    try:
        # ===== MP3 if youtube + user selected =====
        if "youtube.com" in url or "youtu.be" in url:
            # Video first
            pass

        video = f"{chat}.mp4"

        opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": video,
            "quiet": True,
            "noplaylist": True,
            "socket_timeout": 60
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        with open(video, "rb") as f:
            bot.send_video(chat, f, caption="🎬 Video tayyor")

        if os.path.exists(video):
            os.remove(video)

        bot.delete_message(chat, wait.message_id)

    except Exception as e:
        bot.edit_message_text(
            "❌ Yuklab bo‘lmadi.\nBoshqa link yuboring.",
            chat,
            wait.message_id
        )

# ================= OTHER =================
@bot.message_handler(func=lambda m: True)
def other(m):
    bot.send_message(m.chat.id, "👇 Menyudan tanlang yoki link yuboring.", reply_markup=menu())

# ================= RUN =================
def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

print("MAJORBOT PRO ishga tushdi...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
