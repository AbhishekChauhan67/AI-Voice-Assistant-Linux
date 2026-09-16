import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VoskConfig:
    model_path: str = os.environ.get(
        "VOSK_MODEL_PATH",
        str(Path(__file__).resolve().parents[3] / "models" / "vosk"),
    )
    sample_rate: int = 16000
    channels: int = 1
    max_recording_seconds: float = 8.0
    language: str = "en-us"
