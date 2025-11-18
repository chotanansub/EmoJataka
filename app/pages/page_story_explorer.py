"""Story Explorer page for the Jataka Emotion Analysis app."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path - handle both running from root and from app directory
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.data_loader import (
    load_stories, load_emotion_scores, load_cluster_assignments,
    load_emotion_words_found, load_chapter_similarity
)
from utils.emotion_scaling import get_scaling_description
from visualization.star_plot import create_star_plot

# Import components from app directory
components_path = Path(__file__).parent.parent / "components"
if str(components_path) not in sys.path:
    sys.path.insert(0, str(components_path))
from story_display import (
    display_story_info, display_emotion_words, display_similar_stories
)

st.set_page_config(
    page_title="Story Explorer - Jataka Emotion Analysis",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Story Explorer")

# Global controls for all plots on this page
col_theme, col_scaling = st.columns(2)

with col_theme:
    plot_theme = st.selectbox(
        "🎨 Plot Theme",
        options=["light", "dark"],
        format_func=lambda x: "☀️ Light" if x == "light" else "🌙 Dark",
        key="story_explorer_global_theme"
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
        key="story_explorer_scaling"
    )

# Show scaling method description
with st.expander("ℹ️ About Score Display Methods"):
    st.markdown(get_scaling_description(scaling_method))

st.markdown("---")

try:
    stories = load_stories()
    emotion_scores = load_emotion_scores()
    
    if stories.empty or emotion_scores.empty:
        st.warning("Stories or emotion scores data not available.")
    else:
        # Get chapter options
        if 'chapter' in stories.columns:
            chapters = sorted(stories['chapter'].unique())
        elif 'chapter' in emotion_scores.columns:
            chapters = sorted(emotion_scores['chapter'].unique())
        else:
            chapters = list(range(1, len(stories) + 1))
        
        # Create format function to show chapter with title
        def format_chapter(chapter_num):
            if 'title' in stories.columns:
                story = stories[stories['chapter'] == chapter_num]
                if not story.empty:
                    title = story.iloc[0]['title']
                    return f"Chapter {chapter_num} : {title}"
            return f"Chapter {chapter_num}"

        selected_chapter = st.selectbox(
            "🔍 Select Chapter",
            chapters,
            format_func=format_chapter
        )
        
        st.markdown("---")
        
        if selected_chapter:
            # Get story data
            story_data = stories[stories['chapter'] == selected_chapter]
            
            if not story_data.empty:
                # Chapter info
                st.header(f"Chapter {selected_chapter}")
                
                # Display story info
                display_story_info(
                    story_data.iloc[0],
                    chapter_col='chapter',
                    title_col='title' if 'title' in story_data.columns else None,
                    text_col='text' if 'text' in story_data.columns else None
                )
                
                st.markdown("---")
                
                # Emotion profile
                chapter_emotions = emotion_scores[emotion_scores['chapter'] == selected_chapter]
                
                if not chapter_emotions.empty:
                    st.subheader("🌟 Emotion Profile")

                    # Get emotion columns
                    emotion_cols = [col for col in chapter_emotions.columns
                                  if col.lower() in ['trust', 'joy', 'anger', 'anticipation',
                                                    'fear', 'disgust', 'surprise', 'sadness']]

                    if emotion_cols:
                        emotion_data = {col: chapter_emotions[col].iloc[0]
                                      for col in emotion_cols if col in chapter_emotions.columns}

                        fig = create_star_plot(
                            emotion_data,
                            f"Chapter {selected_chapter} Emotion Profile",
                            theme=plot_theme,
                            scaling=scaling_method
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Emotion data not found for this chapter.")
                else:
                    st.warning("Emotion scores not available for this chapter.")
                
                st.markdown("---")
                
                # Cluster assignment
                try:
                    cluster_assignments = load_cluster_assignments()
                    if not cluster_assignments.empty and 'chapter' in cluster_assignments.columns:
                        cluster_data = cluster_assignments[
                            cluster_assignments['chapter'] == selected_chapter
                        ]
                        if not cluster_data.empty and 'cluster' in cluster_data.columns:
                            cluster_id = cluster_data['cluster'].iloc[0]
                            st.info(f"📊 **Belongs to Cluster {cluster_id}**")
                except:
                    pass
                
                st.markdown("---")
                
                # Emotion words found
                try:
                    emotion_words = load_emotion_words_found()
                    if not emotion_words.empty:
                        display_emotion_words(emotion_words, selected_chapter)
                        st.markdown("---")
                except FileNotFoundError:
                    pass
                except Exception as e:
                    st.debug(f"Could not load emotion words: {e}")
                
                # Similar stories
                try:
                    similarity_df = load_chapter_similarity()
                    if not similarity_df.empty:
                        display_similar_stories(
                            similarity_df,
                            selected_chapter,
                            stories,
                            top_n=5
                        )
                except FileNotFoundError:
                    pass
                except Exception as e:
                    st.debug(f"Could not load similar stories: {e}")
            else:
                st.warning(f"No story data found for chapter {selected_chapter}.")
        
except FileNotFoundError:
    st.info("📝 Story data not found. Please generate the data files first.")
except Exception as e:
    st.error(f"Error loading story data: {e}")

