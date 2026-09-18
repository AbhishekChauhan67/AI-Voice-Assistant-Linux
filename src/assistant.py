
import logging
import sys
import termios
import time
import tty
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    src_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(src_dir))

try:
    from llm.ollama_client import LocalLLM
    from stt import STT
    from stt.settings import AppConfig
    from tts.config import AUDIO_DEVICE, PIPER_MODEL
    from tts.piper import PiperTTS
except ModuleNotFoundError:
    from src.llm.ollama_client import LocalLLM
    from src.stt import STT
    from src.stt.settings import AppConfig
    from src.tts.config import AUDIO_DEVICE, PIPER_MODEL
    from src.tts.piper import PiperTTS


logger = logging.getLogger(__name__)


class Assistant:
    def __init__(self, llm_model: str) -> None:
        logger.info("Initializing command-line assistant with model %s", llm_model)
        self.stt = STT(AppConfig().stt)
        self.llm = LocalLLM(
            model=llm_model,
            system_prompt=(
                "You are a local voice assistant named Anna. "
                "Give short, natural answers suitable for speech. "
                "Do not use markdown unless necessary."
            ),
        )
        self.tts = PiperTTS(
            model_path=PIPER_MODEL,
            audio_device=AUDIO_DEVICE,
        )
        self.running = False

    def _read_key(self) -> str:
        file_descriptor = sys.stdin.fileno()
        previous_settings = termios.tcgetattr(file_descriptor)

        try:
            tty.setcbreak(file_descriptor)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(
                file_descriptor,
                termios.TCSADRAIN,
                previous_settings,
            )

    def speak(self, text: str) -> None:
        if not text:
            return

        print(f"Assistant: {text}")
        logger.info("Speaking response (%d characters)", len(text))
        self.tts.speak(text)

        while self.tts.is_playing():
            time.sleep(0.05)

    def think(self, text: str) -> str:
        return self.llm.ask(text)

    def process(self, text: str) -> None:
        if not text:
            return

        logger.info("Processing command (%d characters)", len(text))
        response = self.think(text)
        if response:
            self.speak(response)

    def listen_for_command(self) -> str | None:
        logger.info("Listening for command")
        self.stt.start_recording()

        while True:
            key = self._read_key().lower()

            if key == " ":
                break

            if key == "q":
                self.running = False
                return None

        text = self.stt.stop_recording()
        return text.strip() if text else ""

    def run(self) -> None:
        logger.info("Starting command-line assistant")
        self.running = True
        self.speak("Hello. I am Anna.")

        try:
            while self.running:
                text = self.listen_for_command()

                if text is None:
                    break

                if not text:
                    print("No text recognized.")
                    continue

                print(f"You: {text}")
                self.process(text)

        except KeyboardInterrupt:
            print("\nStopping assistant...")
        finally:
            self.close()

    def close(self) -> None:
        logger.info("Stopping command-line assistant")
        self.running = False
        self.stt.stop_recording()
        self.tts.stop()
        print("Assistant stopped.")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    assistant = Assistant(llm_model="qwen3:4b")
    assistant.run()


if __name__ == "__main__":
    main()

