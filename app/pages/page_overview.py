"""Overview page for the Jataka Emotion Analysis app."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path - handle both running from root and from app directory
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.data_loader import get_dataset_stats, load_emotion_scores
from utils.emotion_scaling import get_scaling_description
from visualization.charts import create_emotion_bar_chart

# Import components from app directory
components_path = Path(__file__).parent.parent / "components"
if str(components_path) not in sys.path:
    sys.path.insert(0, str(components_path))
from metrics_cards import render_metrics_row

st.set_page_config(
    page_title="Overview - Jataka Emotion Analysis",
    page_icon="🪷",
    layout="wide"
)

st.title("🪷 Overview")

# Global controls for all plots on this page
col_theme, col_scaling = st.columns(2)

with col_theme:
    plot_theme = st.selectbox(
        "🎨 Plot Theme",
        options=["light", "dark"],
        format_func=lambda x: "☀️ Light" if x == "light" else "🌙 Dark",
        key="overview_global_theme"
    )

with col_scaling:
    scaling_method = st.selectbox(
        "📊 Score Display",
        options=["minmax", "baseline", "raw"],
        format_func=lambda x: {
            "minmax": "Highlight Differences (Min-Max)",
            "baseline": "Above/Below Baseline",
            "raw": "Raw Scores"
        }[x],
        index=0,  # Default to minmax
        key="overview_scaling"
    )

# Show scaling method description
with st.expander("ℹ️ About Score Display Methods"):
    st.markdown(get_scaling_description(scaling_method))

st.markdown("---")

# Project description
st.header("📚 About This Project")
st.markdown("""
This project analyzes emotions in **314 Jataka tales** (Buddhist stories of Buddha's previous lives)
written in Thai language.

### 🎯 Core Analysis
- **Emotion Analysis**: 8 basic emotions (trust, joy, anger, anticipation, fear, disgust, surprise, sadness)
- **Analysis Levels**:
  - Overall (all stories combined)
  - Cluster-level (K-means grouped stories)
  - Story-level (individual story analysis)
- **Text Analysis**: Word clouds, POS tagging, NER, and text statistics

### 🔧 Technical Approach
- **Emotion Detection**: Lexicon-based matching with NRC Thai lexicon
- **Clustering**: K-means on TF-IDF features for story grouping
- **NLP Processing**: PyThaiNLP for tokenization, POS tagging, and NER
- **Visualization**: Interactive dashboard with star plots, word clouds, and charts
""")

st.markdown("---")

# Dataset statistics
st.header("📊 Dataset Quick Facts")

try:
    stats = get_dataset_stats()

    metrics = [
        ("Total Stories", str(stats['total_stories']), "Number of Jataka tales in the dataset"),
        ("Total Words", f"{stats['total_words']:,}", "Total word count across all stories"),
        ("Avg Words/Story", f"{stats['avg_words_per_chapter']:,}", "Average words per story"),
        ("Language", stats['language'], "Primary language of the dataset"),
        ("Emotions", "8", "Basic emotions analyzed (NRC lexicon)")
    ]

    render_metrics_row(metrics)

except Exception as e:
    st.error(f"Error loading dataset statistics: {e}")
    st.info("Using default values. Please ensure data files are available.")

st.markdown("---")

# Overall emotion distribution
st.header("🌟 Overall Emotion Distribution")

try:
    # Load chapter emotions and calculate mean across all chapters
    chapter_emotions = load_emotion_scores()

    if not chapter_emotions.empty:
        # Get emotion columns
        emotion_cols = [col for col in chapter_emotions.columns
                       if col.lower() in ['trust', 'joy', 'anger', 'anticipation',
                                         'fear', 'disgust', 'surprise', 'sadness']]

        if emotion_cols:
            # Calculate mean emotion scores across all chapters
            emotion_data = {col: chapter_emotions[col].mean()
                          for col in emotion_cols if col in chapter_emotions.columns}

            fig = create_emotion_bar_chart(emotion_data, "Overall Emotion Scores (Mean Across All Chapters)",
                                          theme=plot_theme, scaling=scaling_method)
            st.plotly_chart(fig, use_container_width=True, key="overview_emotion_bar")

            # Key insights
            max_emotion = max(emotion_data.items(), key=lambda x: x[1])
            min_emotion = min(emotion_data.items(), key=lambda x: x[1])
            
            st.info(f"""
            **Key Insights:**
            - Highest emotion: **{max_emotion[0].title()}** ({max_emotion[1]:.3f})
            - Lowest emotion: **{min_emotion[0].title()}** ({min_emotion[1]:.3f})
            """)
        else:
            st.warning("Emotion columns not found in overall_emotions.csv")
    else:
        st.warning("Overall emotions data is empty.")
        
except FileNotFoundError:
    st.info("📝 Overall emotion data not found. Please generate the data files first.")
except Exception as e:
    st.error(f"Error loading overall emotions: {e}")

st.markdown("---")

# What you can explore
st.header("🔍 What You Can Explore")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌟 Emotion Analysis
    - View emotion profiles across all stories
    - Compare emotions by story groups (clusters)
    - Analyze individual story emotions
    - Interactive star plots and bar charts
    """)
    
    st.markdown("""
    ### 🎭 Story Groups
    - Explore K-means clusters
    - Visualize story groupings in 2D
    - Compare emotion patterns across clusters
    """)

with col2:
    st.markdown("""
    ### 📖 Story Explorer
    - Search and browse individual chapters
    - View detailed emotion profiles
    - Find similar stories
    - Read story text previews
    """)
    
    st.markdown("""
    ### 📊 Text Insights
    - Word clouds by cluster and emotion
    - POS tag distribution
    - Named entity recognition results
    - Language pattern analysis
    """)

