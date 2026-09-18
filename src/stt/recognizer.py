import logging
import os

from faster_whisper import WhisperModel


from .exception import (
    STTModelError,
    STTRecognitionError,
)
from .settings import STTConfig


logger = logging.getLogger(__name__)


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
            logger.info("Loading local Whisper model from %s", model_name)
        else:
            logger.info("Loading Whisper model: %s", model_name)

        try:
            self.model = WhisperModel(
                model_name,
                device=self.config.device,
                compute_type=self.config.compute_type,
            )

            logger.info("Whisper model ready")

        except Exception as exc:
            logger.exception("Could not load Whisper model")
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

            result = " ".join(texts).strip()
            logger.info("Transcription complete: %d characters", len(result))
            return result

        except Exception as exc:
            logger.exception("Speech recognition failed")
            raise STTRecognitionError(
                f"Speech recognition failed: {exc}"
            ) from exc