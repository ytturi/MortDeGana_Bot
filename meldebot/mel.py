from telegram.ext import CommandHandler

def get_gif_url():
    return "https://media1.giphy.com/media/SBC7hH4Wgpt8A/giphy.gif?cid=790b76115cdce320614b4b6636dd5b7a&rid=giphy.gif"

def get_mel_gifs(bot, update):
    update.message.reply_text('WIP!')

mel_handler = CommandHandler('mel', get_mel_gifs)