# VoiceIM

Push-to-talk voice input method for X11/i3wm.

Hold Right Ctrl to record your voice, release to transcribe and type the text at your cursor position.

## Requirements

- Python 3.11+
- X11 (Linux)
- [FireRedASR](https://github.com/archibate/FireRedASR) server running locally

## Installation

```bash
pip install voiceim
```

Or from source:

```bash
git clone https://github.com/archibate/VoiceIM.git
cd VoiceIM
pip install -e .
```

## Usage

1. Start the FireRedASR server (see [FireRedASR](https://github.com/archibate/FireRedASR))

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
   voiceim
   ```

4. Hold **Right Ctrl** to record, release to transcribe and type

## How it works

```
[Hold Right Ctrl] → Record audio → Send to FireRedASR API → Type transcribed text
```

## License

MIT
