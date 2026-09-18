# Minimal setup for the voice assistant

This project only needs a small set of runtime libraries to run the assistant:

- `faster-whisper` for speech-to-text
- `sounddevice` for microphone input
- `numpy` for audio processing
- `piper-tts` for text-to-speech
- `ollama` for the local LLM

## 1) Install only the required packages

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

The project keeps the dependency list minimal in [requirements.txt](requirements.txt).

## 2) Download the Piper model

The assistant expects a local Piper voice model in:

```text
models/piper/
```

Use the official Piper voice model files in that folder, for example:

```text
models/piper/en_US-lessac-medium.onnx
models/piper/en_US-lessac-medium.onnx.json
```

If the model is missing, the app will fail during TTS initialization.

You can download the model from the official Piper voice repository and place the files in that directory.

## 3) Download or configure the Whisper model

The STT code uses `faster-whisper` and can work with either:

- a local folder path via `WHISPER_MODEL_PATH`, or
- a model name such as `small` that will be downloaded automatically by `faster-whisper`

Example:

```bash
export WHISPER_MODEL=small
```

or:

```bash
export WHISPER_MODEL_PATH=/absolute/path/to/whisper-model
```

The default project config is already set to a small model name, so the first run will fetch it automatically if you do not provide a local path.

## 4) Run the assistant

```bash
python src/assistant.py
```

## 5) Unused libraries removed

The old dependency list included many packages that were not used by the current assistant flow, such as:

- wake word libraries
- speech recognition libraries
- pyttsx3
- audio libs not used by the current pipeline
- general ML packages not required for this simple setup

They were removed to keep the project lightweight and easier to run.

## 6) Notes

- The assistant currently uses a simple local LLM via Ollama.
- Make sure Ollama is installed and the model is available, for example `qwen3:8b`.
- The TTS and STT are intentionally kept simple and direct with minimal wrapper code.
