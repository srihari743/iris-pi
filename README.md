# iris-pi


# Project Jarvis

⚠️ **Archived Project**  
This project is archived and no longer under active development.

---

## Overview

Project Jarvis was an experimental attempt to build a **self-sufficient local AI assistant** running entirely on a **Raspberry Pi**. The objective was to explore whether a lightweight edge device could host a **LLaMA-based language model** and function as a personal AI assistant without relying on cloud services.

The system was designed to process voice input, convert it to text using Speech-to-Text (STT), feed the transcription to a locally hosted language model, and return a response. The entire development environment was managed using Python’s **virtual environment (`venv`)** for dependency isolation and reproducibility.

The project successfully reached the stage where the language model and STT pipeline were functional. However, hardware limitations of the Raspberry Pi created performance bottlenecks that prevented real-time interaction.

---

## Project Goals

- Build a **locally hosted AI assistant**
- Run a **LLaMA-based language model** on a Raspberry Pi
- Implement a **voice input pipeline**
- Integrate **Speech-to-Text → LLM → Response workflow**
- Maintain a **self-contained offline system**

---

## System Architecture

**Hardware**
- Raspberry Pi (primary compute node)
- USB microphone for audio input
- Headless SSH access for development

**Software**
- Raspberry Pi OS (Linux)
- Python 3
- Python virtual environment (`venv`)
- Local LLaMA-based language model
- Whisper-based Speech-to-Text experiments
- Audio processing via PyAudio

---

## Development Flow

### 1. Environment Setup
- Raspberry Pi OS installation and system updates
- SSH configuration for remote development
- Python environment creation using `venv`
- Installation of required dependencies

### 2. Local LLM Deployment
- Integration of a LLaMA-based model
- Initial local inference tests
- Validation of text-based interaction pipeline

### 3. Audio Pipeline Development
- Microphone input testing using PyAudio
- Wake-word detection experiments
- Speech-to-Text integration using Whisper

### 4. Voice Assistant Pipeline
The intended pipeline architecture was:

AUDIO INPUT -> SPEECH-TO-TEXT -> LLM PROCESSING -> TEXT RESPONSE


The pipeline worked functionally but exposed hardware limitations.

---

## Performance Limitations

When running both the **LLM inference** and **Speech-to-Text processing** on the Raspberry Pi, the system experienced significant latency.

Observed performance:

- Speech-to-Text delay: ~10 seconds
- Combined pipeline latency: too high for conversational use

The Raspberry Pi CPU became the primary bottleneck when handling:

- audio processing
- transcription
- language model inference simultaneously

---

## Attempted Optimization

An experimental attempt was made to **offload Speech-to-Text processing to a secondary device (mobile phone)** while keeping the language model on the Raspberry Pi.

The idea was to reduce the Pi's workload and improve responsiveness. However, the cross-device setup did not reach a stable working implementation and development stalled at this stage.

---

## Reason for Archival

The project was archived for the following reasons:

- Hardware limitations of the Raspberry Pi for combined LLM + STT workloads
- Real-time assistant performance could not be achieved
- Further optimization would require significant architectural changes or stronger hardware
- Development focus shifted to other technical priorities

The repository is preserved as a **documented experimental build** rather than a production-ready system.

---

## Repository Structure

core/
iris_core.py
iris_conversation.py

tests/
pyaudio_test.py
wakeword_test.py
whisper_test.py


Additional files:
- `requirements.txt` – Python dependencies
- `.gitignore` – ignored runtime files

---

## Lessons Learned

- Edge devices have strict limits when running **multiple AI workloads simultaneously**
- Running **LLM + STT pipelines locally requires careful resource planning**
- Modular environments using `venv` simplify reproducibility
- Early architectural decisions significantly impact system performance

---

## Future Possibilities

If revisited in the future, potential improvements include:

- running the system on a more powerful machine
- offloading STT to a separate service
- optimizing model quantization
- distributed processing architecture

---

## Status

**Archived**  
This project remains as a record of experimentation with **local AI assistants on constrained hardware**.


