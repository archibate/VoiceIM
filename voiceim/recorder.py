"""Audio recording with sounddevice."""

import os
import tempfile

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    """Records audio while active."""

    SAMPLE_RATE = 16000  # FireRedASR expects 16kHz
    CHANNELS = 1

    def __init__(self, min_duration: float = 0.3):
        """Initialize the recorder.

        Args:
            min_duration: Minimum recording duration in seconds.
        """
        self.min_duration = min_duration
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

        if duration < self.min_duration:
            print(f"Recording too short ({duration:.2f}s), skipping")
            return None

        fd, temp_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        sf.write(temp_path, audio, self.SAMPLE_RATE)
        return temp_path
