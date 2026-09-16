import select
import sys
import termios
import threading
import tty

from .piper import PiperTTS


class PiperController:
    CTRL_D = "\x04"

    def __init__(self, tts: PiperTTS) -> None:
        self.tts = tts

        self._running = False
        self._keyboard_thread = None

    def start(self) -> None:
        if self._running:
            return

        self._running = True

        self._keyboard_thread = threading.Thread(
            target=self._keyboard_loop,
            daemon=True,
        )

        self._keyboard_thread.start()

    def stop(self) -> None:
        self._running = False
        self.tts.stop()

        if (
            self._keyboard_thread is not None
            and self._keyboard_thread is not threading.current_thread()
        ):
            self._keyboard_thread.join(timeout=1)

        self._keyboard_thread = None

    def _keyboard_loop(self) -> None:
        if not sys.stdin.isatty():
            return

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)

            while self._running:
                ready, _, _ = select.select(
                    [sys.stdin],
                    [],
                    [],
                    0.1,
                )

                if not ready:
                    continue

                key = sys.stdin.read(1)

                if key == self.CTRL_D:
                    print("\n⏹ Stopped")
                    self.tts.stop()
                    self._running = False

        finally:
            termios.tcsetattr(
                fd,
                termios.TCSADRAIN,
                old_settings,
            )

