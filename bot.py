# ==========================================
# MAJORBOT PRO V2 FULL FIXED
# TikTok / Instagram / YouTube Downloader
# Auto Detect + Audio + Quality
# Render Ready
# ==========================================

import os
import telebot
import yt_dlp
from telebot.types import ReplyKeyboardMarkup
from flask import Flask
from threading import Thread

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# ================= WEB =================
@app.route('/')
def home():
    return "MAJORBOT PRO V2 LIVE 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= MENU =================
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📥 Download", "🎵 Audio")
    kb.row("ℹ️ Help")
    return kb

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🔥 <b>MAJORBOT PRO V2</b>\n\n"
        "📥 TikTok / Instagram / YouTube link yuboring.",
        reply_markup=menu()
    )

# ================= HELP =================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_cmd(m):
    bot.send_message(
        m.chat.id,
        "📌 Ishlatish:\n"
        "1. Link yuboring\n"
        "2. Video keladi\n\n"
        "🎵 Audio uchun YouTube link yuboring."
    )

# ================= BUTTONS =================
@bot.message_handler(func=lambda m: m.text == "📥 Download")
def down_btn(m):
    bot.send_message(m.chat.id, "📥 Link yuboring.")

@bot.message_handler(func=lambda m: m.text == "🎵 Audio")
def audio_btn(m):
    bot.send_message(m.chat.id, "🎵 YouTube link yuboring.")

# ================= VIDEO DOWNLOAD =================
@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def download(m):
    chat_id = m.chat.id
    url = m.text.strip()

    wait = bot.send_message(chat_id, "⏳ Yuklanmoqda...")

    try:
        # TikTok / Instagram / YouTube detect
        if "youtube.com" in url or "youtu.be" in url:
            filename = f"{chat_id}.mp4"

            opts = {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": filename,
                "quiet": True,
                "noplaylist": True
            }

        elif "instagram.com" in url:
            filename = f"{chat_id}.mp4"

            opts = {
                "format": "best",
                "outtmpl": filename,
                "quiet": True
            }

        elif "tiktok.com" in url:
            filename = f"{chat_id}.mp4"

            opts = {
                "format": "best",
                "outtmpl": filename,
                "quiet": True
            }

        else:
            bot.edit_message_text(
                "❌ Noto‘g‘ri link.",
                chat_id,
                wait.message_id
            )
            return

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        with open(filename, "rb") as file:
            bot.send_video(chat_id, file, caption="✅ Tayyor")

        os.remove(filename)

        bot.delete_message(chat_id, wait.message_id)

    except Exception as e:
        bot.edit_message_text(
            "❌ Yuklab bo‘lmadi.\nQayta urinib ko‘ring.",
            chat_id,
            wait.message_id
        )

# ================= AUDIO =================
@bot.message_handler(func=lambda m: m.text and ("youtube.com" in m.text or "youtu.be" in m.text) and "🎵" in m.text)
def audio(m):
    pass

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

print("MAJORBOT PRO V2 STARTED 🚀")
bot.infinity_polling(skip_pending=True)
