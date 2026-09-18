import logging


logger = logging.getLogger(__name__)


class Detect:
    def __init__(self, word: str) -> None:
        self.wake = word.strip().lower()
        logger.info("Wake-word detector configured")

    def check(self, text: str) -> bool:
        text = text.strip().lower()

        matched = text.startswith(self.wake)
        logger.debug("Wake-word match: %s", matched)
        return matched