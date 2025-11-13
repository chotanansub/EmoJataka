"""Configuration settings for the Jataka Emotion Analysis app."""

import os
from pathlib import Path
from typing import Optional

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"
MOCKUP_DIR = DATA_DIR / "mockup"

# Assets directory
ASSETS_DIR = BASE_DIR / "app" / "assets"
FONT_DIR = ASSETS_DIR / "fonts"
THAI_FONT_FILENAME = "thsarabunnew-webfont.ttf"
THAI_FONT_PATH = FONT_DIR / THAI_FONT_FILENAME
THAI_FONT_FAMILY = "TH Sarabun New"
if not THAI_FONT_PATH.exists():
    THAI_FONT_PATH = None

# Legacy flag for backwards compatibility
USE_MOCKUP = os.getenv("USE_MOCKUP", "false").lower() == "true"

# Data loading mode: "real", "mockup", or "adaptive"
_data_mode_env = os.getenv("DATA_MODE")
if _data_mode_env:
    DATA_MODE = _data_mode_env.lower()
else:
    # Fall back to legacy flag if DATA_MODE is not provided
    DATA_MODE = "mockup" if USE_MOCKUP else "adaptive"

VALID_DATA_MODES = {"real", "mockup", "adaptive"}
if DATA_MODE not in VALID_DATA_MODES:
    DATA_MODE = "real"

# Emotion list (8 basic emotions from NRC lexicon)
EMOTIONS = [
    "trust",
    "joy",
    "anger",
    "anticipation",
    "fear",
    "disgust",
    "surprise",
    "sadness"
]

# Data file paths
def get_data_path(filename: str, mode: Optional[str] = None) -> Path:
    """
    Get the path to a data file according to the configured data loading mode.

    Modes:
        - "real": always load from the real data directory
        - "mockup": always load from the mockup data directory
        - "adaptive": load from real data if it exists, otherwise fall back to mockup
    """
    data_mode = (mode or DATA_MODE or "real").lower()
    if data_mode not in VALID_DATA_MODES:
        data_mode = "real"

    if data_mode == "mockup":
        return MOCKUP_DIR / filename

    if data_mode == "adaptive":
        real_path = DATA_DIR / filename
        if real_path.exists():
            return real_path
        mockup_path = MOCKUP_DIR / filename
        if mockup_path.exists():
            return mockup_path
        # If neither exists, fall back to the real path so the caller raises a helpful error
        return real_path

    # Default to real data
    return DATA_DIR / filename

