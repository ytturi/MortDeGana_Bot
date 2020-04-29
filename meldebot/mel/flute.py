###############################################################################
# Project: Mort de Gana Bot
# Author: Ytturi
# Descr: Answer command with youtube URL
# Commands:
# - FLUTE: Send random shitty flute video
###############################################################################
from telegram.ext import CommandHandler
from random import randint
from logging import getLogger

from meldebot.mel.conf import send_typing_action

def search_video_url(params):
    # TODO: actually search the videos
    vkey = params[0]
    url = 'https://www.youtube.com/watch?v={}'.format(vkey)
    return url 

def get_random_flute():
    # TODO: actually return search parameters
    URLS = [
        'Ep_blZhvI2A', # Jurassic park
        'KolfEhV-KiA', # Titanic
        '3jW4feI2q_I', # Harry Potter
        'SAAFA5T_GBE', # Attack on Titan
    ]    
    vnum = randint(0,3)
    return [URLS[vnum]]

def get_video_url(opt):
    if 'flute' in opt:
        params = get_random_flute()
    return search_video_url(params)

# Def Handler
@send_typing_action
def cb_flute_handler(update, context):
    update.message.reply_html(get_video_url('flute'))

flute_handler = CommandHandler('flute', cb_flute_handler)
