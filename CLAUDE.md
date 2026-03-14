# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceIM is a push-to-talk voice input method for X11/i3wm. It records audio when the Right Ctrl key is held, transcribes it via a FireRedASR API server, and types the result at the current cursor position.

## Commands

```bash
# Run the application
voiceim

# Or directly
python -m voiceim.main

# Install in development mode
pip install -e .
```

## Architecture

The application follows a simple pipeline architecture orchestrated by `VoiceIM` class in `main.py`:

```
[Right Ctrl held] → AudioRecorder → Transcriber → Typer → [text typed at cursor]
```

### Components

- **`main.py`** - `VoiceIM` class orchestrates the pipeline using pynput keyboard listener
- **`recorder.py`** - `AudioRecorder` captures 16kHz mono audio via sounddevice (FireRedASR requires 16kHz)
- **`transcriber.py`** - `Transcriber` sends WAV files to FireRedASR API at `http://localhost:8000/v1/transcribe`
- **`typer.py`** - `Typer` simulates keyboard typing via pynput

## Configuration

Requires `FIREREDASR_API_KEY` environment variable (can be set in `.env` file). The FireRedASR API server must be running on localhost:8000.

## Platform Notes

- Uses pynput for keyboard handling (requires X11)
- Designed for i3wm environment
- Audio captured via sounddevice (requires PulseAudio or ALSA)
