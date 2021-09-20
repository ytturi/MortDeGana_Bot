###############################################################################
# Project: Mort de Gana Bot
# Author: Bcedu
# Descr: Answer command with ImageServer images
# Commands:
#  - GISCEMEME: Send random gisce meme. Usage: `/gisce_meme`
###############################################################################
from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from telegram.ext import CommandHandler
from logging import getLogger
from requests import get as http_get
from requests.auth import HTTPBasicAuth

# Self imports
from meldebot.mel.conf import get_image_server_auth, get_image_server_url
from meldebot.mel.utils import send_typing_action, remove_command_message

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext

logger = getLogger(__name__)


def get_gisce_meme_url(**params: Dict[str, str]) -> str:
    """Get gisce_meme URL as an IMAGE_SERVER API request

    Returns:
        str: URL to the image (gisce_meme)
    """

    base_url = get_image_server_url()
    if base_url is None:
        return None

    auth_info = get_image_server_auth()
    if not auth_info:
        logger.critical("NO AUTH INFO FOR ImageServer!")
        exit(-1)

    auth = HTTPBasicAuth(auth_info["user"], auth_info["password"])

    if params.get("id"):
        base_url += "/image/{}".format(params.get("id"))
    elif params.get("tags"):
        base_url += "/random_image/{0}".format(params.get("tags"))
    else:
        base_url += "/random_image"

    logger.debug("ImageServer - GET: {}".format(base_url))
    r = http_get(base_url, auth=auth)
    if r.status_code != 200:
        logger.error("Could not get ImageServer content!")
        logger.error("{} - {}".format(r.status_code, r.text))
        r.raise_for_status()
    img_url = r.json()["url"]
    return img_url


# Def Handler
@send_typing_action
@remove_command_message
def cb_gisce_meme_handler(update: Update, context: CallbackContext) -> None:
    logger.info("Handling meme")
    meme_url = get_gisce_meme_url()
    if meme_url is not None:
        update.message.reply_photo(meme_url, quote=False)

    else:
        logger.error('No connection to image server. Set IMAGE_SERVER config section.')


gisce_meme_handler = CommandHandler("gisce_meme", cb_gisce_meme_handler)

MEME_HANDLERS = [gisce_meme_handler]
