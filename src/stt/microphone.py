import logging

import numpy as np

import sounddevice as sd

from .exception import STTMicrophoneError


logger = logging.getLogger(__name__)


class Microphone:
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        device=None,
    ) -> None:

        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device
        self._stream = None
        self._chunks = []

    def start_recording(self) -> None:
        if sd is None:
            raise STTMicrophoneError(
                "sounddevice is not installed. Install it with 'pip install sounddevice'."
            )

        if self._stream is not None:
            return

        self._chunks = []

        def callback(indata, frames, time, status):
            if status:
                logger.warning("Microphone status: %s", status)
            self._chunks.append(indata.copy())

        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                device=self.device,
                callback=callback,
            )
            self._stream.start()
            logger.info("Started microphone recording")
        except Exception as exc:
            self._stream = None
            self._chunks = []
            logger.exception("Failed to start microphone recording")
            raise STTMicrophoneError(
                f"Failed to start microphone recording: {exc}"
            ) from exc

    def stop_recording(self) -> np.ndarray:
        if self._stream is None:
            return np.array([], dtype="float32")

        stream = self._stream
        self._stream = None

        try:
            stream.stop()
            stream.close()
            if not self._chunks:
                logger.info("Stopped microphone recording with no audio")
                return np.array([], dtype="float32")

            audio = np.concatenate(self._chunks, axis=0)
            logger.info("Stopped microphone recording: %d samples", audio.shape[0])
            return np.squeeze(audio)
        except Exception as exc:
            logger.exception("Failed to stop microphone recording")
            raise STTMicrophoneError(
                f"Failed to stop microphone recording: {exc}"
            ) from exc
        finally:
            self._chunks = []

    def record(self, seconds: float) -> np.ndarray:
        if sd is None:
            raise STTMicrophoneError(
                "sounddevice is not installed. Install it with 'pip install sounddevice'."
            )

        try:
            logger.info("Recording microphone audio for %.1f seconds", seconds)

            audio = sd.rec(
                int(seconds * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                device=self.device,
            )

            sd.wait()

            result = np.squeeze(audio)
            logger.info("Microphone recording complete: %d samples", result.shape[0])
            return result

        except Exception as exc:
            logger.exception("Failed to record microphone audio")
            raise STTMicrophoneError(
                f"Failed to record microphone audio: {exc}"
            ) from exc