# 08 Sep, 2026
# Set Path Of model needed for piper-tts

from pathlib import Path

ProjectDir = Path(__file__).resolve().parents[3]

PIPER_MODEL = ProjectDir / "models" / "piper" / "en_US-lessac-medium.onnx"
AUDIO_DEVICE = None
