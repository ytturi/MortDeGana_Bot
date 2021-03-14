###############################################################################
# Project: Mort de Gana Bot
# Author: Ytturi
# Descr: Commands executed on reply to messages
# Commands:
# - Substitute (replace): Replace text usage: `/s <textToReplace>/<replacement>`
# - Spoiler: Hide spoiler messages in pop-up attachments. Usage: `/spoiler`
###############################################################################
from __future__ import annotations
from typing import TYPE_CHECKING

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from logging import getLogger
import telegram

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext

logger = getLogger(__name__)

from meldebot.mel.utils import (
    send_typing_action,
    remove_command_message,
    get_username,
    get_insult,
    reply_not_implemented,
)


@send_typing_action
def cb_spoiler_handler(update: Update, context: CallbackContext) -> None:
    logger.info("Reply spoiler")
    logger.warn("Spoiler: Not yet implemented")
    reply_not_implemented(update)
    # TODO: Store message to get_store_path() and reply with filename_id
    # spoiler_message = update.effective_message.reply_to_message
    # if not spoiler_message:
    #     spoiler_message = update.effective_message
    # logger.debug(spoiler_message.text)
    # update.message.reply_text(
    #     "{} that's a spoiler!".format(spoiler_message.from_user.name),
    #     reply_markup=InlineKeyboardMarkup([
    #         [
    #             InlineKeyboardButton(
    #                 'Show Spoiler',
    #                 callback_data='spoiler_popup {}'.format(f'Spoiler: {spoiler_message.text}')),
    #         ],
    #     ]),
    # )
    # #TODO: Borrar missatges
    # spoiler_message.delete()


@send_typing_action
@remove_command_message
def cb_substitute_handler(update: Update, context: CallbackContext) -> None:
    logger.info("Reply subsitute")
    substitute_text = update.effective_message.text.split(" ", 1)[1]

    original_message = update.effective_message.reply_to_message

    from_text = substitute_text.split("/", 1)[0]
    to_text = substitute_text.split("/", 1)[1]

    final_text = original_message.text.replace(from_text, to_text)
    update.message.reply_text(
        '*Did you mean?*:\n"{}"'.format(final_text),
        reply_to_message_id=original_message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


@send_typing_action
@remove_command_message
def cb_insult_handler(update, context) -> None:
    logger.info("Reply insult")

    original_message = update.effective_message.reply_to_message
    insult = get_insult()

    if original_message:
        update.message.reply_text(
            f"Ets un {insult}",
            reply_to_message_id=original_message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            quote=True,
        )
    else:
        update.message.reply_text(
            f"Ets un {insult}",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )


spoiler_handler = CommandHandler("spoiler", cb_spoiler_handler)
substitute_handler = CommandHandler("s", cb_substitute_handler)
insult_handler = CommandHandler("insult", cb_insult_handler)

REPLY_HANDLERS = [spoiler_handler, substitute_handler, insult_handler]
