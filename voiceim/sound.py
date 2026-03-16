"""Sound feedback for VoiceIM."""

import threading
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf


class SoundPlayer:
    """Play sound feedback for recording events."""

    def __init__(
        self,
        enabled: bool = True,
        record_complete_sound: str | None = None,
        transcribe_error_sound: str | None = None,
    ):
        """Initialize SoundPlayer.

        Args:
            enabled: Whether sound feedback is enabled.
            record_complete_sound: Path to custom WAV file for record complete,
                or None to use default beep.
            transcribe_error_sound: Path to custom WAV file for error,
                or None to use default warning.
        """
        self.enabled = enabled
        self.record_complete_sound = record_complete_sound
        self.transcribe_error_sound = transcribe_error_sound

    def _generate_beep(self, frequency: float, duration: float = 0.1) -> np.ndarray:
        """Generate a simple sine wave beep.

        Args:
            frequency: Frequency in Hz.
            duration: Duration in seconds.

        Returns:
            Numpy array with audio samples.
        """
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        return 0.3 * np.sin(2 * np.pi * frequency * t)

    def _play_audio(self, audio: np.ndarray, sample_rate: int = 44100) -> None:
        """Play audio in a non-blocking way.

        Args:
            audio: Audio samples as numpy array.
            sample_rate: Sample rate for playback.
        """
        try:
            sd.play(audio, sample_rate)
        except Exception:
            pass  # Silently ignore playback errors

    def _play_file(self, path: str) -> None:
        """Play a WAV file.

        Args:
            path: Path to the WAV file.
        """
        try:
            data, sample_rate = sf.read(path, dtype=np.float32)
            self._play_audio(data, sample_rate)
        except Exception:
            pass  # Silently ignore playback errors

    def _play_in_thread(self, play_func) -> None:
        """Run playback in a background thread to avoid blocking.

        Args:
            play_func: Function to call for playback.
        """
        if not self.enabled:
            return
        thread = threading.Thread(target=play_func, daemon=True)
        thread.start()

    def play_record_complete(self) -> None:
        """Play sound after recording completes."""
        def play():
            if self.record_complete_sound:
                self._play_file(self.record_complete_sound)
            else:
                beep = self._generate_beep(800, 0.1)
                self._play_audio(beep)

        self._play_in_thread(play)

    def play_error(self) -> None:
        """Play sound when transcription fails."""
        def play():
            if self.transcribe_error_sound:
                self._play_file(self.transcribe_error_sound)
            else:
                beep = self._generate_beep(400, 0.2)
                self._play_audio(beep)

        self._play_in_thread(play)
