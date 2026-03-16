# VoiceIM

Push-to-talk voice input method for X11/i3wm.

Hold Right Ctrl to record your voice, release to transcribe and type the text at your cursor position.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- X11 (Linux)
- [xdotool](https://www.semicomplete.com/projects/xdotool/) (for Unicode text input)
- [xclip](https://github.com/astrand/xclip) (for clipboard paste)
- [FireRedASR](https://github.com/archibate/FireRedASR) server running locally

## Installation

```bash
git clone https://github.com/archibate/VoiceIM.git
cd VoiceIM
```

## Usage

1. Start the FireRedASR server (see [FireRedASR `api/README.md`](https://github.com/archibate/FireRedASR/blob/main/api/README.md) for setup guide)

2. Set your API key:

   ```bash
   export FIREREDASR_API_KEY=your-api-key
   ```

   Or create a `.env` file in the project directory:
   ```
   FIREREDASR_API_KEY=your-api-key
   ```

3. Run VoiceIM:

   ```bash
   uv run voiceim
   ```

4. Hold **Right Ctrl** to record, release to transcribe and type

## Configuration

VoiceIM uses a config file at `~/.config/voiceim/config.json`. It's created automatically with defaults on first run.

### Config Options

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
| `hot_key` | string | `ctrl_r` | Key to hold for recording |
| `min_duration` | float | `0.3` | Minimum recording duration in seconds |
| `clipboard_threshold` | int | `20` | Text length threshold for clipboard paste (shorter uses keyboard simulation) |

### Custom Config Path

Use `-f` to specify a different config file:

```bash
uv run voiceim -f /path/to/config.json
```

### Hot Keys

Valid hot key names: `ctrl_r`, `ctrl_l`, `shift`, `shift_r`, `alt`, `alt_r`, `cmd`, `f1`-`f20`, `space`, `tab`, etc.

## How it works

```
[Hold Right Ctrl] → Record audio → Send to FireRedASR API → Type transcribed text
```

## License

MIT
