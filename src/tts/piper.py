# 08 Sep, 2026
# Piper Load Model And Generate Byte for player

import logging
from pathlib import Path

from piper import PiperVoice

from .config import AUDIO_DEVICE, PIPER_MODEL
from .exception import TTS_ERROR, TTS_MODEL_NOT_FOUND
from .player import AudioPlayer
from .cleaner import clean_for_piper

logger = logging.getLogger(__name__)


class PiperTTS:
    def __init__(
        self,
        model_path: Path = PIPER_MODEL,
        audio_device=AUDIO_DEVICE,
    ):
        self.model_path = model_path
        self.audio_device = audio_device

        self.player = AudioPlayer(device=self.audio_device)

        if not self.model_path.exists():
            logger.error("Piper model not found at %s", self.model_path)
            raise TTS_MODEL_NOT_FOUND(f"Model not found at {self.model_path}")

        try:
            logger.info("Loading Piper model from %s", self.model_path)
            self.voice = PiperVoice.load(model_path=str(self.model_path))
            logger.info("Piper model ready")
        except Exception as ex:
            logger.exception("Failed to load Piper model")
            raise TTS_ERROR(f"Failed to load Piper model: {ex}") from ex

    def speak(self, text: str) -> None:
        clean_for_piper(text=text)
        if not text or not text.strip():
            logger.debug("Ignoring empty TTS input")
            return

        logger.info("Synthesizing %d characters of speech", len(text.strip()))
        audio_stream = self.voice.synthesize(text)

        self.player.play(audio_stream)

    def stop(self) -> None:
        logger.debug("Stopping TTS playback")
        self.player.stop()

    def is_playing(self) -> bool:
        return self.player.is_playing()

