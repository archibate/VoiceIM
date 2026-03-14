"""Audio recording with sounddevice."""

import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np


class AudioRecorder:
    """Records audio while active."""

    SAMPLE_RATE = 16000  # FireRedASR expects 16kHz
    CHANNELS = 1
    MIN_DURATION = 0.3  # Minimum recording duration in seconds

    def __init__(self):
        self.stream = None
        self.frames = []

    def start(self):
        """Start recording audio."""
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            callback=self._callback,
        )
        self.stream.start()

    def _callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        self.frames.append(indata.copy())

    def stop(self) -> str | None:
        """Stop recording and save to temp WAV file.

        Returns file path if recording is valid, None if too short.
        """
        self.stream.stop()
        self.stream.close()

        if not self.frames:
            return None

        audio = np.concatenate(self.frames, axis=0)
        duration = len(audio) / self.SAMPLE_RATE

        if duration < self.MIN_DURATION:
            print(f"Recording too short ({duration:.2f}s), skipping")
            return None

        temp_path = tempfile.mktemp(suffix=".wav")
        sf.write(temp_path, audio, self.SAMPLE_RATE)
        return temp_path
