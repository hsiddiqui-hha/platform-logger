from abc import abstractmethod, ABC

import scrubadub

from .imports import *


class AnonymizationAdapter(ABC):
    @abstractmethod
    def anonymize(self, text: str) -> str:
        pass


class Anonymizer(AnonymizationAdapter):
    def __init__(self, config):
        self.pre_scrub_patterns = config.get("anonymize_patterns", {})
        self.use_scrubadub = config.get("use_scrubadub", True)

    def pre_scrub(self, text: str) -> str:
        for pattern in self.pre_scrub_patterns.values():
            text = re.sub(pattern, "[ANONYMIZED]", text)
        return text

    def anonymize(self, text: str) -> str:
        text = self.pre_scrub(text)
        if self.use_scrubadub:
            text = scrubadub.clean(text)
        return text
