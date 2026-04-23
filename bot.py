# ===============================
# MEGABOT CLEAN FINAL VERSION
# TikTok / Instagram / YouTube Downloader
# ===============================

import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# -------- WEB --------
@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

# -------- START --------
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(
        m.chat.id,
        "🔥 MegaBot Ishlayapti!\n\n📥 TikTok / Instagram / YouTube link yuboring."
    )

# -------- ONLY ONE HANDLER --------
@bot.message_handler(func=lambda m: m.text and "http" in m.text)
def download(m):
    chat = m.chat.id
    url = m.text.strip().split("?")[0]

    wait = bot.send_message(chat, "⏳ Yuklanmoqda...")

    try:
        video = f"{chat}.mp4"
        audio = f"{chat}.mp3"

        # VIDEO
        opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": video,
            "quiet": True,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        if os.path.exists(video):
            with open(video, "rb") as f:
                bot.send_video(chat, f, caption="🎬 Video tayyor")
            os.remove(video)

        # AUDIO
        opts2 = {
            "format": "bestaudio/best",
            "outtmpl": audio,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

        with yt_dlp.YoutubeDL(opts2) as ydl:
            ydl.download([url])

        if os.path.exists(audio):
            with open(audio, "rb") as f:
                bot.send_audio(chat, f, caption="🎵 Audio tayyor")
            os.remove(audio)

        bot.delete_message(chat, wait.message_id)

    except Exception as e:
        bot.send_message(chat, "❌ Yuklab bo‘lmadi")

# -------- RUN --------
Thread(target=run_web).start()
print("Bot ishga tushdi")
bot.infinity_polling()
