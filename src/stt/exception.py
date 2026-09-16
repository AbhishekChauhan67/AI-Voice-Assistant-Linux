class STTError(Exception):
    """Base exception for STT errors."""


class STTModelError(STTError):
    """Raised when the STT model cannot be loaded."""


class STTMicrophoneError(STTError):
    """Raised when microphone capture fails."""


class STTRecognitionError(STTError):
    """Raised when speech recognition fails."""