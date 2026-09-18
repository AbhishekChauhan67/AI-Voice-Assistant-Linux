import logging
import time

from .config import AUDIO_DEVICE, PIPER_MODEL
from .piper import PiperTTS


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting TTS demo")
    tts = PiperTTS(
        model_path=PIPER_MODEL,
        audio_device=AUDIO_DEVICE,
    )

    try:
        tts.speak("Hello. I am Anna.")
        while tts.is_playing():
            time.sleep(0.1)
    finally:
        logger.info("Stopping TTS demo")
        tts.stop()


if __name__ == "__main__":
    main()
