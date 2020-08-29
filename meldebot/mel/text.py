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
from telegram.ext import CommandHandler
from random import randint

from meldebot.mel.utils import send_typing_action

def get_random_phrase():
    phrase = ["Druty",
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
     "-Nice... +tru mit iu pro eh"
     "Mel",
     "El rp",
     "Nas fent",
     "Muakatrakamatrakatek",
     "Hacendado me hallo",
     "Mort de gana",
     "Els reis son els pandas",
     "i tu qui ets?"]
    phrase_num = randint(0, len(phrase) -1)
    return phrase[phrase_num]

@send_typing_action
def get_hc_text(update, context):
    phrase = get_random_phrase()
    update.message.reply_text(phrase)

def get_random_name():
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
    name_num = randint(0, len(name) -1)
    return name[name_num]

@send_typing_action
def get_tuquiets_text(update, context):
    _name = get_random_name()
    update.message.reply_text(_name)

tuquiets_handler = CommandHandler('tuquiets', get_tuquiets_text)
hc_handler = CommandHandler('hacescosas', get_hc_text)

TEXT_HANDLERS = [
    tuquiets_handler,
    hc_handler
]