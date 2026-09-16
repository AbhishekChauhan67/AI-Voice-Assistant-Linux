import os
from dataclasses import dataclass


@dataclass(frozen=True)
class STTConfig:

    # Whisper model can be a Hugging Face model name such as "small"
    # or a local directory path via WHISPER_MODEL_PATH.
    model: str = os.environ.get("WHISPER_MODEL", "medium")
    model_path: str | None = os.environ.get("WHISPER_MODEL_PATH")
    language: str = os.environ.get("WHISPER_LANGUAGE", "en")

    # Audio
    sample_rate: int = 16000
    channels: int = 1

    # Hardware
    device: str = os.environ.get("WHISPER_DEVICE", "cpu")
    compute_type: str = os.environ.get("WHISPER_COMPUTE_TYPE", "int8")

    # Recording
    max_recording_seconds: float = 8.0

    # VAD
    min_silence_duration_ms: int = 500
    speech_pad_ms: int = 300

    # Whisper decoding
    beam_size: int = 5
    temperature: float = 0.0

    # Hallucination filtering
    no_speech_threshold: float = 0.6
    log_prob_threshold: float = -1.0
    compression_ratio_threshold: float = 2.4


@dataclass(frozen=True)
class AppConfig:

    stt: STTConfig = STTConfig()