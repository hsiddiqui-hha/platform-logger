import os


class Constants:
    DEFAULT_LOG_LEVEL = 'DEBUG'
    DEFAULT_LOG_DESTINATION = 'console'
    DEFAULT_LOG_FILE_PATH = '/var/log/app.log'
    DEFAULT_LOG_FORMAT = 'plain'

    LOG_FORMAT_JSON = 'json'
    LOG_FORMAT_PLAIN = 'plain'

    CONFIG_FILE_PATH = os.getenv("LOG_CONFIG_PATH", "log_config.json")

