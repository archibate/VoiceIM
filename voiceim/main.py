"""Main application - push-to-talk voice input method."""

import signal
import sys
from pynput import keyboard

from .recorder import AudioRecorder
from .transcriber import Transcriber
from .typer import Typer

HOT_KEY = keyboard.Key.ctrl_r  # Right Ctrl


class VoiceIM:
    """Push-to-talk voice input method."""

    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.typer = Typer()
        self.is_recording = False
        self.listener = None

    def on_press(self, key):
        """Handle key press events."""
        if key == HOT_KEY and not self.is_recording:
            self.is_recording = True
            self.recorder.start()
            print("Recording...")

    def on_release(self, key):
        """Handle key release events."""
        if key == HOT_KEY and self.is_recording:
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
        print("VoiceIM started. Hold Right Ctrl to record.")

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
    app = VoiceIM()
    app.run()


if __name__ == "__main__":
    main()
