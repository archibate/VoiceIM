"""Qwen ASR transcription client via Gradio."""

import asyncio
import sys
from contextlib import contextmanager, redirect_stdout

import aiohttp
from gradio_client import Client, handle_file

from .config import create_default_config

BASE_URL = "https://qwen-qwen3-asr-demo.ms.show"
USER_AGENT = "Mozilla/5.0 AppleWebKit/537.36 Chrome/143 Safari/537"


@contextmanager
def _suppress_gradio_stdout():
    with redirect_stdout(sys.stderr):
        yield


class Transcriber:
    """Client for Qwen ASR transcription via Gradio."""

    def __init__(
        self,
        api_base_url: str = BASE_URL,
        lang: str = "auto",
        itn: bool = False,
        timeout: float = 60.0,
    ):
        """Initialize the transcriber.

        Args:
            api_base_url: Base URL for the Gradio ASR server.
            lang: Language code (auto/zh/en/ja/ko/es/fr/de/ar/it/ru/pt).
            itn: Enable inverse text normalization.
            timeout: HTTP request timeout in seconds.
        """
        create_default_config()
        self.base_url = api_base_url.rstrip("/")
        self.lang = lang
        self.itn = itn
        self.timeout = timeout

    def transcribe(self, audio_path: str) -> str:
        """Send audio file to Qwen ASR and return transcribed text."""
        return asyncio.run(self._transcribe_async(audio_path))

    async def _transcribe_async(self, audio_path: str) -> str:
        async with aiohttp.ClientSession(
            base_url=self.base_url,
            headers={aiohttp.hdrs.USER_AGENT: USER_AGENT},
            timeout=aiohttp.ClientTimeout(total=self.timeout),
        ) as session:
            # Upload audio file
            with open(audio_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field("files", f, filename="audio.wav")
                res = await session.post("/gradio_api/upload", data=form)
                res.raise_for_status()
                server_path = (await res.json())[0]

            audio_url = f"{self.base_url}/gradio_api/file={server_path}"

            # Call Gradio predict (sync)
            with _suppress_gradio_stdout():
                client = Client(self.base_url)
                result = client.predict(
                    audio_file=handle_file(audio_url),
                    context="",
                    language=self.lang,
                    enable_itn=self.itn,
                    api_name="/asr_inference",
                )
                client.close()
                return result[0]
