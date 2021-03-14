###############################################################################
# Project: Mort de Gana Bot
# Authors:
# - Ytturi
# - gdalmau
# Descr: Utils for the bot
###############################################################################
from __future__ import annotations
from functools import wraps
from random import randint, choice
from typing import Callable, Optional, TYPE_CHECKING

import telegram
from telegram import User

from meldebot.mel.conf import get_debug_enabled

if TYPE_CHECKING:
    from telegram import Update


TILTING_MESSAGES = (
    "Te crees un Jedi por mover asi la mano?",
    "Esta no es la orden que buscas",
    "Ejecuten la orden 66 *cof, cof* Perdona que deies?",
    "Vas passat de voltes tu eh!",
    "Diselo a la mano",
    "Qui et penses que ets tu?",
    "Qui l'ha invitat al grup a aquest?",
    "Algu el coneix? No li faré cas per si de cas...",
    "Ja en parlarem no et preocupis",
    "Esta demanat",
    "I la teva mare també per si de cas",
)


def send_typing_action(func: Callable) -> Callable:
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


def remove_command_message(func: Callable) -> Callable:
    """Removes the message that triggered the handler."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        if get_debug_enabled():
            return func(update, context, *args, **kwargs)
        return_value = func(update, context, *args, **kwargs)
        # Try to remove the original message
        try:
            update.effective_message.delete()
        except:
            # It raises an exception if
            # - it's already removed
            # - it doesn't have permissions
            # But we don't care
            pass
        return return_value

    return command_func


def get_insult() -> Optional[str]:
    from meldebot.insults import get_insults

    # 1703 is INSULTS length
    num: int = randint(0, 1703)

    index = 0
    for insult in get_insults():
        if index == num:
            return insult

        index += 1

    return None


def get_username(telegram_user: User) -> str:
    """
    Get the username from the telegram user

    Args:
        telegram_user (User): Telegram User

    Returns:
        str: Username if it has one. Public name otherwise
    """
    return telegram_user.username or telegram_user.full_name


def reply_not_implemented(update: Update) -> None:
    """
    Reply random text.
    Used to tilt someone who tries to use a not yet implemented command.

    Args:
        update (Update): Chat update as the handler received it
    """

    message = choice(TILTING_MESSAGES)
    update.effective_message.reply_text(
        message,
        quote=True,
    )
