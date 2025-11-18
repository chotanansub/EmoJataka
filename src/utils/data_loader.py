"""Data loading utilities for CSV files."""

import pandas as pd
from typing import Optional, Dict, Any
from .config import (
    get_data_path,
    EMOTIONS,
    DATA_MODE,
)


def _resolve_mode(mode: Optional[str] = None) -> str:
    if mode:
        return mode.lower()
    return (DATA_MODE or "real").lower()


def load_csv(filename: str, mode: Optional[str] = None, **kwargs) -> pd.DataFrame:
    """
    Load a CSV file using the configured data mode.

    Args:
        filename: Name of the CSV file to load.
        mode: Optional override for the data mode ("real", "mockup", "adaptive").
        **kwargs: Additional arguments passed to ``pandas.read_csv``.
    """
    resolved_mode = _resolve_mode(mode)
    filepath = get_data_path(filename, mode=resolved_mode)

    if filepath.exists():
        return pd.read_csv(filepath, **kwargs)

    if resolved_mode == "adaptive":
        real_path = get_data_path(filename, mode="real")
        mockup_path = get_data_path(filename, mode="mockup")
        raise FileNotFoundError(
            f"Data file '{filename}' not found.\n"
            f"- Expected real data path: {real_path}\n"
            f"- Expected mockup data path: {mockup_path}"
        )

    raise FileNotFoundError(f"Data file not found: {filepath}")

def load_stories() -> pd.DataFrame:
    """Load the jataka stories dataset."""
    return load_csv("jataka_stories.csv")

def load_emotion_scores() -> pd.DataFrame:
    """
    Load emotion scores for all chapters from chapter_emotions.csv.

    Returns:
        DataFrame with columns: chapter_id, pred_anger, pred_anticipation,
        pred_disgust, pred_fear, pred_joy, pred_sadness, pred_surprise, pred_trust

    Note: The column names use 'pred_' prefix and the data is indexed by chapter_id.
    """
    df = load_csv("chapter_emotions.csv")

    # Rename chapter_id to chapter for consistency with other datasets
    if 'chapter_id' in df.columns:
        df = df.rename(columns={'chapter_id': 'chapter'})

    # Rename pred_* columns to match expected emotion names (without pred_ prefix)
    emotion_mapping = {
        'pred_anger': 'anger',
        'pred_anticipation': 'anticipation',
        'pred_disgust': 'disgust',
        'pred_fear': 'fear',
        'pred_joy': 'joy',
        'pred_sadness': 'sadness',
        'pred_surprise': 'surprise',
        'pred_trust': 'trust'
    }

    df = df.rename(columns=emotion_mapping)

    return df

def load_cluster_assignments() -> pd.DataFrame:
    """Load cluster assignments for chapters."""
    return load_csv("cluster_assignments.csv")

def load_cluster_emotions() -> pd.DataFrame:
    """Load emotion statistics by cluster."""
    return load_csv("cluster_emotions.csv")

def load_overall_emotions() -> pd.DataFrame:
    """Load overall emotion statistics."""
    return load_csv("overall_emotions.csv")

def load_text_statistics() -> pd.DataFrame:
    """Load text statistics."""
    return load_csv("text_statistics.csv")

def load_pos_distribution() -> pd.DataFrame:
    """Load POS distribution data."""
    return load_csv("pos_distribution.csv")

def load_pos_by_chapter() -> pd.DataFrame:
    """Load POS data by chapter."""
    return load_csv("pos_by_chapter.csv")

def load_pos_by_cluster() -> pd.DataFrame:
    """Load POS data by cluster."""
    return load_csv("pos_by_cluster.csv")

def load_ner_entities() -> pd.DataFrame:
    """Load NER entities."""
    return load_csv("ner_entities.csv")

def load_ner_by_chapter() -> pd.DataFrame:
    """Load NER data by chapter."""
    return load_csv("ner_by_chapter.csv")

def load_ner_counts() -> pd.DataFrame:
    """Load NER counts."""
    return load_csv("ner_counts.csv")

def load_word_frequencies() -> pd.DataFrame:
    """Load word frequencies."""
    return load_csv("word_frequencies.csv")

def load_word_freq_by_cluster() -> pd.DataFrame:
    """Load word frequencies by cluster."""
    return load_csv("word_freq_by_cluster.csv")

def load_word_freq_by_emotion() -> pd.DataFrame:
    """Load word frequencies by emotion."""
    return load_csv("word_freq_by_emotion.csv")

def load_word_freq_by_pos() -> pd.DataFrame:
    """Load word frequencies by POS tag."""
    return load_csv("word_freq_by_pos.csv")

def load_word_freq_by_ner() -> pd.DataFrame:
    """Load word frequencies by NER entity type."""
    return load_csv("word_freq_by_ner.csv")

def load_emotion_words_found() -> pd.DataFrame:
    """Load emotion words found in text."""
    return load_csv("emotion_words_found.csv")

def load_chapter_similarity() -> pd.DataFrame:
    """Load chapter similarity matrix."""
    return load_csv("chapter_similarity.csv")

def load_cluster_visualization() -> pd.DataFrame:
    """Load cluster visualization data (2D coordinates)."""
    return load_csv("cluster_visualization.csv")

def get_dataset_stats() -> Dict[str, Any]:
    """Get overall dataset statistics."""
    try:
        stories = load_stories()
        text_stats = load_text_statistics()
        
        total_chapters = len(stories)
        total_stories = stories.get('story_id', stories.index).nunique() if 'story_id' in stories.columns else total_chapters
        
        # Get word counts from text_stats if available
        total_words = text_stats['total_words'].sum() if 'total_words' in text_stats.columns else 0
        avg_words = text_stats['total_words'].mean() if 'total_words' in text_stats.columns else 0
        
        return {
            'total_stories': total_stories,
            'total_chapters': total_chapters,
            'total_words': int(total_words),
            'avg_words_per_chapter': int(avg_words),
            'language': 'Thai'
        }
    except Exception as e:
        # Return defaults if data not available
        return {
            'total_stories': 300,
            'total_chapters': 313,
            'total_words': 0,
            'avg_words_per_chapter': 0,
            'language': 'Thai'
        }

