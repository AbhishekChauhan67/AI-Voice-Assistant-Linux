# AI Voice Assistant — AI/Voice Setup Guide

This document explains how to install and configure the main AI components used by the project:

- Piper TTS
- faster-whisper
- Ollama
- Ollama LLM models

---

## 1. Prerequisites

Recommended environment:

- Linux
- Python 3.10+
- `pip`
- `venv`
- Git
- curl

Check your versions:

```bash
python3 --version
pip --version
git --version
curl --version
```

---

# 2. Create Python Virtual Environment

From the project directory:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Verify:

```bash
which python
python --version
```

---

# 3. Install Piper TTS

Piper is used for **Text-to-Speech (TTS)**.

## Option A — Install with pip

Install Piper:

```bash
pip install piper-tts
```

Verify:

```bash
python -m piper --help
```

---

## 3.1 Download a Piper Voice

Create a directory for voices:

```bash
mkdir -p models/piper
cd models/piper
```

Piper requires a voice model and its configuration file.

A voice consists of:

```text
voice.onnx
voice.onnx.json
```

For example:

```text
models/
└── piper/
    ├── en_US-lessac-medium.onnx
    └── en_US-lessac-medium.onnx.json
```

Use the Piper voice/model source to download the voice you want.

Return to the project directory:

```bash
cd ../..
```

---

## 3.2 Test Piper

Example:

```bash
echo "Hello, I am your AI voice assistant." | \
python -m piper \
--model models/piper/en_US-lessac-medium.onnx \
--output_file test.wav
```

Play the generated audio:

```bash
aplay test.wav
```

If `aplay` is unavailable, use another audio player such as:

```bash
ffplay test.wav
```

---

# 4. Install faster-whisper

`faster-whisper` is used for **Speech-to-Text (STT)**.

Install:

```bash
pip install faster-whisper
```

Verify:

```bash
pip show faster-whisper
```

---

## 4.1 Basic faster-whisper Test

Create:

```bash
touch test_whisper.py
```

Add:

```python
from faster_whisper import WhisperModel

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe("test.wav")

print("Detected language:", info.language)

for segment in segments:
    print(segment.text)
```

Run:

```bash
python test_whisper.py
```

The first execution may download the Whisper model.

---

## 4.2 Whisper Model Sizes

Common models:

| Model | Speed | Accuracy | RAM/CPU Requirement |
|---|---|---|---|
| `tiny` | Very fast | Lower | Very low |
| `base` | Fast | Good | Low |
| `small` | Moderate | Better | Moderate |
| `medium` | Slow | High | High |
| `large-v3` | Very slow | Very high | Very high |

For a CPU-based assistant, start with:

```python
WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)
```

For better accuracy:

```python
WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)
```

---

# 5. Install Ollama

Ollama is used to run the **local LLM**.

## Arch Linux

Install:

```bash
sudo pacman -S ollama
```

Enable and start the service:

```bash
sudo systemctl enable --now ollama
```

Check:

```bash
systemctl status ollama
```

Check Ollama:

```bash
ollama --version
```

---

## Other Linux Distributions

The official installer can be used:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Then check:

```bash
ollama --version
```

---

# 6. Install an Ollama Model

List installed models:

```bash
ollama list
```

Download a model:

```bash
ollama pull llama3.2
```

Other examples:

```bash
ollama pull qwen2.5
```

```bash
ollama pull gemma3
```

```bash
ollama pull mistral
```

---

# 7. Test Ollama

Run a model:

```bash
ollama run llama3.2
```

Then type:

```text
Hello
```

To exit:

```text
/bye
```

---

# 8. Test Ollama API

Ollama normally provides a local API.

Check:

```bash
curl http://localhost:11434/api/tags
```

You should receive information about installed models.

---

# 9. Install Python Ollama Library

Inside the virtual environment:

```bash
pip install ollama
```

Verify:

```bash
pip show ollama
```

---

# 10. Test Ollama from Python

Create:

```bash
touch test_ollama.py
```

Add:

```python
from ollama import chat

response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Hello, introduce yourself."
        }
    ]
)

print(response.message.content)
```

Run:

```bash
python test_ollama.py
```

---

# 11. Recommended Project Model Structure

Keep downloaded AI models outside your source code where possible.

Example:

```text
AI Voice Assistant/
│
├── models/
│   ├── piper/
│   │   ├── en_US-lessac-medium.onnx
│   │   └── en_US-lessac-medium.onnx.json
│   │
│   └── whisper/
│
├── src/
│   ├── assistant.py
│   │
│   ├── stt/
│   │   └── whisper.py
│   │
│   ├── tts/
│   │   └── piper.py
│   │
│   ├── llm/
│   │   └── ollama.py
│   │
│   ├── wakeword/
│   │
│   └── database/
│       └── history.py
│
├── tests/
│
├── requirements.txt
├── .env
└── README.md
```

---

# 12. Python Requirements

A basic `requirements.txt` can contain:

```text
faster-whisper
piper-tts
ollama
```

Install everything:

```bash
pip install -r requirements.txt
```

If you also use audio recording/playback:

```bash
pip install sounddevice
```

For serial communication:

```bash
pip install pyserial
```

---

# 13. Check Installation

Run:

```bash
python -c "import ollama; print('Ollama Python library: OK')"
```

Run:

```bash
python -c "import faster_whisper; print('faster-whisper: OK')"
```

Run:

```bash
python -m piper --help
```

Check Ollama:

```bash
ollama --version
```

Check models:

```bash
ollama list
```

---

# 14. Complete Installation

For a fresh Linux installation, the basic setup is:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install Python packages
pip install faster-whisper piper-tts ollama sounddevice pyserial

# Install Ollama on Arch
sudo pacman -S ollama

# Start Ollama
sudo systemctl enable --now ollama

# Download LLM
ollama pull llama3.2

# Check installation
ollama list
```

---

# 15. Quick Test

### Piper

```bash
echo "Hello from Piper." | \
python -m piper \
--model models/piper/en_US-lessac-medium.onnx \
--output_file test.wav
```

### faster-whisper

```bash
python test_whisper.py
```

### Ollama

```bash
ollama run llama3.2
```

### Python Ollama

```bash
python test_ollama.py
```

---

# 16. Troubleshooting

## Piper cannot be imported

Check:

```bash
pip show piper-tts
```

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -U piper-tts
```

---

## faster-whisper model download is slow

The first execution downloads the selected Whisper model.

After downloading, subsequent executions can use the cached model.

For a CPU system, try:

```python
WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)
```

---

## Ollama service is not running

Check:

```bash
systemctl status ollama
```

Start it:

```bash
sudo systemctl start ollama
```

Enable it at boot:

```bash
sudo systemctl enable ollama
```

Test:

```bash
curl http://localhost:11434/api/tags
```

---

## Ollama model not found

Check installed models:

```bash
ollama list
```

Download the required model:

```bash
ollama pull llama3.2
```

Make sure the Python code uses the exact model name:

```python
response = chat(
    model="llama3.2",
    messages=messages
)
```

---

# 17. Recommended Initial Configuration

For development, start with:

```text
STT
└── faster-whisper
    └── base / small
```

```text
TTS
└── Piper
    └── en_US-lessac-medium
```

```text
LLM
└── Ollama
    └── llama3.2
```

Once the complete pipeline works:

```text
Microphone
    ↓
Wake Word
    ↓
Speech-to-Text
    ↓
faster-whisper
    ↓
LLM
    ↓
Ollama
    ↓
Response Cleaning
    ↓
Piper TTS
    ↓
Speaker
```

This gives you a simple local pipeline that can later be optimized for lower latency and lower memory usage.