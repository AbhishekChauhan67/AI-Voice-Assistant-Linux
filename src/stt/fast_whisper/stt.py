from .microphone import Microphone
from .recognizer import SpeechRecognizer
from .settings import STTConfig


class STT:
    def __init__(self, config: STTConfig) -> None:

        self.config = config

        self.microphone = Microphone(
            sample_rate=config.sample_rate,
            channels=config.channels,
        )

        self.recognizer = SpeechRecognizer(config)

    def listen(self) -> str:

        audio = self.microphone.record(self.config.max_recording_seconds)

        return self.recognizer.transcribe(audio)

    def start_recording(self) -> None:
        self.microphone.start_recording()

    def stop_recording(self) -> str:
        audio = self.microphone.stop_recording()

        if audio.size == 0:
            return ""

        return self.recognizer.transcribe(audio)
