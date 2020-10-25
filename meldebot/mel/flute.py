###############################################################################
# Project: Mort de Gana Bot
# Author: Ytturi
# Descr: Answer command with youtube URL
# Commands:
# - FLUTE: Send random shitty flute video
###############################################################################
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from random import choice
from logging import getLogger

from meldebot.mel.utils import send_typing_action, remove_command_message

logger = getLogger(__name__)


def search_video_url(video_key: str) -> str:
    # TODO: actually search the videos
    return "https://www.youtube.com/watch?v={}".format(video_key)


def get_random_flute() -> str:
    # TODO: actually return search parameters
    URLS = [
        "Ep_blZhvI2A",  # Jurassic park
        "KolfEhV-KiA",  # Titanic
        "3jW4feI2q_I",  # Harry Potter
        "SAAFA5T_GBE",  # Attack on Titan
    ]
    return choice(URLS)


def get_video_url(opt: str) -> str:
    if opt == "flute":
        params = get_random_flute()
    return search_video_url(params)


# Def Handler
@send_typing_action
@remove_command_message
def cb_flute_handler(update: Update, context: CallbackContext) -> None:
    logger.info("Handling flute")
    update.message.reply_html(get_video_url("flute"), quote=False)


flute_handler = CommandHandler("flute", cb_flute_handler)
