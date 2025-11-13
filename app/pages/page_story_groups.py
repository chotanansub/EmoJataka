"""Story Groups (Clusters) page for the Jataka Emotion Analysis app."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path - handle both running from root and from app directory
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.data_loader import (
    load_cluster_assignments, load_cluster_emotions, 
    load_cluster_visualization, load_stories
)
from visualization.charts import create_cluster_pie_chart, create_emotion_bar_chart
from visualization.scatter_plot import create_cluster_scatter_plot

st.set_page_config(
    page_title="Story Groups - Jataka Emotion Analysis",
    page_icon="🎭",
    layout="wide"
)

st.title("🎭 Story Groups (Clusters)")
st.markdown("---")

# Explanation
st.header("📖 What are Story Groups?")
st.markdown("""
Story groups are clusters of similar Jataka tales created using **K-means clustering** on TF-IDF features.
Stories within the same cluster share similar themes, vocabulary, or narrative patterns.

**How it works:**
1. Text from each chapter is converted to TF-IDF vectors
2. K-means clustering groups similar stories together
3. Each cluster represents a distinct narrative pattern or theme
4. Emotion profiles can be compared across clusters to identify patterns
""")

st.markdown("---")

try:
    cluster_assignments = load_cluster_assignments()
    cluster_emotions = load_cluster_emotions()
    
    if not cluster_assignments.empty and 'cluster' in cluster_assignments.columns:
        # Cluster distribution
        st.header("📊 Cluster Distribution")
        
        cluster_counts = cluster_assignments['cluster'].value_counts().sort_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = create_cluster_pie_chart(cluster_counts, "Cluster Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Cluster Statistics")
            for cluster_id in sorted(cluster_counts.index):
                count = cluster_counts[cluster_id]
                percentage = (count / len(cluster_assignments)) * 100
                st.metric(
                    label=f"Cluster {cluster_id}",
                    value=f"{count} chapters",
                    delta=f"{percentage:.1f}%"
                )
        
        st.markdown("---")
        
        # Interactive scatter plot
        st.header("🗺️ Interactive Cluster Visualization")
        
        try:
            cluster_viz = load_cluster_visualization()
            
            if not cluster_viz.empty:
                # Determine column names
                x_col = 'x' if 'x' in cluster_viz.columns else cluster_viz.columns[0]
                y_col = 'y' if 'y' in cluster_viz.columns else cluster_viz.columns[1]
                cluster_col = 'cluster' if 'cluster' in cluster_viz.columns else None
                chapter_col = 'chapter' if 'chapter' in cluster_viz.columns else None
                
                fig_scatter = create_cluster_scatter_plot(
                    cluster_viz,
                    x_col=x_col,
                    y_col=y_col,
                    cluster_col=cluster_col,
                    chapter_col=chapter_col,
                    title="Story Clusters (2D Projection)"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
                st.caption("Hover over points to see chapter information. Points are colored by cluster.")
            else:
                st.info("Cluster visualization data not available. This requires 2D projection coordinates.")
        except FileNotFoundError:
            st.info("📝 Cluster visualization data not found. This requires dimensionality reduction (e.g., PCA, t-SNE).")
        except Exception as e:
            st.warning(f"Could not load cluster visualization: {e}")
        
        st.markdown("---")
        
        # Cluster comparison table
        st.header("📋 Cluster Comparison")
        
        if not cluster_emotions.empty and 'cluster' in cluster_emotions.columns:
            # Get emotion columns
            emotion_cols = [col for col in cluster_emotions.columns 
                          if col.lower() in ['trust', 'joy', 'anger', 'anticipation', 
                                            'fear', 'disgust', 'surprise', 'sadness']]
            
            if emotion_cols:
                # Create comparison table
                comparison_data = []
                for cluster_id in sorted(cluster_emotions['cluster'].unique()):
                    cluster_data = cluster_emotions[cluster_emotions['cluster'] == cluster_id]
                    if not cluster_data.empty:
                        row = {'Cluster': f"Cluster {cluster_id}"}
                        for emotion in emotion_cols:
                            if emotion in cluster_data.columns:
                                row[emotion.title()] = cluster_data[emotion].iloc[0]
                        comparison_data.append(row)
                
                if comparison_data:
                    import pandas as pd
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, use_container_width=True)
                    
                    # Visual comparison
                    st.subheader("📊 Visual Comparison")
                    selected_emotion = st.selectbox(
                        "Select Emotion to Compare",
                        [e.title() for e in emotion_cols]
                    )
                    
                    if selected_emotion:
                        emotion_lower = selected_emotion.lower()
                        if emotion_lower in [e.lower() for e in emotion_cols]:
                            # Get emotion values by cluster
                            emotion_by_cluster = {}
                            for cluster_id in sorted(cluster_emotions['cluster'].unique()):
                                cluster_data = cluster_emotions[cluster_emotions['cluster'] == cluster_id]
                                if not cluster_data.empty and emotion_lower in cluster_data.columns:
                                    emotion_by_cluster[f"Cluster {cluster_id}"] = cluster_data[emotion_lower].iloc[0]
                            
                            if emotion_by_cluster:
                                fig = create_emotion_bar_chart(
                                    emotion_by_cluster,
                                    f"{selected_emotion} by Cluster"
                                )
                                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Emotion columns not found in cluster emotions data.")
        else:
            st.warning("Cluster emotions data not available.")
        
        st.markdown("---")
        
        # Select cluster to explore
        st.header("🔍 Explore a Cluster")
        
        available_clusters = sorted(cluster_assignments['cluster'].unique())
        selected_cluster = st.selectbox(
            "Select a cluster to explore in detail",
            available_clusters,
            format_func=lambda x: f"Cluster {x}"
        )
        
        if selected_cluster is not None:
            cluster_chapters = cluster_assignments[
                cluster_assignments['cluster'] == selected_cluster
            ]
            
            st.info(f"""
            **Cluster {selected_cluster}** contains **{len(cluster_chapters)} chapters**.
            
            Navigate to the **🌟 Emotion Analysis** page and select the "By Story Group" tab 
            to see detailed emotion profiles for this cluster.
            """)
            
            # Show some chapters
            if 'chapter' in cluster_chapters.columns:
                chapters = cluster_chapters['chapter'].tolist()[:10]
                st.markdown("**Sample chapters in this cluster:**")
                st.markdown(", ".join([f"Chapter {ch}" for ch in chapters]))
                if len(cluster_chapters) > 10:
                    st.caption(f"... and {len(cluster_chapters) - 10} more chapters")
    
    else:
        st.warning("Cluster assignments data not available or missing 'cluster' column.")
        
except FileNotFoundError:
    st.info("📝 Cluster data not found. Please generate the cluster assignments and cluster emotions files first.")
except Exception as e:
    st.error(f"Error loading cluster data: {e}")

