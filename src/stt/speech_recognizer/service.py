import speech_recognition as sr
import threading
import os

# Suppress ALSA/JACK warnings
os.environ["PYTHONWARNINGS"] = "ignore"

class STT:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Speech detection
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5

        # Recording state
        self.recording = False
        self.audio = None

        # Calibrate only once
        self._calibrate()

    def _calibrate(self):
        print("Calibrating microphone...")
        print("Please remain silent...")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=2
            )

        print(
            f"Energy threshold: "
            f"{self.recognizer.energy_threshold:.2f}"
        )
        print("Microphone ready.")

    def start_recording(self):
        """Start recording in background."""

        if self.recording:
            return

        self.recording = True
        self.audio = None

        print("Listening...")

        thread = threading.Thread(
            target=self._record,
            daemon=True
        )
        thread.start()

    def _record(self):
        """Record audio until stop_recording() is called."""

        with self.microphone as source:
            try:
                self.audio = self.recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=None
                )

            except Exception as e:
                print(f"Recording error: {e}")

    def stop_recording(self):
        """Stop recording."""

        if not self.recording:
            return None

        self.recording = False

        print("Recording stopped.")

        # IMPORTANT:
        # recognizer.listen() itself cannot be interrupted
        # by simply changing self.recording.
        #
        # So this implementation needs a different recording
        # method for true keyboard-controlled stopping.

        return self.audio

    def recognize(self, audio):
        if audio is None:
            return ""

        try:
            recognize_google = getattr(self.recognizer, "recognize_google")
            text = recognize_google(
                audio,
                language="en-IN"
            )

            return text

        except sr.UnknownValueError:
            print("Could not understand speech.")
            return ""

        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
            return ""