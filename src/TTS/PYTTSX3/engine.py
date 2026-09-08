# 07 Sep, 2026
# TTS Engine (Pyttsx3) Implementation

from typing import Any, cast

import pyttsx3

from .config import TTSConfig
from .models import TTSVoice


class Engine:
    def __init__(self, config: TTSConfig) -> None:
        self.config = config
        self.engine = pyttsx3.init()

        self._configuration()

    # Configure The Engine
    def _configuration(self) -> None:
        self.engine.setProperty("rate", self.config.rate)  # Set Rate
        self.engine.setProperty("volume", self.config.volume)  # Set Volume

        if self.config.voice is not None:
            self.engine.setProperty("voice", self.config.voice)  # Set Voice

    # Engine Start Speak
    def speak(self, text: str) -> None:
        self.engine.say(text)  # Say the given Text
        self.engine.runAndWait()  # run the Engine and wait for next Line

    # Engine Stop Speak
    def stop(self) -> None:
        self.engine.stop()  # Stop the Engine

    # List Available Voices
    def list_voices(self) -> list[TTSVoice]:
        voices = cast(
            list[Any],
            self.engine.getProperty("voices"),  # Get Available Voices
        )

        return [
            TTSVoice(
                id=voice.id,
                name=voice.name,
                language=(
                    voice.languages[0].decode("utf-8")
                    if isinstance(voice.languages[0], bytes)
                    else str(voice.languages[0])
                )
                if voice.languages
                else "Unknown",
            )
            for voice in voices
        ]
