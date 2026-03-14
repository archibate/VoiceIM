"""Keyboard simulation for typing transcribed text."""

from pynput.keyboard import Controller


class Typer:
    """Types text using keyboard simulation."""

    def __init__(self):
        self.keyboard = Controller()

    def type_text(self, text: str):
        """Type the given text at the current cursor position."""
        if text:
            self.keyboard.type(text)
