"""Chart visualizations for emotion analysis."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Optional, Dict
import sys
from pathlib import Path

# Add src to path for importing utilities
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

def create_emotion_bar_chart(
    emotion_data: Dict[str, float],
    title: str = "Emotion Distribution",
    height: int = 400,
    theme: str = "light",
    scaling: str = "minmax"
) -> go.Figure:
    """
    Create a bar chart for emotion scores.

    Args:
        emotion_data: Dictionary mapping emotion names to scores
        title: Chart title
        height: Chart height in pixels
        theme: Theme for the chart ("light" or "dark")
        scaling: Scaling method ("minmax", "baseline", or "raw")

    Returns:
        Plotly figure object
    """
    # Apply scaling to highlight differences
    scaled_scores, raw_scores = scale_emotion_scores(emotion_data, method=scaling)

    emotions = list(scaled_scores.keys())
    scores = list(scaled_scores.values())
    raw_vals = list(raw_scores.values())

    # Theme-specific colors
    if theme == "dark":
        bar_color = '#FFD700'  # Golden
        bg_color = '#0e0e0e'  # Very dark background
        paper_bg = '#0e0e0e'
        text_color = '#FFFFFF'
        grid_color = '#4a4a4a'
    else:
        bar_color = 'rgb(31, 119, 180)'  # Blue
        bg_color = '#FFFFFF'
        paper_bg = '#FFFFFF'
        text_color = '#1F1F1F'
        grid_color = '#E5E5E5'

    # Create hover text and bar labels
    if scaling == 'raw':
        bar_text = [f"{s:.4f}" for s in scores]
        hover_text = [f"{e.title()}: {s:.4f}" for e, s in zip(emotions, scores)]
    else:
        bar_text = [f"{s:.3f}" for s in scores]
        hover_text = [
            format_score_display(e, s, r, scaling)
            for e, s, r in zip(emotions, scores, raw_vals)
        ]

    fig = go.Figure(data=[
        go.Bar(
            x=emotions,
            y=scores,
            marker_color=bar_color,
            text=bar_text,
            textposition='auto',
            hovertext=hover_text,
            hovertemplate='%{hovertext}<extra></extra>'
        )
    ])

    fig.update_layout(
        title=dict(text=title, font=dict(color=text_color)),
        xaxis_title="Emotion",
        yaxis_title="Score",
        height=height,
        showlegend=False,
        paper_bgcolor=paper_bg,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color, color=text_color),
        yaxis=dict(gridcolor=grid_color, color=text_color)
    )

    return fig

def create_emotion_bar_chart_from_df(
    df: pd.DataFrame,
    emotion_columns: Optional[List[str]] = None,
    title: str = "Emotion Distribution",
    theme: str = "light",
    scaling: str = "minmax"
) -> go.Figure:
    """Create bar chart from DataFrame."""
    if emotion_columns is None:
        emotion_columns = EMOTIONS

    emotion_data = {emotion: df[emotion].iloc[0] if emotion in df.columns else 0.0
                   for emotion in emotion_columns}

    return create_emotion_bar_chart(emotion_data, title, theme=theme, scaling=scaling)

def create_cluster_pie_chart(
    cluster_counts: pd.Series,
    title: str = "Cluster Distribution",
    height: int = 400,
    theme: str = "light"
) -> go.Figure:
    """
    Create a pie chart for cluster distribution.

    Args:
        cluster_counts: Series with cluster labels as index and counts as values
        title: Chart title
        height: Chart height in pixels
        theme: Theme for the chart ("light" or "dark")

    Returns:
        Plotly figure object
    """
    # Theme-specific colors
    if theme == "dark":
        paper_bg = '#0e0e0e'
        text_color = '#FFFFFF'
    else:
        paper_bg = '#FFFFFF'
        text_color = '#1F1F1F'

    fig = go.Figure(data=[go.Pie(
        labels=[f"Cluster {i}" for i in cluster_counts.index],
        values=cluster_counts.values,
        hole=0.3
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(color=text_color)),
        height=height,
        paper_bgcolor=paper_bg,
        font=dict(color=text_color)
    )

    return fig

def create_pos_distribution_chart(
    pos_data: pd.DataFrame,
    title: str = "POS Distribution",
    height: int = 400,
    theme: str = "light"
) -> go.Figure:
    """
    Create a bar chart for POS tag distribution.

    Args:
        pos_data: DataFrame with POS tags and counts
        title: Chart title
        height: Chart height in pixels
        theme: Theme for the chart ("light" or "dark")

    Returns:
        Plotly figure object
    """
    # Theme-specific colors
    if theme == "dark":
        bar_color = '#FFA500'  # Orange for dark theme
        bg_color = '#0e0e0e'
        paper_bg = '#0e0e0e'
        text_color = '#FFFFFF'
        grid_color = '#4a4a4a'
    else:
        bar_color = 'rgb(255, 127, 14)'  # Orange
        bg_color = '#FFFFFF'
        paper_bg = '#FFFFFF'
        text_color = '#1F1F1F'
        grid_color = '#E5E5E5'

    if 'pos_tag' in pos_data.columns and 'count' in pos_data.columns:
        fig = go.Figure(data=[
            go.Bar(
                x=pos_data['pos_tag'],
                y=pos_data['count'],
                marker_color=bar_color
            )
        ])
    else:
        # Try to use first two columns
        cols = pos_data.columns.tolist()
        if len(cols) >= 2:
            fig = go.Figure(data=[
                go.Bar(
                    x=pos_data[cols[0]],
                    y=pos_data[cols[1]],
                    marker_color=bar_color
                )
            ])
        else:
            # Return empty figure
            fig = go.Figure()

    fig.update_layout(
        title=dict(text=title, font=dict(color=text_color)),
        xaxis_title="POS Tag",
        yaxis_title="Count",
        height=height,
        showlegend=False,
        paper_bgcolor=paper_bg,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color, color=text_color),
        yaxis=dict(gridcolor=grid_color, color=text_color)
    )

    return fig

def create_ner_distribution_chart(
    ner_data: pd.DataFrame,
    title: str = "NER Distribution",
    height: int = 400,
    theme: str = "light"
) -> go.Figure:
    """
    Create a bar chart for NER entity distribution.

    Args:
        ner_data: DataFrame with entity types and counts
        title: Chart title
        height: Chart height in pixels
        theme: Theme for the chart ("light" or "dark")

    Returns:
        Plotly figure object
    """
    # Theme-specific colors
    if theme == "dark":
        bar_color = '#90EE90'  # Light green for dark theme
        bg_color = '#0e0e0e'
        paper_bg = '#0e0e0e'
        text_color = '#FFFFFF'
        grid_color = '#4a4a4a'
    else:
        bar_color = 'rgb(44, 160, 44)'  # Green
        bg_color = '#FFFFFF'
        paper_bg = '#FFFFFF'
        text_color = '#1F1F1F'
        grid_color = '#E5E5E5'

    if 'entity_type' in ner_data.columns and 'count' in ner_data.columns:
        fig = go.Figure(data=[
            go.Bar(
                x=ner_data['entity_type'],
                y=ner_data['count'],
                marker_color=bar_color
            )
        ])
    else:
        # Try to use first two columns
        cols = ner_data.columns.tolist()
        if len(cols) >= 2:
            fig = go.Figure(data=[
                go.Bar(
                    x=ner_data[cols[0]],
                    y=ner_data[cols[1]],
                    marker_color=bar_color
                )
            ])
        else:
            fig = go.Figure()

    fig.update_layout(
        title=dict(text=title, font=dict(color=text_color)),
        xaxis_title="Entity Type",
        yaxis_title="Count",
        height=height,
        showlegend=False,
        paper_bgcolor=paper_bg,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color, color=text_color),
        yaxis=dict(gridcolor=grid_color, color=text_color)
    )

    return fig

