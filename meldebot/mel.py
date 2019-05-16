from telegram.ext import CommandHandler
from random import randint
from configparser import ConfigParser
from os.path import expanduser
from logging import getLogger
from requests import get as http_get

# Self imports
from confs import get_giphy_api_key

def get_gif_url(params):
    logger = getLogger('GIF')
    api_key = get_giphy_api_key()
    if not api_key:
        logger.critical('NO API KEY FOR GIPHY!')
        exit(-1)

    base_url = "https://api.giphy.com/v1/gifs/search"
    search_params = '+'.join(params)
    idx=randint(1, 50)
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
    param_num = randint(1,3)
    params = []
    while len(params) < param_num:
        params.append(search_params[randint(0, len(search_params)-1)])
    if 'honey' in params:
        # Filter for unwanted gifs e.e'
        params = ['honey']
    return params

def get_mel_gifs(bot, update):
    params = get_random_params()
    update.message.reply_animation(get_gif_url(params))

mel_handler = CommandHandler('mel', get_mel_gifs)