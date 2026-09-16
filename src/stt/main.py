import sys
import termios
import tty

from .settings import AppConfig
from .stt import STT


class FastWhisperApp:
    def __init__(self) -> None:
        self.stt = STT(AppConfig().stt)
        self.recording = False
        self.running = True

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

    def start_recording(self) -> None:
        if self.recording:
            return

        self.stt.start_recording()
        self.recording = True
        print("Recording...")

    def stop_recording(self) -> str:
        if not self.recording:
            return ""

        print("Recording stopped. Recognizing...")

        text = self.stt.stop_recording()

        self.recording = False

        if text:
            print(f"You: {text}")
        else:
            print("No text recognized.")

        return text

    def handle_key(self, key: str) -> None:
        key = key.lower()

        if key == " ":
            if self.recording:
                self.stop_recording()
            else:
                self.start_recording()

        elif key == "q":
            self.running = False

    def run(self) -> None:
        print("Fast Whisper STT")
        print("Press SPACE to start recording.")
        print("Press SPACE again to stop and transcribe.")
        print("Press Q or CTRL+C to exit.")

        try:
            while self.running:
                key = self._read_key()
                self.handle_key(key)

        except KeyboardInterrupt:
            pass

        finally:
            self.close()

    def close(self) -> None:
        if self.recording:
            self.stop_recording()

        print("\nExiting...")


def main() -> None:
    app = FastWhisperApp()
    app.run()


if __name__ == "__main__":
    main()