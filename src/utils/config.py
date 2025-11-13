"""Configuration settings for the Jataka Emotion Analysis app."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"
MOCKUP_DIR = DATA_DIR / "mockup"

# Use mockup data flag (set via environment variable or default to False)
USE_MOCKUP = os.getenv("USE_MOCKUP", "false").lower() == "true"

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
def get_data_path(filename: str) -> Path:
    """Get the path to a data file, using mockup if USE_MOCKUP is True."""
    if USE_MOCKUP:
        return MOCKUP_DIR / filename
    return DATA_DIR / filename

