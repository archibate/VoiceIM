"""Configuration management for VoiceIM."""

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Default configuration values
DEFAULTS = {
    "api_key": None,  # None = use FIREREDASR_API_KEY env var
    "api_base_url": "http://localhost:8000",
    "hot_key": "ctrl_r",
    "min_duration": 0.3,
}

CONFIG_DIR = Path.home() / ".config" / "voiceim"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    return CONFIG_DIR


def get_config_file() -> Path:
    """Get the configuration file path."""
    return CONFIG_FILE


def load_config() -> dict:
    """Load configuration from file, creating default if not exists."""
    if not CONFIG_FILE.exists():
        return DEFAULTS.copy()

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to load config file: {e}")
        return DEFAULTS.copy()

    # Merge with defaults (config file values override defaults)
    merged = DEFAULTS.copy()
    merged.update({k: v for k, v in config.items() if k in DEFAULTS})
    return merged


def create_default_config() -> None:
    """Create default configuration file if it doesn't exist."""
    if CONFIG_FILE.exists():
        return

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULTS, f, indent=2)
    print(f"Created default config at {CONFIG_FILE}")


def get_api_key(config: dict) -> Optional[str]:
    """Get API key with priority: env var > config file."""
    # Environment variable takes precedence for backwards compatibility
    env_key = os.getenv("FIREREDASR_API_KEY")
    if env_key:
        return env_key
    return config.get("api_key")


def get_config() -> dict:
    """Get full configuration with environment variable overrides applied."""
    config = load_config()
    config["api_key"] = get_api_key(config)
    return config
