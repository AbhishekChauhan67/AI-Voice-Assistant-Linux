# 07 Sep, 2026
# Text To Speech (TTS) Implementation

from .config import TTSConfig
from .engine import Engine


class TextToSpeech:
    def __init__(self, config: TTSConfig | None) -> None:
        self.config = config or TTSConfig()  # Set Configuration
        self.engine = Engine(self.config)  # Initialize Engine

    def __call__(self, text: str) -> None:
        self.engine.speak(text)
