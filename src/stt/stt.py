import logging

from .microphone import Microphone
from .recognizer import SpeechRecognizer
from .settings import STTConfig


logger = logging.getLogger(__name__)


class AudioRecorder:
    def __init__(self, config: STTConfig) -> None:
        self.config = config
        self.microphone = Microphone(
            sample_rate=config.sample_rate,
            channels=config.channels,
        )

    def start_recording(self) -> None:
        logger.info("Starting audio recorder")
        self.microphone.start_recording()

    def stop_recording(self):
        logger.info("Stopping audio recorder")
        return self.microphone.stop_recording()

    def record(self):
        logger.info("Recording audio for up to %.1f seconds", self.config.max_recording_seconds)
        return self.microphone.record(self.config.max_recording_seconds)


class STT:
    def __init__(self, config: STTConfig) -> None:
        logger.info("Initializing speech-to-text")
        self.config = config
        self.recorder = AudioRecorder(config)
        self.recognizer = SpeechRecognizer(config)

    def listen(self) -> str:
        logger.info("Listening for speech")
        audio = self.recorder.record()
        result = self.recognizer.transcribe(audio)
        logger.info("Speech-to-text complete: %d characters", len(result))
        return result

    def start_recording(self) -> None:
        logger.debug("Starting STT recording")
        self.recorder.start_recording()

    def stop_recording(self) -> str:
        logger.info("Stopping speech recording")
        audio = self.recorder.stop_recording()

        if audio.size == 0:
            logger.info("No audio captured for STT transcription")
            return ""

        return self.recognizer.transcribe(audio)
