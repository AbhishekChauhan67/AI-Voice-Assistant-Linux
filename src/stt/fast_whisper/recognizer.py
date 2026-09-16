import os

try:
    from faster_whisper import WhisperModel
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    WhisperModel = None

from .exception import (
    STTModelError,
    STTRecognitionError,
)
from .settings import STTConfig


class SpeechRecognizer:

    def __init__(self, config: STTConfig) -> None:
        self.config = config
        self.model = None

        self._load_model()

    def _load_model(self) -> None:
        if WhisperModel is None:
            raise STTModelError(
                "faster-whisper is not installed. Install it with 'pip install faster-whisper'."
            )

        model_name = self.config.model
        if self.config.model_path:
            model_name = self.config.model_path

        if os.path.exists(model_name):
            model_name = os.path.abspath(model_name)
            print(f"Loading local Whisper model from: {model_name}")
        else:
            print(f"Loading Whisper model: {model_name}")

        try:
            self.model = WhisperModel(
                model_name,
                device=self.config.device,
                compute_type=self.config.compute_type,
            )

            print("Whisper ready.")

        except Exception as exc:
            raise STTModelError(
                f"Could not load Whisper model: {exc}"
            ) from exc

    def transcribe(self, audio) -> str:

        if self.model is None:
            raise STTModelError("Whisper model is not loaded.")

        try:
            segments, info = self.model.transcribe(
                audio,

                # Language
                language=self.config.language,

                # Voice Activity Detection
                vad_filter=True,
                vad_parameters={
                    "min_silence_duration_ms":
                        self.config.min_silence_duration_ms,

                    "speech_pad_ms":
                        self.config.speech_pad_ms,
                },

                # Decoding
                beam_size=self.config.beam_size,
                temperature=self.config.temperature,

                # Treat every recording as an independent command
                condition_on_previous_text=False,

                # Hallucination protection
                no_speech_threshold=self.config.no_speech_threshold,
                log_prob_threshold=self.config.log_prob_threshold,
                compression_ratio_threshold=(
                    self.config.compression_ratio_threshold
                ),
            )

            texts = []

            for segment in segments:

                # Ignore probable silence
                if segment.no_speech_prob > self.config.no_speech_threshold:
                    continue

                text = segment.text.strip()

                if text:
                    texts.append(text)

            return " ".join(texts).strip()

        except Exception as exc:
            raise STTRecognitionError(
                f"Speech recognition failed: {exc}"
            ) from exc