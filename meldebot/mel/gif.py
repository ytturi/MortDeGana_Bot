###############################################################################
# Project: Mort de Gana Bot
# Author: Ytturi
# Descr: Answer command with custom GIF options from Giphy
# Commands:
# - MEL: Send random GIF (See `get_mel_params`). Usage: `/mel`
# - MOTO: Send motorbike GIF. Usage: `/moto`
###############################################################################
from telegram.ext import CommandHandler
import telegram
from random import randint
from configparser import ConfigParser
from os.path import expanduser
from logging import getLogger
from requests import get as http_get

# Self imports
from meldebot.mel.conf import get_giphy_api_key, get_debug_enabled
from meldebot.mel.utils import send_typing_action


def get_gif_url(params):
    logger = getLogger('GIF')
    api_key = get_giphy_api_key()
    if not api_key:
        logger.critical('NO API KEY FOR GIPHY!')
        exit(-1)

    base_url = "https://api.giphy.com/v1/gifs/search"
    search_params = '+'.join(params)
    idx = randint(1, 50)
    query_url = '{url}?q={search}&offset={idx}&limit=1&api_key={api}'.format(
        url=base_url, search=search_params, idx=idx, api=api_key
    )
    logger.debug('GIPHY - GET: {}'.format(query_url))
    r = http_get(query_url)
    if r.status_code != 200:
        logger.error("Could not get giphy content!")
        logger.error("{} - {}".format(r.status_code, r.text))
        r.raise_for_status()
    gif_id = r.json()['data'][0]['id']
    gif_url = 'https://media.giphy.com/media/{}/giphy.gif'.format(gif_id)
    return gif_url


def get_random_params():
    search_params = [
        'fun',
        'funny',
        'laugh',
        'honey',
        'falling',
        'drunk'
    ]
    param_num = randint(1, 3)
    params = []
    while len(params) < param_num:
        params.append(search_params[randint(0, len(search_params)-1)])
    if 'honey' in params:
        # Filter for unwanted gifs e.e'
        params = ['honey']
    return params


def get_gifs(opt):
    if 'mel' in opt:
        params = get_random_params()
    elif 'moto' in opt:
        params = ['crash', 'motorbike']
    return get_gif_url(params)


# Def Handler
@send_typing_action
def cb_mel_handler(update, context):
    update.message.reply_animation(get_gifs('mel'))


@send_typing_action
def cb_moto_handler(update, context):
    update.message.reply_animation(get_gifs('moto'))

mel_handler = CommandHandler('mel', cb_mel_handler)
moto_handler = CommandHandler('moto', cb_moto_handler)

GIF_HANDLERS = [
    mel_handler,
    moto_handler
]