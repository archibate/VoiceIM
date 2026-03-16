"""Keyboard simulation for typing transcribed text."""

import subprocess

from pynput.keyboard import Controller


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
            # Copy to both PRIMARY (Shift+Insert in some terminals) and CLIPBOARD (Ctrl+V)
            for selection in ["primary", "clipboard"]:
                subprocess.run(
                    ["xclip", "-selection", selection],
                    input=text.encode(),
                    check=True,
                )
            subprocess.run(
                ["xdotool", "key", "--clearmodifiers", "shift+Insert"],
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
