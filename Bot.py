import os
import requests
from pytube import YouTube
from instaloader import Instaloader
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
logging.basicConfig(level=logging.INFO)

TOKEN = 'YOUR TELEGRAM BOT TOKEN'

def start(update, context):
    update.message.reply_text('Send Instagram or YouTube video URL to download and upload it to Telegram')

def download_video(update, context):
    url = update.message.text
    if 'instagram.com' in url:
        insta_loader = Instaloader()
        insta_loader.download_video(url, target=insta_loader.session.username)
        file_path = os.path.join(insta_loader.config.ADIR, insta_loader.session.username, f'{url.split("/")[-1]}.mp4')
        update.message.reply_video(open(file_path, 'rb'))
    elif 'youtube.com' in url or 'youtu.be' in url:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=False).first()
        stream.download()
        update.message.reply_video(open(stream.default_filename, 'rb'))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
