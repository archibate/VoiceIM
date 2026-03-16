"""Keyboard simulation for typing transcribed text."""

import subprocess

import pyperclip
from pynput.keyboard import Controller, Key


class Typer:
    """Types text using clipboard for long text, pynput/xdotool for short."""

    def __init__(self, clipboard_threshold: int = 20):
        self.keyboard = Controller()
        self.clipboard_threshold = clipboard_threshold

    def type_text(self, text: str):
        """Type the given text at the current cursor position."""
        if not text:
            return

        if len(text) > self.clipboard_threshold:
            # Use clipboard for longer text (instant paste)
            pyperclip.copy(text)
            subprocess.run(
                ["xdotool", "key", "--clearmodifiers", "ctrl+v"],
                check=True,
            )
        elif any(ord(c) > 127 for c in text):
            # Contains Unicode, use xdotool for reliable input
            subprocess.run(
                ["xdotool", "type", "--delay", "0", "--clearmodifiers", text],
                check=True,
            )
        else:
            # Short ASCII, use pynput (fast, preserves clipboard)
            self.keyboard.type(text)
