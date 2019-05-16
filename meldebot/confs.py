def get_logging_options(config):
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