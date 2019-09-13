from telegram.ext import CommandHandler
from random import randint

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

def get_hc_text(bot, update):
    phrase = get_random_phrase()
    update.message.reply_text(phrase)

hc_handler = CommandHandler('hacescosas', get_hc_text)
