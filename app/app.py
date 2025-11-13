"""Main Streamlit app - Component Loader and Router."""

import streamlit as st
from pathlib import Path
import sys
import importlib.util

# Add src to path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

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

# Import components
sys.path.insert(0, str(Path(__file__).parent / "components"))
from sidebar import render_sidebar

# Import pages module
sys.path.insert(0, str(Path(__file__).parent))

def load_page(page_name):
    """Dynamically load and execute a page module."""
    try:
        pages_dir = Path(__file__).parent / "pages"
        page_file = pages_dir / f"{page_name}.py"
        
        if not page_file.exists():
            st.error(f"Page not found: {page_name}")
            return
        
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(page_name, page_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Execute the render function if it exists
        if hasattr(module, 'render'):
            module.render()
        # Otherwise, the page script has already executed
        
    except Exception as e:
        st.error(f"Error loading page {page_name}: {e}")
        import traceback
        st.code(traceback.format_exc())

# Render sidebar and get selected page
selected_page = render_sidebar()

# Page routing - map sidebar selection to page files
page_routes = {
    "overview": "page_overview",
    "emotion_analysis": "page_emotion_analysis",
    "story_groups": "page_story_groups",
    "story_explorer": "page_story_explorer",
    "text_insights": "page_text_insights"
}

# Load the selected page
if selected_page and selected_page in page_routes:
    load_page(page_routes[selected_page])
else:
    # Default home page content (when no page is selected or overview is selected)
    if not selected_page or selected_page == "overview":
        load_page("page_overview")