# 07 Sep, 2026
# Voice Formate Data Class

from dataclasses import dataclass


# Voice Data Class
@dataclass(frozen=True, kw_only=True)
class TTSVoice:
    id: str
    name: str
    language: str
