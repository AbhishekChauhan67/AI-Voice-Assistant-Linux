# 08 Sep, 2026
# Player for Piper
# Piper -> Bytes -> RawOutputStream -> Speaker

import threading

import sounddevice as sd

from .exception import TTS_PLAYBACK_ERROR


class AudioPlayer:
    def __init__(self, device=None) -> None:
        self.device = device

        self._stop_event = threading.Event()

        self._stream = None
        self._thread = None

    def play(self, audio_stream) -> None:
        self.stop()

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._play,
            args=(audio_stream,),
            daemon=True,
        )

        self._thread.start()

    def _play(self, audio_stream) -> None:

        try:
            for chunk in audio_stream:
                if self._stop_event.is_set():
                    break

                if self._stop_event.is_set():
                    break

                if self._stream is None:
                    self._stream = sd.RawOutputStream(
                        samplerate=chunk.sample_rate,
                        channels=chunk.sample_channels,
                        dtype="int16",
                        device=self.device,
                    )

                    self._stream.start()

                self._stream.write(chunk.audio_int16_bytes)

        except Exception as ex:
            raise TTS_PLAYBACK_ERROR("Failed to play audio.") from ex
        finally:
            self._close_stream()
            if self._thread is threading.current_thread():
                self._thread = None

    def is_playing(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def stop(self) -> None:
        """Stop Playback."""
        self._stop_event.set()

        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join()

        self._thread = None

    def _close_stream(self) -> None:
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            finally:
                self._stream = None
