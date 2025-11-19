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
    "joy",
    "trust",
    "fear",
     "surprise",
    "sadness",
    "disgust",
    "anger",
    "anticipation",
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
        # For scaled scores, use 0-0.6 range to make differences more visible
        max_range = 0.5

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

def create_comparison_star_plot(
    primary_scores: Dict[str, float],
    comparison_scores: Dict[str, float],
    primary_label: str = "Selected",
    comparison_label: str = "Overall",
    title: str = "Emotion Comparison",
    height: int = 500,
    theme: str = "light",
    scaling: str = "minmax"
) -> go.Figure:
    """
    Create a star plot with two overlaid traces for comparison.

    Args:
        primary_scores: Dictionary mapping emotion names to scores (main data)
        comparison_scores: Dictionary mapping emotion names to scores (comparison data)
        primary_label: Label for the primary trace
        comparison_label: Label for the comparison trace
        title: Plot title
        height: Plot height in pixels
        theme: Theme for the plot ("light" or "dark")
        scaling: Scaling method ("minmax", "baseline", or "raw")

    Returns:
        Plotly figure object
    """
    # Apply scaling to both sets of scores
    scaled_primary, raw_primary = scale_emotion_scores(primary_scores, method=scaling)
    scaled_comparison, raw_comparison = scale_emotion_scores(comparison_scores, method=scaling)

    # Get scores for plotting
    primary_vals = [scaled_primary.get(emotion, 0.0) for emotion in EMOTIONS]
    comparison_vals = [scaled_comparison.get(emotion, 0.0) for emotion in EMOTIONS]
    raw_primary_vals = [raw_primary.get(emotion, 0.0) for emotion in EMOTIONS]
    raw_comparison_vals = [raw_comparison.get(emotion, 0.0) for emotion in EMOTIONS]

    # Close the polygons
    primary_closed = primary_vals + [primary_vals[0]]
    comparison_closed = comparison_vals + [comparison_vals[0]]
    emotions_closed = [e.title() for e in EMOTIONS] + [EMOTIONS[0].title()]

    # Create hover texts
    primary_hover = [
        f"{primary_label} - " + format_score_display(emotion, scaled_primary.get(emotion, 0.0),
                                                      raw_primary.get(emotion, 0.0), scaling)
        for emotion in EMOTIONS
    ]
    primary_hover_closed = primary_hover + [primary_hover[0]]

    comparison_hover = [
        f"{comparison_label} - " + format_score_display(emotion, scaled_comparison.get(emotion, 0.0),
                                                         raw_comparison.get(emotion, 0.0), scaling)
        for emotion in EMOTIONS
    ]
    comparison_hover_closed = comparison_hover + [comparison_hover[0]]

    # Theme-specific colors
    if theme == "dark":
        primary_line = '#FFD700'  # Golden for primary
        primary_fill = 'rgba(255, 215, 0, 0.3)'
        comparison_line = '#87CEEB'  # Sky blue for comparison
        comparison_fill = 'rgba(135, 206, 235, 0.15)'
        bg_color = '#1a0f0a'
        grid_color = '#4a4a4a'
        text_color = '#FFFFFF'
        paper_bg = '#0e0e0e'
    else:
        primary_line = 'rgb(31, 119, 180)'  # Blue for primary
        primary_fill = 'rgba(31, 119, 180, 0.3)'
        comparison_line = 'rgb(255, 127, 14)'  # Orange for comparison
        comparison_fill = 'rgba(255, 127, 14, 0.15)'
        bg_color = '#FFFFFF'
        grid_color = '#E5E5E5'
        text_color = '#1F1F1F'
        paper_bg = '#FFFFFF'

    # Create polar plot with two traces
    fig = go.Figure()

    # Add comparison trace first (background)
    fig.add_trace(go.Scatterpolar(
        r=comparison_closed,
        theta=emotions_closed,
        fill='toself',
        name=comparison_label,
        line_color=comparison_line,
        fillcolor=comparison_fill,
        line_width=2,
        line_dash='dash',
        text=comparison_hover_closed,
        hovertemplate='%{text}<extra></extra>'
    ))

    # Add primary trace on top (foreground)
    fig.add_trace(go.Scatterpolar(
        r=primary_closed,
        theta=emotions_closed,
        fill='toself',
        name=primary_label,
        line_color=primary_line,
        fillcolor=primary_fill,
        line_width=2,
        text=primary_hover_closed,
        hovertemplate='%{text}<extra></extra>'
    ))

    # Set radial axis range based on scaling method
    if scaling == 'raw':
        max_range = max(max(primary_vals), max(comparison_vals)) * 1.1
        max_range = max_range if max_range > 0 else 0.2
    else:
        max_range = 0.75

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
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color)
        ),
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

