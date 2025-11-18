"""Emotion Analysis page for the Jataka Emotion Analysis app."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path - handle both running from root and from app directory
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.data_loader import (
    load_cluster_emotions, load_emotion_scores,
    load_cluster_assignments, load_stories
)
from utils.emotion_scaling import get_scaling_description
from visualization.star_plot import create_star_plot, create_star_plot_from_df
from visualization.charts import create_emotion_bar_chart, create_emotion_bar_chart_from_df

st.set_page_config(
    page_title="Emotion Analysis - Jataka Emotion Analysis",
    page_icon="🌟",
    layout="wide"
)

st.title("🌟 Emotion Analysis")

# Global controls for all plots on this page
col_theme, col_scaling = st.columns(2)

with col_theme:
    plot_theme = st.selectbox(
        "🎨 Plot Theme",
        options=["light", "dark"],
        format_func=lambda x: "☀️ Light" if x == "light" else "🌙 Dark",
        key="emotion_analysis_global_theme"
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
        key="emotion_analysis_scaling"
    )

# Show scaling method description
with st.expander("ℹ️ About Score Display Methods"):
    st.markdown(get_scaling_description(scaling_method))

st.markdown("---")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 All Stories Combined", "🎭 By Story Group", "📖 Individual Story"])

# Tab 1: All Stories Combined
with tab1:
    st.header("All Stories Combined")

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

                # Charts
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Star Plot")
                    fig_star = create_star_plot(emotion_data, "Overall Emotion Profile (Mean Across All Chapters)",
                                               theme=plot_theme, scaling=scaling_method)
                    st.plotly_chart(fig_star, use_container_width=True, key="tab1_star_plot")

                with col2:
                    st.subheader("Bar Chart")
                    fig_bar = create_emotion_bar_chart(emotion_data, "Emotion Distribution (Mean Across All Chapters)",
                                                       theme=plot_theme, scaling=scaling_method)
                    st.plotly_chart(fig_bar, use_container_width=True, key="tab1_bar_chart")
                
                # Key insights
                max_emotion = max(emotion_data.items(), key=lambda x: x[1])
                min_emotion = min(emotion_data.items(), key=lambda x: x[1])
                avg_score = sum(emotion_data.values()) / len(emotion_data)
                
                st.subheader("💡 Key Insights")
                st.info(f"""
                - **Highest emotion**: {max_emotion[0].title()} ({max_emotion[1]:.3f})
                - **Lowest emotion**: {min_emotion[0].title()} ({min_emotion[1]:.3f})
                - **Average emotion score**: {avg_score:.3f}
                - **Emotion range**: {max_emotion[1] - min_emotion[1]:.3f}
                """)
            else:
                st.warning("Emotion columns not found in the data.")
        else:
            st.warning("Overall emotions data is empty.")
            
    except FileNotFoundError:
        st.info("📝 Overall emotion data not found. Please generate the data files first.")
    except Exception as e:
        st.error(f"Error loading overall emotions: {e}")

# Tab 2: By Story Group
with tab2:
    st.header("By Story Group")
    
    try:
        cluster_emotions = load_cluster_emotions()
        cluster_assignments = load_cluster_assignments()
        stories = load_stories()
        
        if not cluster_emotions.empty and 'cluster' in cluster_emotions.columns:
            # Get available clusters
            available_clusters = sorted(cluster_emotions['cluster'].unique())
            
            if available_clusters:
                selected_cluster = st.selectbox(
                    "Select Cluster",
                    available_clusters,
                    format_func=lambda x: f"Cluster {x}"
                )
                
                # Get cluster emotion data
                cluster_data = cluster_emotions[cluster_emotions['cluster'] == selected_cluster]
                
                if not cluster_data.empty:
                    # Get emotion columns
                    emotion_cols = [col for col in cluster_data.columns 
                                  if col.lower() in ['trust', 'joy', 'anger', 'anticipation', 
                                                    'fear', 'disgust', 'surprise', 'sadness']]
                    
                    if emotion_cols:
                        cluster_emotion_data = {col: cluster_data[col].iloc[0]
                                              for col in emotion_cols if col in cluster_data.columns}

                        # Get overall emotions for comparison (mean across all chapters)
                        try:
                            all_chapters = load_emotion_scores()
                            overall_emotion_data = {col: all_chapters[col].mean()
                                                  for col in emotion_cols if col in all_chapters.columns}
                        except:
                            overall_emotion_data = None

                        # Star plots side by side
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader(f"Cluster {selected_cluster} Emotion Profile")
                            fig_cluster = create_star_plot(
                                cluster_emotion_data,
                                f"Cluster {selected_cluster} Emotions",
                                theme=plot_theme,
                                scaling=scaling_method
                            )
                            st.plotly_chart(fig_cluster, use_container_width=True, key=f"tab2_cluster_{selected_cluster}_star")

                        with col2:
                            if overall_emotion_data:
                                st.subheader("Overall Average (Comparison)")
                                fig_overall = create_star_plot(
                                    overall_emotion_data,
                                    "Overall Average (Mean Across All Chapters)",
                                    theme=plot_theme,
                                    scaling=scaling_method
                                )
                                st.plotly_chart(fig_overall, use_container_width=True, key=f"tab2_overall_star")
                        
                        # Stories in this cluster
                        if not cluster_assignments.empty:
                            cluster_chapters = cluster_assignments[
                                cluster_assignments['cluster'] == selected_cluster
                            ]
                            
                            st.subheader(f"📚 Stories in Cluster {selected_cluster}")
                            st.info(f"**Total chapters in this cluster:** {len(cluster_chapters)}")
                            
                            # Display chapter list
                            if 'chapter' in cluster_chapters.columns:
                                chapters = cluster_chapters['chapter'].tolist()
                                if 'chapter' in stories.columns:
                                    chapter_info = []
                                    for ch in chapters[:20]:  # Show first 20
                                        story_info = stories[stories['chapter'] == ch]
                                        if not story_info.empty:
                                            title = story_info.iloc[0].get('title', f"Chapter {ch}")
                                            chapter_info.append(f"- **Chapter {ch}:** {title}")
                                    
                                    if chapter_info:
                                        st.markdown("\n".join(chapter_info))
                                    if len(chapters) > 20:
                                        st.caption(f"... and {len(chapters) - 20} more chapters")
                                else:
                                    st.markdown("\n".join([f"- Chapter {ch}" for ch in chapters[:20]]))
                    else:
                        st.warning("Emotion columns not found in cluster data.")
                else:
                    st.warning(f"No data found for cluster {selected_cluster}.")
            else:
                st.warning("No clusters found in the data.")
        else:
            st.warning("Cluster emotions data not available.")
            
    except FileNotFoundError:
        st.info("📝 Cluster emotion data not found. Please generate the data files first.")
    except Exception as e:
        st.error(f"Error loading cluster emotions: {e}")

# Tab 3: Individual Story
with tab3:
    st.header("Individual Story")
    
    try:
        emotion_scores = load_emotion_scores()
        stories = load_stories()
        
        if not emotion_scores.empty and not stories.empty:
            # Get chapter options
            if 'chapter' in emotion_scores.columns:
                chapters = sorted(emotion_scores['chapter'].unique())
            elif 'chapter' in stories.columns:
                chapters = sorted(stories['chapter'].unique())
            else:
                chapters = list(range(1, len(emotion_scores) + 1))
            
            # Chapter selector
            selected_chapter = st.selectbox(
                "Select Chapter",
                chapters,
                format_func=lambda x: f"Chapter {x}"
            )
            
            # Get chapter emotion data
            chapter_data = emotion_scores[emotion_scores['chapter'] == selected_chapter]
            
            if not chapter_data.empty:
                # Get emotion columns
                emotion_cols = [col for col in chapter_data.columns 
                              if col.lower() in ['trust', 'joy', 'anger', 'anticipation', 
                                                'fear', 'disgust', 'surprise', 'sadness']]
                
                if emotion_cols:
                    chapter_emotion_data = {col: chapter_data[col].iloc[0]
                                          for col in emotion_cols if col in chapter_data.columns}

                    # Get overall emotions for comparison (mean across all chapters)
                    overall_emotion_data = {col: emotion_scores[col].mean()
                                          for col in emotion_cols if col in emotion_scores.columns}

                    # Star plots side by side
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader(f"Chapter {selected_chapter} Emotion Profile")
                        fig_chapter = create_star_plot(
                            chapter_emotion_data,
                            f"Chapter {selected_chapter} Emotions",
                            theme=plot_theme,
                            scaling=scaling_method
                        )
                        st.plotly_chart(fig_chapter, use_container_width=True, key=f"tab3_chapter_{selected_chapter}_star")

                    with col2:
                        st.subheader("Overall Average (Comparison)")
                        fig_overall = create_star_plot(
                            overall_emotion_data,
                            "Overall Average (Mean Across All Chapters)",
                            theme=plot_theme,
                            scaling=scaling_method
                        )
                        st.plotly_chart(fig_overall, use_container_width=True, key=f"tab3_overall_star")
                    
                    # Story text preview
                    story_info = stories[stories['chapter'] == selected_chapter]
                    if not story_info.empty:
                        st.subheader("📖 Story Preview")
                        with st.expander("View Story Text", expanded=False):
                            text_col = 'text' if 'text' in story_info.columns else story_info.columns[-1]
                            text = story_info[text_col].iloc[0]
                            preview_length = 1000
                            if len(str(text)) > preview_length:
                                st.text(str(text)[:preview_length] + "...")
                                st.caption(f"Showing first {preview_length} characters")
                            else:
                                st.text(str(text))
                else:
                    st.warning("Emotion columns not found in chapter data.")
            else:
                st.warning(f"No emotion data found for chapter {selected_chapter}.")
        else:
            st.warning("Emotion scores or stories data not available.")
            
    except FileNotFoundError:
        st.info("📝 Emotion scores data not found. Please generate the data files first.")
    except Exception as e:
        st.error(f"Error loading emotion scores: {e}")

