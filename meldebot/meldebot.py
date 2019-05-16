from configparser import ConfigParser
from telegram.ext import Updater
from os.path import expanduser
import logging

# Self-imports
from confs import get_logging_options
from mel import mel_handler
from poll import poll_handlers

# Main Process
if __name__ == '__main__':
    # Init confs
    config = ConfigParser()
    config.read(['mortdegana.cfg', expanduser('~/.mortdegana.cfg')])
    # Init logger
    log_level, log_format = get_logging_options(config)
    logging.basicConfig(level=log_level,format=log_format)
    logger = logging.getLogger('INIT')
    # Init listener
    TOKEN = config.defaults().get("token", False)
    if not TOKEN:
        logger.critical("No token provided! Add a token at the config file: '~/.mortdegana.cfg'")
        exit(-1)
    logger.debug("TOKEN: {}".format(TOKEN))
    updater = Updater(TOKEN)
    #   ADD Handler for "hello"
    for handler in poll_handlers:
        updater.dispatcher.add_handler(handler)
    updater.dispatcher.add_handler(mel_handler)
    #   Listen till end
    updater.start_polling()
    updater.idle()
