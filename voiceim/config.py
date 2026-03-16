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
    "clipboard_threshold": 20,
}

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "voiceim"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"

# Module-level config path (can be overridden via CLI)
_config_file: Path = DEFAULT_CONFIG_FILE


def set_config_file(path: Path | str) -> None:
    """Set the configuration file path."""
    global _config_file
    _config_file = Path(path).expanduser().resolve()


def get_config_file() -> Path:
    """Get the current configuration file path."""
    return _config_file


def load_config() -> dict:
    """Load configuration from file, returning defaults if not exists."""
    if not _config_file.exists():
        return DEFAULTS.copy()

    try:
        with open(_config_file, "r") as f:
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
    if _config_file.exists():
        return

    _config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(_config_file, "w") as f:
        json.dump(DEFAULTS, f, indent=2)
    print(f"Created default config at {_config_file}")


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
