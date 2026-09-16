class TTS_ERROR(Exception):
    """Raised When General Exception Of TTS/piper module."""


class TTS_PLAYBACK_ERROR(Exception):
    """Raised When audio playbacks fail."""


class TTS_MODEL_NOT_FOUND(Exception):
    """Raised When TTS/piper models not found."""
