###############################################################################
# Project: Mort de Gana Bot
# Authors:
# - Ytturi
# - gdalmau
# Descr: Configuration management and tooling
###############################################################################
import logging
from configparser import RawConfigParser
from os import makedirs
from os.path import basename, dirname, expanduser, isdir, isfile
from typing import Dict, Optional, Tuple

# Self imports
from meldebot.database import Database

SAMPLE_CFG = """[DEFAULT]
telegram_token: <InsertTelegramBotToken>
giphy_api_key: <InsertGiphyAPIKey>
[LOGGING]
level: INFO
format: [%(asctime)s][%(name)s][%(levelname)s]: %(message)s
[POSTGRES]
# You can either specify the connection URI:
# connection: postgresql://user:password@localhost:port/database
# Or specify each (required) parameter and let the bot build the URI:
# host: localhost
# port: 5432
# user: meldebot
# password: meldebot
# database: meldebot
[IMAGE_SERVER]
url: https://example.com
user: meldebot
password: meldebot
[DEVELOPMENT]
debug: False
"""

config = RawConfigParser(inline_comment_prefixes=[";", "#"], allow_no_value=True)
_database = None


def read_configs(configpath: str = None) -> None:
    """Read Configurations

    Keyword Arguments:
        configpath {str} -- Path to the configuration file (default: {False})
    """
    if not configpath:
        config.read(["mortdegana.cfg", expanduser("~/.mortdegana.cfg")])
    else:
        if isfile(configpath):
            config.read(configpath)


def init_configs(configpath: str = None) -> None:
    """Initialize configurations

    Keyword Arguments:
        configpath {str} -- Path to the configuration file (default: {None})
    """
    if not configpath:
        fname = "mortdegana.cfg"
        configpath = fname
    else:
        fname = basename(configpath)
        pname = dirname(configpath)
        if pname and not isdir(pname):
            makedirs(pname)
    with open(configpath, "w") as cfg:
        cfg.write(SAMPLE_CFG)


def get_logging_options() -> Tuple[int, str]:
    """Get Logging Options

    Returns:
        tuple(int,str) -- Returns a tuple containing the logging level (int) and the format (str)
    """
    # Defaults
    log_level = logging.INFO
    log_format = "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "CRITICAL": logging.CRITICAL,
    }
    # Get from configs
    section = "LOGGING"
    if config.has_section(section):
        if config.has_option(section, "level"):
            log_level_name = config.get(section, "level")
            if log_level_name.upper() in levels:
                log_level = levels[log_level_name]

        if config.has_option(section, "format"):
            log_format = config.get(section, "format")
    else:
        config.add_section(section)
        config.set(section, "level", str(log_level))
        config.set(section, "format", log_format)

    # Return values
    return log_level, log_format


def init_logger(verbose: bool, debug: bool) -> None:
    """Initialize logging settings

    Arguments:
        verbose {boolean} -- Verbosity: Sets logger to INFO level
        debug {boolean} -- Debug: Sets logger to DEBUG level
    """
    log_level, log_format = get_logging_options()
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    config.set("LOGGING", "level", str(logging.getLevelName(log_level)))
    logging.basicConfig(level=log_level, format=log_format)


def get_telegram_token() -> Optional[str]:
    return config.defaults().get("telegram_token")


def get_giphy_api_key() -> Optional[str]:
    return config.defaults().get("giphy_api_key", None)


def get_tenor_api_key() -> Optional[str]:
    return config.defaults().get("tenor_api_key", None)


def get_image_server_url() -> Optional[str]:
    return config.get("IMAGE_SERVER", "url")


def get_image_server_auth() -> Dict[str, Optional[str]]:

    return {
        "user": config.get("IMAGE_SERVER", "user"),
        "password": config.get("IMAGE_SERVER", "password"),
    }


def get_psql_connection() -> Optional[str]:
    """Get the connection URI to connect to the postgres database from the config file.

    Defaults the connection to:

    postgresql://localhost/meldebot

    Returns:
        Optional[str]: Connection URI for the database or None
    """
    section = "POSTGRES"
    if not config.has_section(section):
        return None

    if config.has_option(section, "connection"):
        return config.get(section, "connection")

    host = config.get(section, "host", fallback="localhost")
    database = config.get(section, "database", fallback="meldebot")
    port = config.get(section, "port", fallback=None)
    user = config.get(section, "user", fallback=None)
    password = config.get(section, "password", fallback=None)

    return build_connection_uri_from_params(
        host=host, port=port, user=user, password=password, database=database
    )


def build_connection_uri_from_params(
    host: str,
    database: str,
    user: Optional[str],
    password: Optional[str],
    port: Optional[str],
) -> str:
    """Build the postgresql connection URI from the parameters

    Args:
        host (str): host of the database
        database (str): name of the database
        user (Optional[str]): user to access the database
        password (Optional[str]): password to access the database
        port (Optional[str]): port to access the database

    Returns:
        str: Connection URI
    """

    connection = "postgresql://"

    if user:
        auth = user

        if password:
            auth = f"{user}:{password}"

        connection += f"{auth}@"

    connection += host
    if port:
        connection += f":{port}"

    connection += f"/{database}"

    return connection


def get_database() -> Database:
    """Get the cached database connection or create and cache a new one

    Returns:
        Database: current database connection
    """

    global _database
    if _database is None:
        _database = Database(get_psql_connection())

    return _database


def get_store_path() -> Optional[str]:
    return config.defaults().get("store_path", None)


def get_debug_enabled() -> bool:
    section = "DEVELOPMENT"
    option = "debug"
    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option).lower() == "true"
    return False
