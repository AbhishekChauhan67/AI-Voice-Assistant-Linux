import json
import os

import numpy as np

try:
    from vosk import KaldiRecognizer, Model
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    KaldiRecognizer = None
    Model = None

from ..fast_whisper.exception import STTModelError, STTRecognitionError
from ..fast_whisper.microphone import Microphone
from .config import VoskConfig


class VoskSTT:
    def __init__(self, config: VoskConfig | None = None) -> None:
        self.config = config or VoskConfig()
        self.microphone = Microphone(
            sample_rate=self.config.sample_rate,
            channels=self.config.channels,
        )
        self.model = None
        self.recognizer = None
        self._load_model()

    def _load_model(self) -> None:
        if Model is None or KaldiRecognizer is None:
            raise STTModelError(
                "vosk is not installed. Install it with 'pip install vosk'."
            )

        if not os.path.isdir(self.config.model_path):
            raise STTModelError(
                "Vosk model directory not found. "
                f"Expected a model folder at: {self.config.model_path}. "
                "Download a Vosk model and place it there, or set VOSK_MODEL_PATH."
            )

        try:
            self.model = Model(self.config.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.config.sample_rate)
        except Exception as exc:
            raise STTModelError(
                f"Could not load Vosk model: {exc}"
            ) from exc

    def listen(self) -> str:
        if self.recognizer is None:
            raise STTModelError("Vosk recognizer is not loaded.")

        try:
            audio = self.microphone.record(self.config.max_recording_seconds)

            if audio is None or np.size(audio) == 0:
                return ""

            pcm = np.asarray(audio, dtype=np.float32)
            pcm = np.clip(pcm, -1.0, 1.0)
            pcm = np.int16(pcm * 32767)
            payload = pcm.tobytes()

            if self.recognizer.AcceptWaveform(payload):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()
                return text

            partial = json.loads(self.recognizer.PartialResult())
            return partial.get("partial", "").strip()

        except Exception as exc:
            raise STTRecognitionError(
                f"Vosk speech recognition failed: {exc}"
            ) from exc
