from telegram.ext import Updater
import logging
import click

# Self-imports
from confs import get_logging_options, get_telegram_token, init_configs
from mel import mel_handler
from poll import poll_handlers

@click.command()
@click.option(
    '-i', '--init-config', 'init_config', is_flag=True,
    default=False, help="Initialize config file")
@click.option(
    '-v', '--verbose', is_flag=True,
    default=False, help="Override verbosity level for the logger to INFO")
@click.option(
    '-d', '--debug', is_flag=True,
    default=False, help="Override verbosity level for the logger to DEBUG")
@click.option(
    '-t', '--token',
    default=False, help="Set telegram token instead of using a config file")
def listener(init_config, verbose, debug, token):
    # Init logger
    log_level, log_format = get_logging_options()
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level,format=log_format)
    logger = logging.getLogger('INIT')
    # Init Configs
    if init_config:
        init_configs()
        logger.info("The file 'mortdegana.cfg' has been created.")
        exit(-1)
    # Init listener
    if token:
        TOKEN = token
    else:
        TOKEN = get_telegram_token()
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

# Main Process
if __name__ == '__main__':
    listener()
