"""Keyboard simulation for typing transcribed text."""

import keyboard


class Typer:
    """Types text using keyboard simulation."""

    def type_text(self, text: str):
        """Type the given text at the current cursor position."""
        if text:
            keyboard.write(text, delay=0.01)
