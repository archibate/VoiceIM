"""Main application - push-to-talk voice input method."""

import signal
import sys
from pynput import keyboard

from .config import create_default_config, get_config
from .recorder import AudioRecorder
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
        api_key: str | None = None,
        api_base_url: str = "http://localhost:8000",
        min_duration: float = 0.3,
    ):
        """Initialize VoiceIM.

        Args:
            hot_key: Key to hold for recording.
            api_key: API key for transcription service.
            api_base_url: Base URL for the API.
            min_duration: Minimum recording duration in seconds.
        """
        self.hot_key = hot_key
        self.recorder = AudioRecorder(min_duration=min_duration)
        self.transcriber = Transcriber(api_key=api_key, api_base_url=api_base_url)
        self.typer = Typer()
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

            print("Transcribing...")
            try:
                text = self.transcriber.transcribe(audio_path)
                print(f"Result: {text}")
                self.typer.type_text(text)
            except Exception as e:
                print(f"Error: {e}")

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


def main():
    """Entry point."""
    create_default_config()
    config = get_config()

    try:
        hot_key = parse_hot_key(config["hot_key"])
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    app = VoiceIM(
        hot_key=hot_key,
        api_key=config["api_key"],
        api_base_url=config["api_base_url"],
        min_duration=config["min_duration"],
    )
    app.run()


if __name__ == "__main__":
    main()
