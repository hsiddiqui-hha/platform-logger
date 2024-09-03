import json
import re

from abstract_logger.constants import Constants


class AppConfig:
    def __init__(self, config_file=Constants.CONFIG_FILE_PATH):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        if isinstance(self.config_file, str):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            raise TypeError("config_file should be a string path to a JSON file.")

    @property
    def log_level(self):
        return self.config.get("log_level", "DEBUG").upper()

    @property
    def log_destination(self):
        return self.config.get("log_destination", "console")

    @property
    def log_file_path(self):
        return self.config.get("log_file_path", "/var/log/app.log")

    @property
    def log_format(self):
        return self.config.get("log_format", "plain")

    @property
    def anonymize_fields(self):
        return set(self.config.get("anonymize_fields", ["user_id", "email", "ssn"]))

    @property
    def anonymize_patterns(self):
        return {
            key: re.compile(pattern)
            for key, pattern in self.config.get("anonymize_patterns", {
                "email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
                "ssn": "\\b\\d{3}-\\d{2}-\\d{4}\\b",
                "phone": "\\b\\d{3}[-.\\s]?\\d{3}[-.\\s]?\\d{4}\\b"
            }).items()
        }
