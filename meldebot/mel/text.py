###############################################################################
# Project: Mort de Gana Bot
# Authors:
# - Ytturi
# - gdalmau
# - francescpuig7
# Descr: Send text messages
# Commands:
# - Haces cosas: Send random Haces cosas sentences. Usage: `/hacescosas`
# - Tu qui ets: Send random names of haces cosas & friends. Usage: `/tuquiets`
###############################################################################
from __future__ import annotations

from logging import getLogger
from random import choice
from typing import TYPE_CHECKING

from telegram.ext import CommandHandler

from meldebot.mel.utils import remove_command_message, send_typing_action

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext

logger = getLogger(__name__)


def get_random_phrase() -> str:
    """
    Get a random Mort de gana phrase

    Returns:
        str: Mort de gana phrase
    """
    phrase = [
        "Druty",
        "Se trasca la magedia",
        "La vecina se atormenta",
        "Joc de Crons",
        "Dijendres",
        "Es acil",
        "Padalar",
        "Saitcustomisais",
        "Can lluma",
        "Mes llumat que en Llumi",
        "erpik",
        "isu",
        "phython",
        "L'aplaipr",
        "-Nice... +tru mit iu pro eh" "Mel",
        "El rp",
        "Nas fent",
        "Muakatrakamatrakatek",
        "Hacendado me hallo",
        "Mort de gana",
        "Els reis son els pandas",
        "i tu qui ets?",
    ]
    return choice(phrase)


def get_random_name() -> str:
    """
    Get random Mort de gana names

    Returns:
        str: Mort de gana name
    """
    name = [
        "Jaumayer",
        "Pol obj",
        "Pol ids",
        "Grillem",
        "Agusti Berloso",
        "Eduard Fita",
        "Nicolais ni colareis",
        "Nicolais ni tampoco colareis",
        "Luis Carlos Galan (veure wikipedia)",
        "Pol request",
    ]
    return choice(name)


@send_typing_action
@remove_command_message
def get_hc_text(update: Update, context: CallbackContext) -> None:
    logger.info("Handling hacescosas")
    phrase = get_random_phrase()
    update.message.reply_text(phrase, quote=False)


@send_typing_action
@remove_command_message
def get_tuquiets_text(update: Update, context: CallbackContext) -> None:
    logger.info("Handling tuquiets")
    _name = get_random_name()
    update.message.reply_text(_name, quote=False)


tuquiets_handler = CommandHandler("tuquiets", get_tuquiets_text)
hc_handler = CommandHandler("hacescosas", get_hc_text)

TEXT_HANDLERS = [tuquiets_handler, hc_handler]
