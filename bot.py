# ==========================================
# MAJOR BOT ULTIMATE (FINAL)
# Render / Railway / VPS
# ==========================================

import os
import telebot
import yt_dlp
from telebot.types import ReplyKeyboardMarkup
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

users = set()

# ---------------- WEB ----------------
@app.route("/")
def home():
    return "Major Bot Ultimate Live 🚀"

# ---------------- MENU ----------------
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📥 Downloader", "🤖 AI")
    kb.row("🎬 Kino", "🎵 Musiqa")
    kb.row("📊 Statistika", "⚙️ Admin")
    return kb

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(msg):
    users.add(msg.chat.id)
    bot.send_message(
        msg.chat.id,
        "🔥 <b>MAJOR BOT ULTIMATE</b>\n\nXush kelibsiz!",
        reply_markup=menu()
    )

# ---------------- BUTTONS ----------------
@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stat(m):
    bot.send_message(m.chat.id, f"👥 Foydalanuvchilar: {len(users)}")

@bot.message_handler(func=lambda m: m.text == "⚙️ Admin")
def admin(m):
    if m.chat.id == ADMIN_ID:
        bot.send_message(m.chat.id, "👑 Admin panel tayyor")
    else:
        bot.send_message(m.chat.id, "⛔ Siz admin emassiz")

@bot.message_handler(func=lambda m: m.text == "🤖 AI")
def ai(m):
    bot.send_message(m.chat.id, "🤖 Savolingizni yozing.")

@bot.message_handler(func=lambda m: m.text == "🎬 Kino")
def kino(m):
    bot.send_message(m.chat.id, "🎬 Kino nomini yozing.")

@bot.message_handler(func=lambda m: m.text == "🎵 Musiqa")
def music(m):
    bot.send_message(m.chat.id, "🎵 Qo‘shiq nomini yozing.")

@bot.message_handler(func=lambda m: m.text == "📥 Downloader")
def down(m):
    bot.send_message(m.chat.id, "📥 TikTok / Instagram / YouTube ssilka yuboring.")

# ---------------- DOWNLOAD ----------------
@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def download(m):
    url = m.text.strip()
    chat = m.chat.id

    wait = bot.send_message(chat, "⏳ Yuklanmoqda...")

    try:
        video = f"{chat}.mp4"
        audio = f"{chat}.mp3"

        # VIDEO
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

        # AUDIO
        opts2 = {
            "format": "bestaudio/best",
            "outtmpl": audio,
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        with yt_dlp.YoutubeDL(opts2) as ydl:
            ydl.download([url])

        with open(audio, "rb") as a:
            bot.send_audio(chat, a, caption="🎵 Audio tayyor")

        if os.path.exists(video):
            os.remove(video)

        if os.path.exists(audio):
            os.remove(audio)

        bot.delete_message(chat, wait.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Yuklab bo‘lmadi\n<code>{e}</code>",
            chat,
            wait.message_id
        )

# ---------------- OTHER ----------------
@bot.message_handler(func=lambda m: True)
def other(m):
    txt = m.text.lower()

    if "salom" in txt:
        bot.send_message(m.chat.id, "Va alaykum assalom 😊")
    else:
        bot.send_message(m.chat.id, "📩 Menyudan tanlang yoki ssilka yuboring.")

# ---------------- RUN ----------------
def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

print("🔥 Major Bot Ultimate ishga tushdi...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
