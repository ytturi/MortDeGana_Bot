###############################################################################
# Project: Mort de Gana Bot
# Author: Ytturi
# Descr: Commands executed on reply to messages
# Commands:
# - Substitute (replace): Replace text usage: `/s <textToReplace>/<replacement>`
# - Spoiler: Hide spoiler messages in pop-up attachments. Usage: `/spoiler`
###############################################################################
from telegram.ext import CommandHandler

from meldebot.mel.conf import send_typing_action

@send_typing_action
def cb_spoiler_handler(update, context):
    #TODO
    pass


@send_typing_action
def cb_substitute_handler(update, context):
    substitute_message = update.effective_message
    substitute_text = substitute_message.text.split(' ', 1)[1]

    original_message = update.effective_message.reply_to_message

    from_text = substitute_text.split('/', 1)[0]
    to_text = substitute_text.split('/', 1)[1]

    final_text = original_message.text.replace(from_text, to_text)
    update.message.reply_text(
        "*Did you mean?*:\n\"{}\"".format(final_text),
        reply_to_message_id=original_message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    if not get_debug_enabled():
        substitute_message.delete()


spoiler_handler = CommandHandler('s', cb_spoiler_handler)
substitute_handler = CommandHandler('s', cb_substitute_handler)

REPLY_HANDLERS = [
    spoiler_handler,
    substitute_handler
]