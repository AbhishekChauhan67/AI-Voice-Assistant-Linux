# 07 Sep, 2026
# from src.TTS.PYTTSX3 import TextToSpeech, TTSConfig


# tts = TextToSpeech(config=TTSConfig(rate=130, volume=0.6, voice="gmw/en-us"))
# tts("Today is very good morning.")

# 08 Sep, 2026

from src.TTS.PIPER import PiperTTS
from src.TTS.PIPER.config import PIPER_MODEL


def main() -> None:

    tts = PiperTTS(
        model_path=PIPER_MODEL,
    )

    tts.speak("Hello. This is Piper text to speech.")


if __name__ == "__main__":
    main()
