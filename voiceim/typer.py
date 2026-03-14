"""Keyboard simulation for typing transcribed text."""

import subprocess

from pynput.keyboard import Controller


class Typer:
    """Types text using pynput for ASCII, xdotool for Unicode."""

    def __init__(self):
        self.keyboard = Controller()

    def type_text(self, text: str):
        """Type the given text at the current cursor position."""
        if not text:
            return

        if any(ord(c) > 127 for c in text):
            # Contains Unicode, use xdotool for reliable input
            subprocess.run(
                ["xdotool", "type", "--delay", "0", "--clearmodifiers", text],
                check=True,
            )
        else:
            # ASCII only, use pynput (faster)
            self.keyboard.type(text)
