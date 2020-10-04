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
from random import randint, choice
from configparser import ConfigParser
from os.path import expanduser
from logging import getLogger
from requests import get as http_get

# Self imports
from meldebot.mel.conf import get_giphy_api_key, get_debug_enabled, get_tenor_api_key
from meldebot.mel.utils import send_typing_action, remove_command_message

logger = getLogger(__name__)


def get_gif_url(params, provider=None):
    if not provider:
        provider = get_random_gif_provider()
    return provider(params)


def get_random_gif_provider():
    return get_gif_provider(choice(list(GIF_PROVIDERS.keys())))


def get_gif_provider(provider_name):
    method_caller = GIF_PROVIDERS.get(provider_name)
    if not method_caller:
        logger.critical("NO PROIDER DEFINED FOR {0}".format(provider_name))
        exit(-1)  # exit or raise Exception ?
    else:
        return method_caller


def get_gif_url_giphy(params):
    api_key = get_giphy_api_key()
    if not api_key:
        logger.critical("NO API KEY FOR GIPHY!")
        exit(-1)

    base_url = "https://api.giphy.com/v1/gifs/search"
    search_params = "+".join(params)
    idx = randint(1, 50)
    url_params = {
        'q': search_params,
        'offset': idx,
        'limit': 1,
        'api_key': api_key,
    }
    logger.debug("GIPHY - GET: {}".format(url_params))
    r = http_get(base_url, params=url_params)
    if r.status_code != 200:
        logger.error("Could not get giphy content!")
        logger.error("{} - {}".format(r.status_code, r.text))
        r.raise_for_status()
    gif_id = r.json()["data"][0]["id"]
    gif_url = "https://media.giphy.com/media/{}/giphy.gif".format(gif_id)
    return gif_url


def get_gif_url_tenor(params):
    api_key = get_tenor_api_key()
    if not api_key:
        logger.critical("NO API KEY FOR Tenor!")
        exit(-1)

    base_url = "https://api.tenor.com/v1/search?"
    search_params = "+".join(params)
    idx = randint(1, 50)
    url_params = {
        'q': search_params,
        'pos': idx,
        'limit': 1,
        'key': api_key,
        'contentfilter': 'off',
        'media_filter': 'basic',
        'ar_range': 'all'
    }
    logger.debug("Tenor - GET: {}".format(url_params))
    r = http_get(base_url, params=url_params)
    if r.status_code != 200:
        logger.error("Could not get tenor content!")
        logger.error("{} - {}".format(r.status_code, r.text))
        r.raise_for_status()
    gif_url = r.json()["results"][0]["url"]
    return gif_url


def get_random_params():
    search_params = ["fun", "funny", "laugh", "honey", "falling", "drunk"]
    param_num = randint(1, 3)
    params = []
    while len(params) < param_num:
        params.append(search_params[randint(0, len(search_params) - 1)])
    if "honey" in params:
        # Filter for unwanted gifs e.e'
        params = ["honey"]
    return params


def get_gifs(opt):
    if "mel" in opt:
        params = get_random_params()
    elif "moto" in opt:
        params = ["crash", "motorbike"]
    return get_gif_url(params)


# Def Handler
@send_typing_action
@remove_command_message
def cb_mel_handler(update, context):
    logger.info("Handling mel")
    update.message.reply_animation(get_gifs("mel"), quote=False)


@send_typing_action
@remove_command_message
def cb_moto_handler(update, context):
    logger.info("Handling moto")
    update.message.reply_animation(get_gifs("moto"), quote=False)


mel_handler = CommandHandler("mel", cb_mel_handler)
moto_handler = CommandHandler("moto", cb_moto_handler)

GIF_HANDLERS = [mel_handler, moto_handler]
GIF_PROVIDERS = {
    "giphy": get_gif_url_giphy,
    "tenor": get_gif_url_tenor,
}
