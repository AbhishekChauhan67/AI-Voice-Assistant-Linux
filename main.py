from src.TTS import TextToSpeech, TTSConfig


tts = TextToSpeech(config=TTSConfig(rate=130, volume=0.6, voice="gmw/en-us"))
tts("Today is very good morning.")
