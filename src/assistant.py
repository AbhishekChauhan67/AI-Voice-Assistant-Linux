
import time

from stt.main import FastWhisperApp
from ollama.setting import LocalLLM

from tts.config import AUDIO_DEVICE, PIPER_MODEL
from tts.controller import PiperController
from tts.piper import PiperTTS


class Assistant:
    def __init__(
        self,
        llm_model: str,
    ) -> None:

        # -------------------------
        # STT
        # -------------------------
        self.stt = FastWhisperApp()

        # -------------------------
        # LLM
        # -------------------------
        self.llm = LocalLLM(
            model=llm_model,
            system_prompt=(
                "You are a local voice assistant named Anna. "
                "Give short, natural answers suitable for speech. "
                "Do not use markdown unless necessary."
            ),
        )

        # -------------------------
        # TTS
        # -------------------------
        self.tts = PiperTTS(
            model_path=PIPER_MODEL,
            audio_device=AUDIO_DEVICE,
        )

        self.tts_controller = PiperController(self.tts)

        self.running = False

    # =========================
    # TTS
    # =========================

    def speak(self, text: str) -> None:
        if not text:
            return

        print(f"Assistant: {text}")

        self.tts.speak(text)

        # Wait until Piper finishes speaking
        while self.tts.player.is_playing():
            time.sleep(0.05)

    # =========================
    # LLM
    # =========================

    def think(self, text: str) -> str:
        return self.llm.ask(text)

    # =========================
    # PROCESS USER INPUT
    # =========================

    def process(self, text: str) -> None:
        if not text:
            return

        response = self.think(text)

        if response:
            self.speak(response)

    # =========================
    # START
    # =========================

    def run(self) -> None:
        self.running = True

        print("Starting Piper...")
        self.tts_controller.start()

        self.speak("Hello. I am Anna.")

        try:
            while self.running:

                # -------------------------
                # Start recording
                # -------------------------
                self.stt.start_recording()

                # Wait for SPACE
                while True:
                    key = self.stt._read_key().lower()

                    if key == " ":
                        break

                    if key == "q":
                        self.running = False
                        return

                # -------------------------
                # Stop recording
                # -------------------------
                text = self.stt.stop_recording()
                self.stt.recording = False

                if not text:
                    print("No text recognized.")
                    continue

                print(f"You: {text}")

                # -------------------------
                # LLM → TTS
                # -------------------------
                self.process(text)

        except KeyboardInterrupt:
            print("\nStopping assistant...")

        finally:
            self.close()

    # =========================
    # CLOSE
    # =========================

    def close(self) -> None:
        self.running = False

        if self.stt.recording:
            self.stt.stop_recording()
            self.stt.recording = False

        self.tts_controller.stop()

        print("Assistant stopped.")


def main() -> None:
    assistant = Assistant(
        llm_model="qwen3:8b",
    )

    assistant.run()


if __name__ == "__main__":
    main()

