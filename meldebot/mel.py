###############################################################################
# Project: Mort de Gana Bot
# Author: Ytturi
# Descr: Answer command with custom GIF options from Giphy
# Commands:
# - MEL: Send random GIF (See `get_mel_params`)
# - MOTO: Send motorbike GIF
###############################################################################
from telegram.ext import CommandHandler
import telegram
from random import randint
from configparser import ConfigParser
from os.path import expanduser
from logging import getLogger
from requests import get as http_get
from functools import wraps

# Self imports
from meldebot.confs import get_giphy_api_key


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                     action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


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
def cb_mel_handler(update, context):
    update.message.reply_animation(get_gifs('mel'))

def cb_moto_handler(update, context):
    update.message.reply_animation(get_gifs('moto'))


@send_typing_action
def cb_substitute_handler(update, context):
    substitute_message = update.effective_message
    substitute_text = substitute_message.text.split(' ', 1)[1]

    original_text = substitute_message.reply_to_message.text
    original_message = substitute_message.reply_to_message.message_id

    from_text = substitute_text.split('/')[0]
    to_text = substitute_text.split('/')[1]

    final_text = original_message.text.replace(from_text, to_text)
    update.message.reply_text(
        "*Did you mean?*:\n\"{}\"".format(final_text),
        reply_to_message_id=original_message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    substitute_message.delete()


mel_handler = CommandHandler('mel', cb_mel_handler)
moto_handler = CommandHandler('moto', cb_moto_handler)
substitute_handler = CommandHandler('s', cb_substitute_handler)
