"""Main Streamlit app for Jataka Tales Emotion Analysis."""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Jataka Tales Emotion Analysis",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path(__file__).parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main title
st.title("📚 Jataka Tales Emotion Analysis")
st.markdown("---")

# Welcome message
st.markdown("""
Welcome to the **Jataka Tales Emotion Analysis** dashboard!

This interactive application allows you to explore emotions in 300 Jataka tales (Buddhist stories) 
using the NRC Emotion Lexicon. Navigate through the pages using the sidebar to discover:

- **Overview**: Dataset statistics and overall emotion patterns
- **Emotion Analysis**: Detailed emotion profiles at different levels
- **Story Groups**: K-means clusters of similar stories
- **Story Explorer**: Search and explore individual chapters
- **Text Insights**: Word clouds, POS tags, and named entities

Use the sidebar to navigate between pages.
""")

st.markdown("---")

# Quick stats
try:
    import sys
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from utils.data_loader import get_dataset_stats
    
    stats = get_dataset_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Stories", stats['total_stories'])
    
    with col2:
        st.metric("Total Chapters", stats['total_chapters'])
    
    with col3:
        st.metric("Total Words", f"{stats['total_words']:,}")
    
    with col4:
        st.metric("Language", stats['language'])
        
except Exception as e:
    st.info("📝 Please ensure data files are available. Use mockup data for testing.")

st.markdown("---")

# Instructions
st.info("""
💡 **Getting Started:**
1. Use the sidebar to navigate to different pages
2. If data files are not available, set `USE_MOCKUP=true` in your environment or `.env` file
3. Generate mockup data using the utilities in the `utils/mockup_generator/` directory
""")

