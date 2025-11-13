"""Overview page for the Jataka Emotion Analysis app."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path - handle both running from root and from app directory
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.data_loader import get_dataset_stats, load_overall_emotions
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
st.markdown("---")

# Project description
st.header("📚 Project Description")
st.markdown("""
This project analyzes emotions in **300 Jataka tales** (Buddhist stories of Buddha's previous lives).
The dataset contains **313 chapters** in Thai language.

### Core Analysis
- **Emotion Analysis**: 8 basic emotions (trust, joy, anger, anticipation, fear, disgust, surprise, sadness)
- **Analysis Levels**: 
  - Overall (all stories combined)
  - Cluster-level (K-means grouped stories)
  - Chapter-level (individual story analysis)
- **Additional Analysis**: POS tagging, NER, word frequency, text statistics

### Technical Approach
- **Emotion Detection**: Lexicon-based matching with NRC Thai lexicon
- **Clustering**: K-means on TF-IDF features
- **NLP Tools**: PyThaiNLP for tokenization, POS tagging, NER
- **Visualization**: Interactive Streamlit dashboard with star plots
""")

st.markdown("---")

# Dataset statistics
st.header("📊 Dataset Quick Facts")

try:
    stats = get_dataset_stats()
    
    metrics = [
        ("Total Stories", str(stats['total_stories']), "Number of unique Jataka stories"),
        ("Total Chapters", str(stats['total_chapters']), "Total number of chapters analyzed"),
        ("Total Words", f"{stats['total_words']:,}", "Total word count across all chapters"),
        ("Avg Words/Chapter", f"{stats['avg_words_per_chapter']:,}", "Average words per chapter"),
        ("Language", stats['language'], "Primary language of the dataset")
    ]
    
    render_metrics_row(metrics)
    
except Exception as e:
    st.error(f"Error loading dataset statistics: {e}")
    st.info("Using default values. Please ensure data files are available.")

st.markdown("---")

# Overall emotion distribution
st.header("🌟 Overall Emotion Distribution")

try:
    overall_emotions = load_overall_emotions()
    
    if not overall_emotions.empty:
        # Get emotion columns
        emotion_cols = [col for col in overall_emotions.columns 
                       if col.lower() in ['trust', 'joy', 'anger', 'anticipation', 
                                         'fear', 'disgust', 'surprise', 'sadness']]
        
        if emotion_cols:
            # Get first row's emotion scores
            emotion_data = {col: overall_emotions[col].iloc[0] 
                          for col in emotion_cols if col in overall_emotions.columns}
            
            fig = create_emotion_bar_chart(emotion_data, "Overall Emotion Scores")
            st.plotly_chart(fig, use_container_width=True)
            
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

