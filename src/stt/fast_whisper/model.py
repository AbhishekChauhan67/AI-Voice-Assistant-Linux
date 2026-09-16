from faster_whisper import WhisperModel

model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    "test.wav",
    language="en"
)

for segment in segments:
    print(segment.text)