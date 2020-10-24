###############################################################################
# Project: Mort de Gana Bot
# Author: Bcedu
# Descr: Answer command with ImageServer images
# Commands:
#  - GISCEMEME: Send random gisce meme. Usage: `/gisce_meme`
###############################################################################
from telegram.ext import CommandHandler
from logging import getLogger
from requests import get as http_get
from requests.auth import HTTPBasicAuth

# Self imports
from meldebot.mel.conf import get_image_server_auth
from meldebot.mel.utils import send_typing_action, remove_command_message

logger = getLogger(__name__)


def get_gisce_meme_url(**params):
    auth_info = get_image_server_auth()
    if not auth_info:
        logger.critical("NO AUTH INFO FOR ImageServer!")
        exit(-1)

    auth = HTTPBasicAuth(auth_info['user'], auth_info['password'])

    base_url = "https://bcclean.tk/ImageServer/api"
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
def cb_gisce_meme_handler(update, context):
    logger.info("Handling meme")
    update.message.reply_photo(get_gisce_meme_url(id=None, tags=None), quote=False)


gisce_meme_handler = CommandHandler("gisce_meme", cb_gisce_meme_handler)

MEME_HANDLERS = [gisce_meme_handler]

