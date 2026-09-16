# 07 Sep, 2026
# from src.TTS.PYTTSX3 import TextToSpeech, TTSConfig

# 08 Sep, 2026
# Piper-tts

# 09 Sep, 2026
# Adding Control Logic and KeyBoard Interrupt

from stt.settings import AppConfig
from stt.stt import STT
from src.wake_word.detect import Detect





def TEST() -> None:
    config = AppConfig()
    detect = Detect("Hey Mom")
    stt = STT(config.stt)

    try:
        while True:
            text = stt.listen()

            if text:
                if detect.check(text):
                    print("Wake Word detected")
                else:
                    print("No wake Word.")
                print(f"You: {text}")
            else:
                print("No speech detected.")

            if text and text.lower() in ["exit", "quit", "stop"]:
                print("Exiting...")
                break

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # stt.close()
        print("Exiting...")


if __name__ == "__main__":
    TEST()
