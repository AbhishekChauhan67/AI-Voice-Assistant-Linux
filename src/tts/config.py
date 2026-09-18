# 08 Sep, 2026
# Set Path Of model needed for piper-tts

__all__ = ["PIPER_MODEL", "AUDIO_DEVICE"]

from pathlib import Path

ProjectDir = Path(__file__).resolve().parents[2]

PIPER_MODEL = ProjectDir / "models" / "piper" / "en_US-lessac-medium.onnx"
AUDIO_DEVICE = None
