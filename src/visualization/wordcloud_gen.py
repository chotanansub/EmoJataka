"""Word cloud generation utilities."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from wordcloud import WordCloud
from typing import Dict, Optional
from pathlib import Path
import io
import base64
import logging
import numpy as np
from PIL import Image

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
    width: int = 3200,
    height: int = 2400,
    max_words: int = 500,
    theme: str = "light",
    title: Optional[str] = None
) -> str:
    """
    Generate a word cloud image with Buddha mask and custom colors.

    Args:
        word_freq: Dictionary mapping words to frequencies
        width: Image width
        height: Image height
        max_words: Maximum number of words to display
        theme: Theme style - "light" for white background or "dark" for dark background
        title: Optional title text to display in top-right corner

    Returns:
        Base64 encoded image string
    """
    if not word_freq:
        # Return empty image
        _, ax = plt.subplots(figsize=(width/100, height/100))
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

    # Get project root and paths
    project_root = Path(__file__).parent.parent.parent
    font_path = project_root / "app" / "assets" / "fonts" / "Sarabun-Thin.ttf"
    mask_path = project_root / "app" / "assets" / "img" / "buddha-mask.png"

    # Use Sarabun-Thin font if available, otherwise fallback
    font_path_str = str(font_path) if font_path.exists() else FONT_PATH_STRING

    # Load Buddha mask if available
    mask_image = None
    if mask_path.exists():
        try:
            mask_image = np.array(Image.open(mask_path).convert("L"))
            mask_image = 255 - mask_image  # Invert colors
        except Exception as e:
            LOGGER.warning(f"Could not load Buddha mask: {e}")

    # Create custom colormap with Buddha-inspired golden/red colors
    colors = ['#FFD700', '#FFA500', '#FF8C00', '#FF6347', '#DC143C', '#B8860B']
    cmap = LinearSegmentedColormap.from_list('buddha', colors, N=256)

    # Theme settings
    if theme == "dark":
        background_color = "#1a0f0a"  # Deep warm dark background
        facecolor = "#1a0f0a"
        text_color = "white"
        bbox_props = dict(boxstyle='round', facecolor='#1a0f0a', alpha=0.8, edgecolor='#FFD700')
    else:  # light theme
        background_color = "white"
        facecolor = "white"
        text_color = "black"
        bbox_props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')

    # Create word cloud
    wordcloud = WordCloud(
        font_path=font_path_str,
        width=width,
        height=height,
        background_color=background_color,
        max_words=max_words,
        colormap=cmap,
        collocations=False,
        margin=10,
        normalize_plurals=False,
        include_numbers=False,
        mask=mask_image,
        regexp=r"[\u0E00-\u0E7F]+",
    ).generate_from_frequencies(word_freq)

    # Convert to image with theme-appropriate background
    plt.figure(figsize=(12, 8), facecolor=facecolor)
    ax = plt.gca()
    ax.set_facecolor(facecolor)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Add title text in top-right corner if provided
    if title:
        plt.text(0.98, 0.98, title,
                 transform=ax.transAxes,
                 fontsize=10,
                 verticalalignment='top',
                 horizontalalignment='right',
                 color=text_color,
                 bbox=bbox_props)

    buf = io.BytesIO()
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200, facecolor=facecolor)
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

