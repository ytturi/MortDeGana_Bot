from telegram.ext import CommandHandler
from random import randint

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

def get_tuquiets_text(bot, update):
    _name = get_random_name()
    update.message.reply_text(_name)

tuquiets_handler = CommandHandler('tuquiets', get_tuquiets_text)