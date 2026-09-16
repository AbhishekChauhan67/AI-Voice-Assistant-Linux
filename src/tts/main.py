import time

from tts.config import AUDIO_DEVICE, PIPER_MODEL
from tts.controller import PiperController
from src.tts.piper import PiperTTS

def tts() -> None:

    tts = PiperTTS(
        model_path=PIPER_MODEL,
        audio_device=AUDIO_DEVICE,
    )

    controller = PiperController(tts)

    controller.start()

    try:
        print("Starting Piper...")
        print("CTRL+D -> Stop")
        print()

        tts.speak("Hello. I am Anna. ")

        while tts.player.is_playing():
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        controller.stop()
        
if __name__ == "__main__":
    tts()