"""Star plot visualization for emotion profiles."""

import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Optional

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
    height: int = 500
) -> go.Figure:
    """
    Create a star plot (radar chart) for emotion scores.
    
    Args:
        emotion_scores: Dictionary mapping emotion names to scores
        title: Plot title
        height: Plot height in pixels
    
    Returns:
        Plotly figure object
    """
    # Ensure all emotions are present
    scores = [emotion_scores.get(emotion, 0.0) for emotion in EMOTIONS]
    
    # Create angles for each emotion (8 emotions, 360 degrees)
    angles = [i * 360 / len(EMOTIONS) for i in range(len(EMOTIONS))]
    angles += [angles[0]]  # Close the polygon
    scores += [scores[0]]  # Close the polygon
    
    # Convert to radians for plotting
    import math
    theta = [math.radians(angle) for angle in angles]
    
    # Create polar plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=[e.title() for e in EMOTIONS] + [EMOTIONS[0].title()],
        fill='toself',
        name='Emotions',
        line_color='rgb(31, 119, 180)',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(scores) * 1.1 if max(scores) > 0 else 1]
            ),
            angularaxis=dict(
                direction="counterclockwise",
                rotation=90
            )
        ),
        showlegend=False,
        title=title,
        height=height,
        font=dict(size=12)
    )
    
    return fig

def create_star_plot_from_df(
    df: pd.DataFrame,
    emotion_columns: Optional[List[str]] = None,
    title: str = "Emotion Profile"
) -> go.Figure:
    """
    Create star plot from DataFrame with emotion columns.
    
    Args:
        df: DataFrame with emotion columns
        emotion_columns: List of emotion column names (defaults to EMOTIONS)
        title: Plot title
    
    Returns:
        Plotly figure object
    """
    if emotion_columns is None:
        emotion_columns = EMOTIONS
    
    # Get first row's emotion scores
    emotion_scores = {emotion: df[emotion].iloc[0] if emotion in df.columns else 0.0 
                     for emotion in emotion_columns}
    
    return create_star_plot(emotion_scores, title)

