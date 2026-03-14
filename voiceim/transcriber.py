"""FireRedASR API client."""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()


class Transcriber:
    """Client for FireRedASR transcription API."""

    API_URL = "http://localhost:8000/v1/transcribe"

    def __init__(self):
        self.api_key = os.getenv("FIREREDASR_API_KEY")
        if not self.api_key:
            raise ValueError("FIREREDASR_API_KEY not found in environment")
        self.client = httpx.Client(timeout=30.0)

    def transcribe(self, audio_path: str) -> str:
        """Send audio file to API and return transcribed text."""
        with open(audio_path, "rb") as f:
            files = {"audio": ("audio.wav", f, "audio/wav")}
            headers = {"X-API-Key": self.api_key}
            response = self.client.post(self.API_URL, files=files, headers=headers)
            response.raise_for_status()
            return response.json()["text"]

    def __del__(self):
        """Clean up HTTP client."""
        if hasattr(self, "client"):
            self.client.close()
