"""Word cloud generation utilities."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from wordcloud import WordCloud
from typing import Dict, Optional
from pathlib import Path
import io
import base64
import logging

LOGGER = logging.getLogger(__name__)

try:
    from ..utils.config import THAI_FONT_PATH, THAI_FONT_FAMILY
except ImportError:  # pragma: no cover - defensive for environments without package context
    THAI_FONT_PATH = None
    THAI_FONT_FAMILY = None

FONT_PROPERTIES: Optional[fm.FontProperties] = None
FONT_PATH_STRING: Optional[str] = None

def _register_thai_font() -> None:
    global FONT_PROPERTIES, FONT_PATH_STRING

    candidate_paths = []
    if THAI_FONT_PATH:
        candidate_paths.append(THAI_FONT_PATH)

    # Optional fallback candidates commonly available on macOS / Windows
    fallback_names = [
        "TH Sarabun New",
        "THSarabunNew",
        "Noto Sans Thai",
        "NotoSansThai-Regular",
        "Arial Unicode MS",
        "Tahoma",
    ]

    for name in fallback_names:
        try:
            path = Path(fm.findfont(name, fallback_to_default=False))
            if path.exists() and path not in candidate_paths:
                candidate_paths.append(path)
        except Exception:
            continue

    for path in candidate_paths:
        try:
            font_path_str = str(Path(path).resolve())
            font_props = fm.FontProperties(fname=font_path_str)
            font_name = THAI_FONT_FAMILY or font_props.get_name()

            # Update Matplotlib defaults for other plots
            mpl.rcParams.setdefault("font.family", [])
            if isinstance(mpl.rcParams["font.family"], str):
                mpl.rcParams["font.family"] = [mpl.rcParams["font.family"]]
            if font_name not in mpl.rcParams["font.family"]:
                mpl.rcParams["font.family"].insert(0, font_name)

            mpl.rcParams.setdefault("font.sans-serif", [])
            if isinstance(mpl.rcParams["font.sans-serif"], str):
                mpl.rcParams["font.sans-serif"] = [mpl.rcParams["font.sans-serif"]]
            if font_name not in mpl.rcParams["font.sans-serif"]:
                mpl.rcParams["font.sans-serif"].insert(0, font_name)

            mpl.rcParams["axes.unicode_minus"] = False

            FONT_PROPERTIES = font_props
            FONT_PATH_STRING = font_path_str
            LOGGER.debug("Registered Thai font: %s (%s)", font_name, font_path_str)
            return
        except Exception as exc:
            LOGGER.warning("Could not register Thai font from %s: %s", path, exc)
            continue

    LOGGER.warning("No Thai font could be registered; word clouds may show missing glyphs.")
    FONT_PROPERTIES = None
    FONT_PATH_STRING = None

try:
    _register_thai_font()
except Exception as font_err:  # pragma: no cover - defensive fallback
    LOGGER.warning("Failed to initialize Thai font handling: %s", font_err)
    FONT_PROPERTIES = None
    FONT_PATH_STRING = None

def generate_wordcloud(
    word_freq: Dict[str, int],
    width: int = 800,
    height: int = 400,
    max_words: int = 100,
    background_color: str = "white"
) -> str:
    """
    Generate a word cloud image and return as base64 encoded string.
    
    Args:
        word_freq: Dictionary mapping words to frequencies
        width: Image width
        height: Image height
        max_words: Maximum number of words to display
        background_color: Background color
    
    Returns:
        Base64 encoded image string
    """
    if not word_freq:
        # Return empty image
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        text_kwargs = {"ha": "center", "va": "center"}
        if FONT_PROPERTIES:
            text_kwargs["fontproperties"] = FONT_PROPERTIES
        ax.text(0.5, 0.5, "ไม่มีข้อมูล" if FONT_PROPERTIES else "No data available", **text_kwargs)
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    
    # Create word cloud
    wordcloud = WordCloud(
        width=width,
        height=height,
        max_words=max_words,
        background_color=background_color,
        colormap='viridis',
        font_path=FONT_PATH_STRING,
        regexp=r"[A-Za-z0-9\u0E00-\u0E7F']+",
        collocations=False
    ).generate_from_frequencies(word_freq)
    
    # Convert to image
    fig, ax = plt.subplots(figsize=(width/100, height/100))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.read()).decode()

def wordcloud_from_dict(word_freq: Dict[str, int]) -> str:
    """Convenience function to generate word cloud from dictionary."""
    return generate_wordcloud(word_freq)

def wordcloud_from_dataframe(df, word_col: str = 'word', freq_col: str = 'frequency'):
    """
    Generate word cloud from DataFrame.
    
    Args:
        df: DataFrame with word and frequency columns
        word_col: Name of word column
        freq_col: Name of frequency column
    
    Returns:
        Base64 encoded image string
    """
    if word_col not in df.columns or freq_col not in df.columns:
        return generate_wordcloud({})
    
    word_freq = dict(zip(df[word_col], df[freq_col]))
    return generate_wordcloud(word_freq)

