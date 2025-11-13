"""Metrics cards component for displaying statistics."""

import streamlit as st

def render_metric_card(label: str, value: str, help_text: str = ""):
    """
    Render a metric card.
    
    Args:
        label: Label for the metric
        value: Value to display
        help_text: Optional help text
    """
    st.metric(label=label, value=value, help=help_text)

def render_metrics_row(metrics: list):
    """
    Render a row of metric cards.
    
    Args:
        metrics: List of tuples (label, value, help_text)
    """
    cols = st.columns(len(metrics))
    for i, (label, value, help_text) in enumerate(metrics):
        with cols[i]:
            render_metric_card(label, value, help_text)

