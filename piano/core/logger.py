# piano/core/logger.py
import logging.config
import os

# Configure logging once when module is imported
_logpath = 'LOG'
_log_filename = 'piano.log'

os.makedirs(_logpath, exist_ok=True)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'precise_formatter': {
            'format': '{asctime} | {levelname} | {name} | {filename}:{lineno} | {message}',
            'style': '{',
        },
        'simple_console_formatter': {
            'format': '{levelname}|{filename}:{lineno}|{message}',
            'style': '{',
        },
    },
    'handlers': {
        'rotating_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'precise_formatter',
            'filename': os.path.join(_logpath, _log_filename),
            'when': 'M',  # Note: 'M' for minute, not 'm'
            'interval': 1,
            'backupCount': 5,
            'level': 'DEBUG',
        },
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple_console_formatter',
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['rotating_file_handler', 'console_handler'],
        'level': 'DEBUG',
    },
})

# Export convenience function
get_logger = logging.getLogger
