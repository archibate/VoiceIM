"""FireRedASR API client."""

import httpx

from .config import create_default_config


class Transcriber:
    """Client for FireRedASR transcription API."""

    def __init__(
        self,
        api_key: str | None = None,
        api_base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
    ):
        """Initialize the transcriber.

        Args:
            api_key: API key for authentication.
            api_base_url: Base URL for the API.
            timeout: HTTP request timeout in seconds.
        """
        create_default_config()

        if not api_key:
            raise ValueError(
                "API key required. Set FIREREDASR_API_KEY environment variable "
                "or configure api_key in ~/.config/voiceim/config.json"
            )
        self.api_key = api_key
        self.api_url = f"{api_base_url.rstrip('/')}/v1/transcribe"
        self.client = httpx.Client(timeout=timeout)

    def transcribe(self, audio_path: str) -> str:
        """Send audio file to API and return transcribed text."""
        with open(audio_path, "rb") as f:
            files = {"audio": ("audio.wav", f, "audio/wav")}
            headers = {"X-API-Key": self.api_key}
            response = self.client.post(self.api_url, files=files, headers=headers)
            response.raise_for_status()
            return response.json()["text"]

    def __del__(self):
        """Clean up HTTP client."""
        if hasattr(self, "client"):
            self.client.close()
