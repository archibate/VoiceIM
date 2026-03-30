"""Main application - push-to-talk voice input method."""

import argparse
import signal
import sys
from pathlib import Path
from pynput import keyboard

from .config import create_default_config, get_config, set_config_file
from .recorder import AudioRecorder
from .sound import SoundPlayer
from .transcriber import Transcriber
from .typer import Typer


def parse_hot_key(key_name: str) -> keyboard.Key:
    """Parse hot key name to pynput Key enum.

    Args:
        key_name: Name of the key (e.g., 'ctrl_r', 'ctrl_l', 'shift', 'alt').

    Returns:
        pynput.keyboard.Key enum value.

    Raises:
        ValueError: If the key name is not valid.
    """
    try:
        return getattr(keyboard.Key, key_name)
    except AttributeError:
        valid_keys = [k for k in dir(keyboard.Key) if not k.startswith("_")]
        raise ValueError(
            f"Invalid hot_key '{key_name}'. Valid keys: {', '.join(valid_keys)}"
        )


class VoiceIM:
    """Push-to-talk voice input method."""

    def __init__(
        self,
        hot_key: keyboard.Key = keyboard.Key.ctrl_r,
        api_base_url: str = "https://qwen-qwen3-asr-demo.ms.show",
        lang: str = "auto",
        itn: bool = False,
        min_duration: float = 0.3,
        clipboard_threshold: int = 20,
        sound_enabled: bool = True,
        record_complete_sound: str | None = None,
        transcribe_error_sound: str | None = None,
    ):
        """Initialize VoiceIM.

        Args:
            hot_key: Key to hold for recording.
            api_base_url: Base URL for the ASR API.
            lang: Language code for transcription.
            itn: Enable inverse text normalization.
            min_duration: Minimum recording duration in seconds.
            clipboard_threshold: Text length threshold for clipboard paste.
            sound_enabled: Whether sound feedback is enabled.
            record_complete_sound: Path to custom WAV for record complete.
            transcribe_error_sound: Path to custom WAV for error.
        """
        self.hot_key = hot_key
        self.recorder = AudioRecorder(min_duration=min_duration)
        self.transcriber = Transcriber(
            api_base_url=api_base_url, lang=lang, itn=itn
        )
        self.typer = Typer(clipboard_threshold=clipboard_threshold)
        self.sound_player = SoundPlayer(
            enabled=sound_enabled,
            record_complete_sound=record_complete_sound,
            transcribe_error_sound=transcribe_error_sound,
        )
        self.is_recording = False
        self.listener = None

    def on_press(self, key):
        """Handle key press events."""
        if key == self.hot_key and not self.is_recording:
            self.is_recording = True
            self.recorder.start()
            print("Recording...")

    def on_release(self, key):
        """Handle key release events."""
        if key == self.hot_key and self.is_recording:
            self.is_recording = False
            audio_path = self.recorder.stop()

            if audio_path is None:
                return

            self.sound_player.play_record_complete()
            print("Transcribing...")
            try:
                text = self.transcriber.transcribe(audio_path)
                print(f"Result: {text}")
                self.typer.type_text(text)
            except Exception as e:
                self.sound_player.play_error()
                print(f"Error: {e}")
            finally:
                Path(audio_path).unlink(missing_ok=True)

    def run(self):
        """Start the voice input method."""
        hot_key_name = self.hot_key.name if hasattr(self.hot_key, "name") else str(self.hot_key)
        print(f"VoiceIM started. Hold {hot_key_name} to record.")

        # Set up signal handler for clean shutdown
        def signal_handler(sig, frame):
            print("\nShutting down...")
            if self.listener:
                self.listener.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener.start()
        self.listener.join()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="voiceim",
        description="Push-to-talk voice input method for X11/i3wm.",
    )
    parser.add_argument(
        "-f",
        "--config",
        type=Path,
        default=None,
        metavar="FILE",
        help="path to configuration file (default: ~/.config/voiceim/config.json)",
    )
    return parser.parse_args()


def main():
    """Entry point."""
    args = parse_args()

    if args.config:
        set_config_file(args.config)

    create_default_config()
    config = get_config()

    try:
        hot_key = parse_hot_key(config["hot_key"])
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    app = VoiceIM(
        hot_key=hot_key,
        api_base_url=config["api_base_url"],
        lang=config["lang"],
        itn=config["itn"],
        min_duration=config["min_duration"],
        clipboard_threshold=config["clipboard_threshold"],
        sound_enabled=config["sound_enabled"],
        record_complete_sound=config["record_complete_sound"],
        transcribe_error_sound=config["transcribe_error_sound"],
    )
    app.run()


if __name__ == "__main__":
    main()
