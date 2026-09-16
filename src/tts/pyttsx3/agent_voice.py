# 07 Sep, 2026
# Agent Voice List

import json
from pathlib import Path

from .config import TTSConfig
from .engine import Engine


class VoiceStorage:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.file_path = Path(__file__).parent / "voices.json"

    def save_voices(self) -> None:
        voices = self.engine.list_voices()

        data = [
            {
                "id": voice.id,
                "name": voice.name,
                "language": voice.language,
            }
            for voice in voices
        ]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    engine = Engine(TTSConfig())
    json_file = VoiceStorage(engine)

    json_file.save_voices()
