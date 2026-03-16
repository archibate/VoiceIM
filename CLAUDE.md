# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceIM is a push-to-talk voice input method for X11/i3wm. It records audio when the Right Ctrl key is held, transcribes it via a FireRedASR API server, and types the result at the current cursor position.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for Python package management. Use `uv run` to execute commands:

```bash
uv run voiceim                    # Run the application
uv run voiceim -f config.json     # Run with custom config
```

## Architecture

The application follows a simple pipeline architecture orchestrated by `VoiceIM` class:

```
[Hot key held] → AudioRecorder → Transcriber → Typer → [text typed at cursor]
```

- **`main.py`** - `VoiceIM` class orchestrates the pipeline using pynput keyboard listener
- **`recorder.py`** - `AudioRecorder` captures 16kHz mono audio via sounddevice (FireRedASR requires 16kHz)
- **`transcriber.py`** - `Transcriber` sends WAV files to FireRedASR API at `{api_base_url}/v1/transcribe`
- **`typer.py`** - `Typer` types text using clipboard (long text), xdotool (Unicode), or pynput (short ASCII)
- **`config.py`** - Configuration loading with file/env var precedence

## Configuration

Configuration is loaded from `~/.config/voiceim/config.json` by default. Use `-f FILE` to specify a custom config path.

```json
{
  "api_key": null,
  "api_base_url": "http://localhost:8000",
  "hot_key": "ctrl_r",
  "min_duration": 0.3,
  "clipboard_threshold": 20
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | string \| null | null | API key. If null, uses `FIREREDASR_API_KEY` env var |
| `api_base_url` | string | `http://localhost:8000` | Base URL for the transcription API |
| `hot_key` | string | `ctrl_r` | Key to hold for recording (pynput Key enum name) |
| `min_duration` | float | `0.3` | Minimum recording duration in seconds |
| `clipboard_threshold` | int | `20` | Text length threshold for clipboard paste |

## Platform Notes

- Requires X11 (uses pynput for keyboard events)
- Requires xdotool for Unicode text input
- Audio captured via sounddevice (requires PulseAudio or ALSA)
