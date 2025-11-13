"""Sidebar component for navigation."""

import streamlit as st

def render_sidebar():
    """Render the sidebar navigation."""
    st.sidebar.title("📚 Jataka Tales")
    st.sidebar.markdown("### Emotion Analysis")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### Navigation")
    
    # Navigation links
    pages = {
        "🏠 Overview": "Overview",
        "🌟 Emotion Analysis": "Emotion_Analysis",
        "🎭 Story Groups": "Story_Groups",
        "📖 Story Explorer": "Story_Explorer",
        "📊 Text Insights": "Text_Insights"
    }
    
    selected = st.sidebar.radio(
        "Select a page",
        list(pages.keys()),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "Analyzing emotions in 300 Jataka tales using NRC Emotion Lexicon. "
        "Explore emotion patterns across Buddhist narratives."
    )
    
    return selected

