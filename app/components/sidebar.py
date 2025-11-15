"""Enhanced sidebar component with independent navigation."""

import streamlit as st
from pathlib import Path
import sys

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def hide_streamlit_elements():
    """Hide Streamlit's default elements."""
    st.markdown("""
        <style>
        /* Hide default Streamlit navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        section[data-testid="stSidebarNav"] {
            display: none !important;
        }
        /* Hide hamburger menu */
        #MainMenu {
            visibility: hidden;
        }
        /* Hide footer */
        footer {
            visibility: hidden;
        }
        /* Adjust sidebar spacing */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the custom sidebar with navigation."""
    
    # Hide default Streamlit elements
    hide_streamlit_elements()
    
    # Initialize session state for selected page
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'overview'
    
    # Header with gradient
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 1.5rem 0.5rem; 
                    background: linear-gradient(135deg, #FF6B35 0%, #D84315 100%); 
                    border-radius: 12px; margin-bottom: 1.5rem; 
                    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.8rem; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>🪷</h1>
            <h2 style='color: white; margin: 0.5rem 0 0 0; font-size: 1.4rem; 
                       font-weight: 600; letter-spacing: 0.5px;'>Jataka Tales</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 0.3rem 0 0 0; 
                      font-size: 0.9rem; font-weight: 300;'>
                Emotion Analysis Dashboard
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation section
    st.sidebar.markdown("### 🧭 Navigation")
    
    # Define navigation items (independent of file names)
    nav_items = [
        {
            "id": "overview",
            "icon": "🪷",
            "title": "Overview",
            "description": "Dataset summary & statistics"
        },
        {
            "id": "emotion_analysis",
            "icon": "🌟",
            "title": "Emotion Analysis",
            "description": "Explore emotion profiles & patterns"
        },
        {
            "id": "story_groups",
            "icon": "🎭",
            "title": "Story Groups",
            "description": "View clusters & groupings"
        },
        {
            "id": "story_explorer",
            "icon": "📖",
            "title": "Story Explorer",
            "description": "Search & browse chapters"
        },
        {
            "id": "text_insights",
            "icon": "📊",
            "title": "Text Insights",
            "description": "Word clouds & text analysis"
        }
    ]
    
    # Create simple selectbox for navigation
    nav_options = {f"{item['icon']} {item['title']}": item['id'] for item in nav_items}
    
    # Find current selection for display
    current_display = None
    for display, page_id in nav_options.items():
        if page_id == st.session_state.selected_page:
            current_display = display
            break
    
    if current_display is None:
        current_display = list(nav_options.keys())[0]
    
    # Use selectbox for navigation
    selected_display = st.sidebar.selectbox(
        "Choose a page",
        options=list(nav_options.keys()),
        index=list(nav_options.keys()).index(current_display),
        key="page_selector"
    )
    
    # Update session state
    selected_id = nav_options[selected_display]
    if selected_id != st.session_state.selected_page:
        st.session_state.selected_page = selected_id
        st.rerun()
    
    # Show description of selected page
    current_item = [item for item in nav_items if item['id'] == selected_id][0]
    st.sidebar.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 0.8rem; 
                    border-radius: 8px; margin-top: 0.5rem;'>
            <p style='margin: 0; font-size: 0.85rem; color: #666;'>
                {current_item['description']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Quick stats section
    st.sidebar.markdown("### 📊 Quick Stats")
    
    try:
        from utils.data_loader import get_dataset_stats
        stats = get_dataset_stats()
        
        st.sidebar.markdown(f"""
            <div style='background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
                        padding: 1.3rem; border-radius: 12px; color: white;
                        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);'>
                <div style='display: flex; justify-content: space-between;
                            align-items: center; margin-bottom: 0.7rem;
                            padding-bottom: 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.3);'>
                    <span style='font-size: 0.95rem; display: flex; align-items: center;'>
                        <span style='font-size: 1.3rem; margin-right: 0.6rem;'>📖</span> Stories
                    </span>
                    <strong style='font-size: 1.2rem;'>{stats['total_stories']}</strong>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-size: 0.95rem; display: flex; align-items: center;'>
                        <span style='font-size: 1.3rem; margin-right: 0.6rem;'>💬</span> Words
                    </span>
                    <strong style='font-size: 1.2rem;'>{stats['total_words']:,}</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.sidebar.markdown("""
            <div style='background: linear-gradient(135deg, #FF8A65 0%, #FFAB91 100%);
                        padding: 1.3rem; border-radius: 12px;
                        box-shadow: 0 4px 12px rgba(255, 138, 101, 0.3);'>
                <p style='margin: 0; font-size: 0.95rem; color: #3E2723;
                          line-height: 2; font-weight: 500;'>
                    📖 <strong>314</strong> Stories<br>
                    🌏 <strong>Thai</strong> Language
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # 8 Emotions legend with enhanced styling
    st.sidebar.markdown("### 💭 Emotions")
    
    emotions = [
        ("🤝", "Trust", "#1f77b4"),
        ("😊", "Joy", "#ff7f0e"),
        ("😠", "Anger", "#d62728"),
        ("⏳", "Anticipation", "#9467bd"),
        ("😨", "Fear", "#8c564b"),
        ("🤢", "Disgust", "#e377c2"),
        ("😲", "Surprise", "#7f7f7f"),
        ("😢", "Sadness", "#17becf")
    ]
    
    # Display in 2-column layout using Streamlit columns
    for i in range(0, len(emotions), 2):
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if i < len(emotions):
                icon, name, color = emotions[i]
                st.markdown(
                    f"<div style='text-align: center; padding: 0.4rem; "
                    f"background: {color}20; border-radius: 8px; "
                    f"border-left: 3px solid {color};'>"
                    f"<span style='font-size: 1.1rem;'>{icon}</span><br>"
                    f"<span style='font-size: 0.75rem; color: {color}; font-weight: 600;'>{name}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        
        with col2:
            if i + 1 < len(emotions):
                icon, name, color = emotions[i + 1]
                st.markdown(
                    f"<div style='text-align: center; padding: 0.4rem; "
                    f"background: {color}20; border-radius: 8px; "
                    f"border-left: 3px solid {color};'>"
                    f"<span style='font-size: 1.1rem;'>{icon}</span><br>"
                    f"<span style='font-size: 0.75rem; color: {color}; font-weight: 600;'>{name}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    
    st.sidebar.markdown("---")
    
    # About section
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
        <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%); 
                    padding: 1.2rem; border-radius: 10px; 
                    border-left: 4px solid #ffc107; 
                    box-shadow: 0 4px 8px rgba(255, 193, 7, 0.2);'>
            <p style='margin: 0; font-size: 0.88rem; color: #856404; 
                      line-height: 1.7; font-weight: 400;'>
                Analyzing emotions in <strong>300 Jataka tales</strong> using the 
                <strong>NRC Emotion Lexicon</strong>. Discover emotion patterns in 
                Buddhist narratives through interactive visualizations.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style='text-align: center; font-size: 0.75rem; color: #999; 
                    padding: 1rem 0; line-height: 1.6;'>
            <p style='margin: 0;'>Built with <span style='color: #ff4b4b;'>❤️</span> 
               using <strong>Streamlit</strong></p>
            <p style='margin: 0.4rem 0 0 0;'>Text Analytics Project 2024</p>
        </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.selected_page