"""Scatter plot visualization for cluster visualization."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List

def create_cluster_scatter_plot(
    df: pd.DataFrame,
    x_col: str = 'x',
    y_col: str = 'y',
    cluster_col: str = 'cluster',
    chapter_col: Optional[str] = None,
    title: str = "Story Clusters (2D Projection)",
    height: int = 600
) -> go.Figure:
    """
    Create an interactive scatter plot for cluster visualization.
    
    Args:
        df: DataFrame with x, y coordinates and cluster assignments
        x_col: Column name for x coordinates
        y_col: Column name for y coordinates
        cluster_col: Column name for cluster labels
        chapter_col: Column name for chapter names/IDs (for hover)
        title: Plot title
        height: Plot height in pixels
    
    Returns:
        Plotly figure object
    """
    if x_col not in df.columns or y_col not in df.columns:
        # Return empty figure if required columns missing
        fig = go.Figure()
        fig.add_annotation(
            text="Visualization data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Create hover text
    hover_data = []
    if chapter_col and chapter_col in df.columns:
        hover_data.append(df[chapter_col])
    if cluster_col in df.columns:
        hover_data.append(df[cluster_col].apply(lambda x: f"Cluster {x}"))
    
    hover_text = None
    if hover_data:
        hover_text = ["<br>".join([str(h[i]) for h in hover_data]) for i in range(len(df))]
    
    # Create scatter plot
    if cluster_col in df.columns:
        # Color by cluster
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=cluster_col,
            hover_name=chapter_col if chapter_col in df.columns else None,
            hover_data={cluster_col: True},
            title=title,
            labels={x_col: "Dimension 1", y_col: "Dimension 2", cluster_col: "Cluster"},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    else:
        # Single color
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(size=8, color='rgb(31, 119, 180)'),
            text=hover_text,
            hovertemplate='%{text}<extra></extra>'
        ))
        fig.update_layout(title=title, height=height)
    
    fig.update_layout(
        height=height,
        xaxis_title="Dimension 1",
        yaxis_title="Dimension 2"
    )
    
    return fig

