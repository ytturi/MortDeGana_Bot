from configparser import ConfigParser
from os.path import expanduser

SAMPLE_CFG = """[DEFAULT]
telegram_token: <InsertTelegramBotToken>
giphy_api_key: <InsertGiphyAPIKey>
[LOGGING]
level: INFO
format: [%(asctime)s][%(name)s][%(levelname)s]: %(message)s
"""

config = ConfigParser()

def read_configs(path=False):
    if not path:
        config.read(['mortdegana.cfg', expanduser('~/.mortdegana.cfg')])
    else:
        config.read(path)

def init_configs():
    with open('mortdegana.cfg', 'w') as cfg:
        cfg.write(SAMPLE_CFG)

def get_logging_options():
    from logging import INFO, DEBUG, CRITICAL
    # Defaults
    log_level = INFO
    log_format = '[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'
    levels = {
        'DEBUG': DEBUG,
        'INFO': INFO,
        'CRITICAL': CRITICAL
    }
    # Get from configs
    section = 'LOGGING'
    if config.has_section(section):
        if config.has_option(section, 'level'):
            log_level = config.get(section, 'level')
            if log_level.upper() in levels:
                log_level = levels[log_level]
        if config.has_option(section, 'format'):
            log_format = config.get(section, 'level')

    # Return values
    return log_level, log_format

def get_telegram_token():
    return config.defaults().get("telegram_token", False)

def get_giphy_api_key():
    return config.defaults().get("giphy_api_key", False)
