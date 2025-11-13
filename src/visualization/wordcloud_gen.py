"""Word cloud generation utilities."""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from typing import Dict, Optional
import io
import base64

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
        ax.text(0.5, 0.5, "No data available", ha='center', va='center')
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
        colormap='viridis'
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

