# 08 Sep, 2026
# Piper Load Model And Generate Byte for player

from pathlib import Path

from piper import PiperVoice

from .config import AUDIO_DEVICE, PIPER_MODEL
from .exception import TTS_ERROR, TTS_MODEL_NOT_FOUND
from .player import AudioPlayer


class PiperTTS:
    def __init__(self, model_path: Path = PIPER_MODEL, audio_device=AUDIO_DEVICE):
        self.model_path = model_path
        self.audio_device = audio_device
        self.player = AudioPlayer(device=self.audio_device)

        if not self.model_path.exists():
            raise TTS_MODEL_NOT_FOUND(f"Model not found at {self.model_path}")

        try:
            self.voice = PiperVoice.load(model_path=str(self.model_path))
        except Exception as ex:
            raise TTS_ERROR(f"Failed to load Piper model: {ex}") from ex

    def speak(self, text: str) -> None:

        if not text or not text.strip():
            return

        audio_stream = self.voice.synthesize(text)

        self.player.play(audio_stream)
