"""Star plot visualization for emotion profiles."""

import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Optional

# Import scaling utilities
import sys
from pathlib import Path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.emotion_scaling import scale_emotion_scores, format_score_display

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

def create_star_plot(
    emotion_scores: Dict[str, float],
    title: str = "Emotion Profile",
    height: int = 500,
    theme: str = "light",
    scaling: str = "minmax"
) -> go.Figure:
    """
    Create a star plot (radar chart) for emotion scores.

    Args:
        emotion_scores: Dictionary mapping emotion names to scores
        title: Plot title
        height: Plot height in pixels
        theme: Theme for the plot ("light" or "dark")
        scaling: Scaling method ("minmax", "baseline", or "raw")

    Returns:
        Plotly figure object
    """
    # Apply scaling to highlight differences
    scaled_scores, raw_scores = scale_emotion_scores(emotion_scores, method=scaling)

    # Ensure all emotions are present (use scaled scores for plotting)
    scores = [scaled_scores.get(emotion, 0.0) for emotion in EMOTIONS]
    raw_vals = [raw_scores.get(emotion, 0.0) for emotion in EMOTIONS]

    # Close the polygon
    scores_closed = scores + [scores[0]]
    raw_vals_closed = raw_vals + [raw_vals[0]]
    emotions_closed = [e.title() for e in EMOTIONS] + [EMOTIONS[0].title()]

    # Create hover text with both scaled and raw values
    hover_texts = [
        format_score_display(emotion, scaled_scores.get(emotion, 0.0),
                           raw_scores.get(emotion, 0.0), scaling)
        for emotion in EMOTIONS
    ]
    hover_texts_closed = hover_texts + [hover_texts[0]]

    # Theme-specific colors
    if theme == "dark":
        # Dark theme: golden/orange Buddhist-inspired colors on dark background
        line_color = '#FFD700'  # Golden
        fill_color = 'rgba(255, 215, 0, 0.3)'  # Golden with transparency
        bg_color = '#1a0f0a'  # Deep warm dark background
        grid_color = '#4a4a4a'  # Gray grid
        text_color = '#FFFFFF'  # White text
        paper_bg = '#0e0e0e'  # Very dark paper background
    else:
        # Light theme: blue colors on white background
        line_color = 'rgb(31, 119, 180)'  # Blue
        fill_color = 'rgba(31, 119, 180, 0.3)'  # Blue with transparency
        bg_color = '#FFFFFF'  # White background
        grid_color = '#E5E5E5'  # Light gray grid
        text_color = '#1F1F1F'  # Dark text
        paper_bg = '#FFFFFF'  # White paper background

    # Create polar plot
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=emotions_closed,
        fill='toself',
        name='Emotions',
        line_color=line_color,
        fillcolor=fill_color,
        line_width=2,
        text=hover_texts_closed,
        hovertemplate='%{text}<extra></extra>'
    ))

    # Set radial axis range based on scaling method
    if scaling == 'raw':
        # For raw scores, use dynamic range
        max_range = max(scores) * 1.1 if max(scores) > 0 else 0.2
    else:
        # For scaled scores, use 0-1 range
        max_range = 1.0

    fig.update_layout(
        polar=dict(
            bgcolor=bg_color,
            radialaxis=dict(
                visible=True,
                range=[0, max_range],
                gridcolor=grid_color,
                linecolor=grid_color
            ),
            angularaxis=dict(
                direction="counterclockwise",
                rotation=90,
                gridcolor=grid_color,
                linecolor=grid_color
            )
        ),
        showlegend=False,
        title=dict(text=title, font=dict(color=text_color)),
        height=height,
        font=dict(size=12, color=text_color),
        paper_bgcolor=paper_bg,
        plot_bgcolor=bg_color
    )
    
    return fig

def create_star_plot_from_df(
    df: pd.DataFrame,
    emotion_columns: Optional[List[str]] = None,
    title: str = "Emotion Profile",
    theme: str = "light",
    scaling: str = "minmax"
) -> go.Figure:
    """
    Create star plot from DataFrame with emotion columns.

    Args:
        df: DataFrame with emotion columns
        emotion_columns: List of emotion column names (defaults to EMOTIONS)
        title: Plot title
        theme: Theme for the plot ("light" or "dark")
        scaling: Scaling method ("minmax", "baseline", or "raw")

    Returns:
        Plotly figure object
    """
    if emotion_columns is None:
        emotion_columns = EMOTIONS

    # Get first row's emotion scores
    emotion_scores = {emotion: df[emotion].iloc[0] if emotion in df.columns else 0.0
                     for emotion in emotion_columns}

    return create_star_plot(emotion_scores, title, theme=theme, scaling=scaling)

