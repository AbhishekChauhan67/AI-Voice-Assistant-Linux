import logging
import sys
import termios
import tty

from .settings import AppConfig
from .stt import STT


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting STT demo")
    stt = STT(AppConfig().stt)
    print("Press SPACE to record and stop. Press Q to quit.")

    while True:
        file_descriptor = sys.stdin.fileno()
        previous_settings = termios.tcgetattr(file_descriptor)

        try:
            tty.setcbreak(file_descriptor)
            key = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(
                file_descriptor,
                termios.TCSADRAIN,
                previous_settings,
            )

        if key == "q":
            logger.info("Stopping STT demo")
            break

        if key == " ":
            logger.info("Starting manual recording")
            stt.start_recording()
            print("Recording...")

            while True:
                file_descriptor = sys.stdin.fileno()
                previous_settings = termios.tcgetattr(file_descriptor)

                try:
                    tty.setcbreak(file_descriptor)
                    key = sys.stdin.read(1).lower()
                finally:
                    termios.tcsetattr(
                        file_descriptor,
                        termios.TCSADRAIN,
                        previous_settings,
                    )

                if key == " ":
                    logger.info("Stopping manual recording")
                    text = stt.stop_recording()
                    print(f"Recognized: {text or 'nothing'}")
                    break

                if key == "q":
                    logger.info("Exiting STT demo during recording")
                    print("Exiting STT demo.")
                    return


if __name__ == "__main__":
    main()
