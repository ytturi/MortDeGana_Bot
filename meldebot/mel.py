from telegram.ext import CommandHandler

def get_mel_gifs(bot, update):
    update.message.reply_text('WIP!')

mel_handler = CommandHandler('mel', get_mel_gifs)