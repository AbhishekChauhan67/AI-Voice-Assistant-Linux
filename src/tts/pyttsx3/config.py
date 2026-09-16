# 07 Sep, 2026
# Configuration For Engine TTS (Pyttsx3)

from dataclasses import dataclass


# Default Configuration For Engine TTS (Pyttsx3)
@dataclass(kw_only=True)
class TTSConfig:
    rate: int = 170
    volume: float = 1.0
    voice: str | None = None
