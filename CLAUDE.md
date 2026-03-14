# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceIM is a push-to-talk voice input method for X11/i3wm. It records audio when the Right Ctrl key is held, transcribes it via a FireRedASR API server, and types the result at the current cursor position.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for Python package management. Use `uv run` to execute commands:

```bash
uv run voiceim
uv run python -m voiceim.main
uv run pytest
```

See the `uv` skill for more details on uv usage patterns.

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

Configuration is loaded from `~/.config/voiceim/config.json` by default. Use `-f FILE` to specify a custom config path.

### Config File Schema

```json
{
  "api_key": null,
  "api_base_url": "http://localhost:8000",
  "hot_key": "ctrl_r",
  "min_duration": 0.3
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string \| null | null | API key for FireRedASR. If null, uses `FIREREDASR_API_KEY` env var |
| `api_base_url` | string | `http://localhost:8000` | Base URL for the transcription API |
| `hot_key` | string | `ctrl_r` | Key to hold for recording (pynput Key name) |
| `min_duration` | float | `0.3` | Minimum recording duration in seconds |

### Hot Key Names

Valid hot key names correspond to pynput's `keyboard.Key` enum: `ctrl_r`, `ctrl_l`, `shift`, `shift_r`, `alt`, `alt_r`, `cmd`, `f1`-`f20`, etc.

### Environment Variables

- `FIREREDASR_API_KEY` - API key (takes precedence over config file `api_key`)

## Platform Notes

- Uses pynput for keyboard handling (requires X11)
- Designed for i3wm environment
- Audio captured via sounddevice (requires PulseAudio or ALSA)
