# VoiceIM

Push-to-talk voice input method for X11/i3wm.

Hold Right Ctrl to record your voice, release to transcribe and type the text at your cursor position.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- X11 (Linux)
- [xdotool](https://www.semicomplete.com/projects/xdotool/) (for Unicode text input)
- [xclip](https://github.com/astrand/xclip) (for clipboard paste)
## Installation

```bash
git clone https://github.com/archibate/VoiceIM.git
cd VoiceIM
```

## Usage

1. Run VoiceIM:

   ```bash
   uv run voiceim
   ```

2. Hold **Right Ctrl** to record, release to transcribe and type

## Configuration

VoiceIM uses a config file at `~/.config/voiceim/config.json`. It's created automatically with defaults on first run.

### Config Options

```json
{
  "api_base_url": "https://qwen-qwen3-asr-demo.ms.show",
  "hot_key": "ctrl_r",
  "min_duration": 0.3,
  "clipboard_threshold": 0,
  "sound_enabled": true,
  "record_complete_sound": null,
  "transcribe_error_sound": null,
  "lang": "auto",
  "itn": false
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_base_url` | string | `https://qwen-qwen3-asr-demo.ms.show` | Base URL for the Qwen ASR Gradio server |
| `hot_key` | string | `ctrl_r` | Key to hold for recording |
| `min_duration` | float | `0.3` | Minimum recording duration in seconds |
| `clipboard_threshold` | int | `0` | Text length threshold for clipboard paste (shorter uses keyboard simulation) |
| `sound_enabled` | bool | `true` | Enable/disable sound feedback |
| `record_complete_sound` | string \| null | null | Path to custom WAV for record complete (null = default beep) |
| `transcribe_error_sound` | string \| null | null | Path to custom WAV for error (null = default warning) |
| `lang` | string | `auto` | Language for transcription (auto/zh/en/ja/ko/es/fr/de/ar/it/ru/pt) |
| `itn` | bool | `false` | Enable inverse text normalization |

### Custom Config Path

Use `-f` to specify a different config file:

```bash
uv run voiceim -f /path/to/config.json
```

### Hot Keys

Valid hot key names: `ctrl_r`, `ctrl_l`, `shift`, `shift_r`, `alt`, `alt_r`, `cmd`, `f1`-`f20`, `space`, `tab`, etc.

### Sound Feedback

VoiceIM plays sound feedback for recording events:

| Event | Default Sound | When |
|-------|---------------|------|
| Record complete | 800 Hz beep (0.1s) | After recording finishes, before transcription |
| Transcription error | 400 Hz beep (0.2s) | When API request fails |

To use custom sounds, set `record_complete_sound` or `transcribe_error_sound` to a WAV file path. Set `sound_enabled: false` to disable all sounds.

## How it works

```
[Hold Right Ctrl] → Record audio → Send to Qwen ASR (Gradio) → Type transcribed text
```

## License

MIT
