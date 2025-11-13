"""Chart visualizations for emotion analysis."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Optional, Dict

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
    height: int = 400
) -> go.Figure:
    """
    Create a bar chart for emotion scores.
    
    Args:
        emotion_data: Dictionary mapping emotion names to scores
        title: Chart title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    emotions = list(emotion_data.keys())
    scores = list(emotion_data.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=emotions,
            y=scores,
            marker_color='rgb(31, 119, 180)',
            text=[f"{s:.3f}" for s in scores],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Emotion",
        yaxis_title="Score",
        height=height,
        showlegend=False
    )
    
    return fig

def create_emotion_bar_chart_from_df(
    df: pd.DataFrame,
    emotion_columns: Optional[List[str]] = None,
    title: str = "Emotion Distribution"
) -> go.Figure:
    """Create bar chart from DataFrame."""
    if emotion_columns is None:
        emotion_columns = EMOTIONS
    
    emotion_data = {emotion: df[emotion].iloc[0] if emotion in df.columns else 0.0 
                   for emotion in emotion_columns}
    
    return create_emotion_bar_chart(emotion_data, title)

def create_cluster_pie_chart(
    cluster_counts: pd.Series,
    title: str = "Cluster Distribution",
    height: int = 400
) -> go.Figure:
    """
    Create a pie chart for cluster distribution.
    
    Args:
        cluster_counts: Series with cluster labels as index and counts as values
        title: Chart title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure(data=[go.Pie(
        labels=[f"Cluster {i}" for i in cluster_counts.index],
        values=cluster_counts.values,
        hole=0.3
    )])
    
    fig.update_layout(
        title=title,
        height=height
    )
    
    return fig

def create_pos_distribution_chart(
    pos_data: pd.DataFrame,
    title: str = "POS Distribution",
    height: int = 400
) -> go.Figure:
    """
    Create a bar chart for POS tag distribution.
    
    Args:
        pos_data: DataFrame with POS tags and counts
        title: Chart title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if 'pos_tag' in pos_data.columns and 'count' in pos_data.columns:
        fig = go.Figure(data=[
            go.Bar(
                x=pos_data['pos_tag'],
                y=pos_data['count'],
                marker_color='rgb(255, 127, 14)'
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
                    marker_color='rgb(255, 127, 14)'
                )
            ])
        else:
            # Return empty figure
            fig = go.Figure()
    
    fig.update_layout(
        title=title,
        xaxis_title="POS Tag",
        yaxis_title="Count",
        height=height,
        showlegend=False
    )
    
    return fig

def create_ner_distribution_chart(
    ner_data: pd.DataFrame,
    title: str = "NER Distribution",
    height: int = 400
) -> go.Figure:
    """
    Create a bar chart for NER entity distribution.
    
    Args:
        ner_data: DataFrame with entity types and counts
        title: Chart title
        height: Chart height in pixels
    
    Returns:
        Plotly figure object
    """
    if 'entity_type' in ner_data.columns and 'count' in ner_data.columns:
        fig = go.Figure(data=[
            go.Bar(
                x=ner_data['entity_type'],
                y=ner_data['count'],
                marker_color='rgb(44, 160, 44)'
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
                    marker_color='rgb(44, 160, 44)'
                )
            ])
        else:
            fig = go.Figure()
    
    fig.update_layout(
        title=title,
        xaxis_title="Entity Type",
        yaxis_title="Count",
        height=height,
        showlegend=False
    )
    
    return fig

