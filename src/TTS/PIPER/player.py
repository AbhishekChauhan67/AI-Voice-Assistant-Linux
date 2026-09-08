# 08 Sep, 2026
# Player for Piper
# Piper -> Bytes -> RawOutputStream -> Speaker

import threading
import sounddevice as sd

from .exception import TTS_PLAYBACK_ERROR



class AudioPlayer:
    def __init__(self, device=None) -> None:
        self.device = device

        self._pause_event = threading.Event()
        self._stop_event = threading.Event()

        self._pause_event.set()

        self._stream = None
        self._thread = None

    
    def play(self, audio_stream):
        stream = None

        try:
            for chunk in audio_stream:
                if stream is None:
                    stream = sd.RawOutputStream(
                        samplerate=chunk.sample_rate,
                        channels=chunk.sample_channels,
                        dtype="int16",
                        device=self.device,
                    )
                    stream.start()

                stream.write(chunk.audio_int16_bytes)

        except Exception as ex:
            raise TTS_PLAYBACK_ERROR("Failed To Play Audio.") from ex

        finally:
            if stream is not None:
                stream.stop()
                stream.close()
