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

# 3. Install All libs

Piper is used for **Text-to-Speech (TTS)**.

## Option A — Install with pip

Install Piper:

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
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

# 4. Verify faster-whisper

`faster-whisper` is used for **Speech-to-Text (STT)**.

Verify:

```bash
pip show faster-whisper
```

---

## 4.1 Basic faster-whisper Test

src/stt/model.py:


```python
from faster_whisper import WhisperModel

model = WhisperModel(
    "medium",
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
python src/stt/model.py
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

# 11. Python Requirements

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
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

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