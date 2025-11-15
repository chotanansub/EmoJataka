"""Text Insights page for the Jataka Emotion Analysis app."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path - handle both running from root and from app directory
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.data_loader import (
    load_word_frequencies, load_word_freq_by_cluster, load_word_freq_by_emotion,
    load_word_freq_by_pos, load_word_freq_by_ner,
    load_pos_distribution, load_pos_by_chapter, load_pos_by_cluster,
    load_ner_entities, load_ner_by_chapter, load_ner_counts,
    load_cluster_assignments
)
from visualization.charts import create_pos_distribution_chart, create_ner_distribution_chart
import pandas as pd
import base64
from io import BytesIO
from PIL import Image as PILImage

try:
    from streamlit_image_zoom import image_zoom
    HAS_IMAGE_ZOOM = True
except ImportError:
    HAS_IMAGE_ZOOM = False

st.set_page_config(
    page_title="Text Insights - Jataka Emotion Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Text Insights")
st.markdown("---")

# Helper functions
def get_filtered_words(word_freq_df, filter_type, cluster=None, emotion=None):
    """
    Filter word frequencies based on POS tag or NER entity type.

    Args:
        word_freq_df: DataFrame with word frequencies (can include cluster/emotion column)
        filter_type: One of 'all', 'noun', 'verb', 'adjective', 'person', 'location'
        cluster: Optional cluster number to filter by
        emotion: Optional emotion to filter by

    Returns:
        Dictionary of {word: frequency}
    """
    # Handle cluster filtering for cluster-specific data
    if cluster is not None and 'cluster' in word_freq_df.columns:
        word_freq_df = word_freq_df[word_freq_df['cluster'] == cluster]

    # Handle emotion filtering for emotion-specific data
    if emotion is not None and 'emotion' in word_freq_df.columns:
        word_freq_df = word_freq_df[word_freq_df['emotion'] == emotion]

    if filter_type == "all":
        # Return all words
        word_col = 'word' if 'word' in word_freq_df.columns else word_freq_df.columns[0]
        freq_col = 'frequency' if 'frequency' in word_freq_df.columns else word_freq_df.columns[1]
        return dict(zip(word_freq_df[word_col], word_freq_df[freq_col]))

    # For filtered types, we need to intersect specific words with POS/NER filtered words
    if cluster is not None or emotion is not None:
        # Get the word list from the filtered data
        word_col = 'word' if 'word' in word_freq_df.columns else word_freq_df.columns[0]
        specific_words = set(word_freq_df[word_col])

    # POS-based filters
    if filter_type in ["noun", "verb", "adjective"]:
        try:
            word_freq_pos = load_word_freq_by_pos()

            # Map filter to POS tags
            pos_tag_map = {
                "noun": "NOUN",
                "verb": "VERB",
                "adjective": "ADJ"
            }
            pos_tag = pos_tag_map[filter_type]

            # Filter by POS tag
            filtered = word_freq_pos[word_freq_pos['pos_tag'] == pos_tag]

            # If cluster/emotion is specified, intersect with those words
            if cluster is not None or emotion is not None:
                filtered = filtered[filtered['word'].isin(specific_words)]

            return dict(zip(filtered['word'], filtered['frequency']))
        except Exception as e:
            st.warning(f"Could not load POS-filtered words: {e}")
            return {}

    # NER-based filters
    if filter_type in ["person", "location"]:
        try:
            word_freq_ner = load_word_freq_by_ner()

            # Map filter to entity types
            entity_type_map = {
                "person": "PERSON",
                "location": "LOCATION"
            }
            entity_type = entity_type_map[filter_type]

            # Filter by entity type
            filtered = word_freq_ner[word_freq_ner['entity_type'] == entity_type]

            # If cluster/emotion is specified, intersect with those words
            if cluster is not None or emotion is not None:
                filtered = filtered[filtered['word'].isin(specific_words)]

            return dict(zip(filtered['word'], filtered['frequency']))
        except Exception as e:
            st.warning(f"Could not load NER-filtered words: {e}")
            return {}

    return {}

def display_wordcloud_image(img_base64: str):
    """Display word cloud image with native Streamlit for sharp viewing."""
    # Display at small size by default (preview)
    st.image(f"data:image/png;base64,{img_base64}", width=600, caption="Preview - Expand below to see full resolution")

    # Provide expander with full-scale image
    with st.expander("🔍 View Full Scale (3200x2400 @ 200 DPI)"):
        st.image(f"data:image/png;base64,{img_base64}", use_container_width=True)
        st.caption("💡 Tip: Right-click and 'Open image in new tab' for pixel-perfect zoom in your browser")

# Create tabs
tab1, tab2, tab3 = st.tabs(["☁️ Word Clouds", "📝 Language Patterns", "🏷️ Named Entities"])

# Tab 1: Word Clouds
with tab1:
    st.header("☁️ Word Clouds")

    # Configuration row
    col_filter, col_theme = st.columns([2, 1])

    with col_filter:
        filter_option = st.selectbox(
            "🔍 Filter by",
            options=["all", "noun", "verb", "adjective", "person", "location"],
            format_func=lambda x: {
                "all": "All Words",
                "noun": "Nouns Only",
                "verb": "Verbs Only",
                "adjective": "Adjectives Only",
                "person": "Person Names",
                "location": "Location Names"
            }[x],
            key="wordcloud_filter"
        )

    with col_theme:
        theme_option = st.selectbox(
            "🎨 Theme",
            options=["dark", "light"],
            format_func=lambda x: "☀️ Light" if x == "light" else "🌙 Dark",
            key="wordcloud_theme"
        )

    try:
        word_freq = load_word_frequencies()

        if not word_freq.empty:
            # Overall word cloud
            st.subheader("Overall Word Cloud")

            # Get filtered words based on selection
            word_dict = get_filtered_words(word_freq, filter_option)

            if word_dict:
                # Limit to top 100 words
                sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:100]
                top_word_dict = dict(sorted_words)

                # Generate word cloud with theme
                from visualization.wordcloud_gen import generate_wordcloud
                filter_label = {
                    "all": "Overall",
                    "noun": "Nouns",
                    "verb": "Verbs",
                    "adjective": "Adjectives",
                    "person": "Person Names",
                    "location": "Locations"
                }[filter_option]
                img_base64 = generate_wordcloud(top_word_dict, theme=theme_option, title=f"{filter_label} Word Cloud")
                display_wordcloud_image(img_base64)
            else:
                st.warning(f"No {filter_option} words available.")
        else:
            st.warning("Word frequencies data not available.")
        
        st.markdown("---")
        
        # Word cloud by cluster
        st.subheader("Word Cloud by Cluster")

        try:
            word_freq_cluster = load_word_freq_by_cluster()
            cluster_assignments = load_cluster_assignments()

            if not word_freq_cluster.empty and not cluster_assignments.empty:
                available_clusters = sorted(cluster_assignments['cluster'].unique())
                selected_cluster = st.selectbox(
                    "Select Cluster",
                    available_clusters,
                    format_func=lambda x: f"Cluster {x}",
                    key="cluster_wordcloud"
                )

                # Get filtered words for this cluster
                word_dict = get_filtered_words(word_freq_cluster, filter_option, cluster=selected_cluster)

                if word_dict:
                    # Limit to top 100 words
                    sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:100]
                    top_word_dict = dict(sorted_words)

                    from visualization.wordcloud_gen import generate_wordcloud
                    filter_label = {
                        "all": "",
                        "noun": "Nouns - ",
                        "verb": "Verbs - ",
                        "adjective": "Adjectives - ",
                        "person": "Person Names - ",
                        "location": "Locations - "
                    }[filter_option]
                    img_base64 = generate_wordcloud(top_word_dict, theme=theme_option, title=f"{filter_label}Cluster {selected_cluster}")
                    display_wordcloud_image(img_base64)
                else:
                    st.info(f"No {filter_option} words for cluster {selected_cluster}.")
            else:
                st.info("Word frequency by cluster data not available.")
        except FileNotFoundError:
            st.info("📝 Word frequency by cluster data not found.")
        except Exception as e:
            st.warning(f"Could not load word frequency by cluster: {e}")
        
        st.markdown("---")
        
        # Word cloud by emotion
        st.subheader("Word Cloud by Emotion")

        try:
            word_freq_emotion = load_word_freq_by_emotion()

            if not word_freq_emotion.empty:
                emotions = ['trust', 'joy', 'anger', 'anticipation', 'fear', 'disgust', 'surprise', 'sadness']
                available_emotions = [e for e in emotions if e in word_freq_emotion.get('emotion', pd.Series()).values]

                if available_emotions:
                    selected_emotion = st.selectbox(
                        "Select Emotion",
                        available_emotions,
                        format_func=lambda x: x.title(),
                        key="emotion_wordcloud"
                    )

                    # Get filtered words for this emotion
                    word_dict = get_filtered_words(word_freq_emotion, filter_option, emotion=selected_emotion)

                    if word_dict:
                        # Limit to top 100 words
                        sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:100]
                        top_word_dict = dict(sorted_words)

                        from visualization.wordcloud_gen import generate_wordcloud
                        filter_label = {
                            "all": "",
                            "noun": "Nouns - ",
                            "verb": "Verbs - ",
                            "adjective": "Adjectives - ",
                            "person": "Person Names - ",
                            "location": "Locations - "
                        }[filter_option]
                        img_base64 = generate_wordcloud(top_word_dict, theme=theme_option, title=f"{filter_label}{selected_emotion.title()} Emotion")
                        display_wordcloud_image(img_base64)
                    else:
                        st.info(f"No {filter_option} words for emotion {selected_emotion}.")
                else:
                    st.info("No emotion data available in word frequencies.")
            else:
                st.info("Word frequency by emotion data not available.")
        except FileNotFoundError:
            st.info("📝 Word frequency by emotion data not found.")
        except Exception as e:
            st.warning(f"Could not load word frequency by emotion: {e}")
    except FileNotFoundError:
        st.info("📝 Word frequency data not found. Please generate the data files first.")
    except Exception as e:
        st.error(f"Error loading word frequencies: {e}")

# Tab 2: Language Patterns
with tab2:
    st.header("📝 Language Patterns")
    
    # POS distribution
    st.subheader("POS Tag Distribution")
    
    try:
        pos_dist = load_pos_distribution()
        
        if not pos_dist.empty:
            fig = create_pos_distribution_chart(pos_dist, "POS Tag Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show top POS tags
            if 'pos_tag' in pos_dist.columns and 'count' in pos_dist.columns:
                top_pos = pos_dist.nlargest(10, 'count')
                st.dataframe(top_pos, use_container_width=True)
            else:
                st.dataframe(pos_dist.head(20), use_container_width=True)
        else:
            st.warning("POS distribution data not available.")
    except FileNotFoundError:
        st.info("📝 POS distribution data not found.")
    except Exception as e:
        st.error(f"Error loading POS distribution: {e}")
    
    st.markdown("---")
    
    # Most common nouns/verbs
    st.subheader("Most Common Nouns and Verbs")
    
    try:
        pos_dist = load_pos_distribution()
        
        if not pos_dist.empty:
            # Try to identify nouns and verbs (common POS tags in Thai: N, V, etc.)
            if 'pos_tag' in pos_dist.columns and 'count' in pos_dist.columns:
                # Filter for nouns (common tags: N, NOUN, NN, etc.)
                nouns = pos_dist[
                    pos_dist['pos_tag'].str.contains('N|NOUN', case=False, na=False)
                ].nlargest(10, 'count')
                
                # Filter for verbs (common tags: V, VERB, VB, etc.)
                verbs = pos_dist[
                    pos_dist['pos_tag'].str.contains('V|VERB', case=False, na=False)
                ].nlargest(10, 'count')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top Nouns**")
                    if not nouns.empty:
                        st.dataframe(nouns, use_container_width=True)
                    else:
                        st.info("No noun data available.")
                
                with col2:
                    st.markdown("**Top Verbs**")
                    if not verbs.empty:
                        st.dataframe(verbs, use_container_width=True)
                    else:
                        st.info("No verb data available.")
            else:
                st.info("POS tag structure not recognized. Showing raw data:")
                st.dataframe(pos_dist.head(20), use_container_width=True)
        else:
            st.warning("POS distribution data not available.")
    except FileNotFoundError:
        st.info("📝 POS distribution data not found.")
    except Exception as e:
        st.warning(f"Could not load POS data: {e}")
    
    st.markdown("---")

    # Word count distribution
    st.subheader("Word Count Distribution")

    try:
        from utils.data_loader import load_text_statistics
        text_stats = load_text_statistics()

        if not text_stats.empty:
            if 'total_words' in text_stats.columns:
                import plotly.express as px

                fig = px.histogram(
                    text_stats,
                    x='total_words',
                    nbins=30,
                    title="Distribution of Word Count per Story",
                    labels={'total_words': 'Total Words', 'count': 'Number of Stories'}
                )
                st.plotly_chart(fig, use_container_width=True)

                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Words", f"{text_stats['total_words'].mean():.0f}")
                with col2:
                    st.metric("Min Words", f"{text_stats['total_words'].min():.0f}")
                with col3:
                    st.metric("Max Words", f"{text_stats['total_words'].max():.0f}")
            else:
                st.info("Word count data not available in text statistics.")
        else:
            st.warning("Text statistics data not available.")
    except FileNotFoundError:
        st.info("📝 Text statistics data not found.")
    except Exception as e:
        st.warning(f"Could not load text statistics: {e}")

# Tab 3: Named Entities
with tab3:
    st.header("🏷️ Named Entities")
    
    # People mentioned
    st.subheader("People Mentioned")
    
    try:
        ner_entities = load_ner_entities()
        ner_counts = load_ner_counts()
        
        if not ner_entities.empty:
            # Filter for person entities
            if 'entity_type' in ner_entities.columns:
                people = ner_entities[ner_entities['entity_type'].str.contains('PERSON|คน|บุคคล', case=False, na=False)]
                
                if not people.empty:
                    if 'entity' in people.columns and 'count' in people.columns:
                        top_people = people.nlargest(20, 'count')
                        st.dataframe(top_people, use_container_width=True)
                    elif 'entity' in people.columns:
                        entity_counts = people['entity'].value_counts().head(20)
                        st.dataframe(pd.DataFrame({
                            'Entity': entity_counts.index,
                            'Count': entity_counts.values
                        }), use_container_width=True)
                    else:
                        st.dataframe(people.head(20), use_container_width=True)
                else:
                    st.info("No person entities found.")
            else:
                st.info("Entity type information not available. Showing all entities:")
                st.dataframe(ner_entities.head(20), use_container_width=True)
        else:
            st.warning("NER entities data not available.")
    except FileNotFoundError:
        st.info("📝 NER entities data not found.")
    except Exception as e:
        st.warning(f"Could not load NER entities: {e}")
    
    st.markdown("---")
    
    # Places mentioned
    st.subheader("Places Mentioned")
    
    try:
        ner_entities = load_ner_entities()
        
        if not ner_entities.empty:
            if 'entity_type' in ner_entities.columns:
                places = ner_entities[ner_entities['entity_type'].str.contains('LOC|PLACE|สถานที่|สถานที่', case=False, na=False)]
                
                if not places.empty:
                    if 'entity' in places.columns and 'count' in places.columns:
                        top_places = places.nlargest(20, 'count')
                        st.dataframe(top_places, use_container_width=True)
                    elif 'entity' in places.columns:
                        entity_counts = places['entity'].value_counts().head(20)
                        st.dataframe(pd.DataFrame({
                            'Entity': entity_counts.index,
                            'Count': entity_counts.values
                        }), use_container_width=True)
                    else:
                        st.dataframe(places.head(20), use_container_width=True)
                else:
                    st.info("No place entities found.")
            else:
                st.info("Entity type information not available.")
        else:
            st.warning("NER entities data not available.")
    except FileNotFoundError:
        st.info("📝 NER entities data not found.")
    except Exception as e:
        st.warning(f"Could not load NER entities: {e}")
    
    st.markdown("---")
    
    # Entity distribution chart
    st.subheader("Entity Type Distribution")
    
    try:
        ner_counts = load_ner_counts()
        
        if not ner_counts.empty:
            fig = create_ner_distribution_chart(ner_counts, "NER Entity Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show table
            st.dataframe(ner_counts, use_container_width=True)
        else:
            st.warning("NER counts data not available.")
    except FileNotFoundError:
        st.info("📝 NER counts data not found.")
    except Exception as e:
        st.warning(f"Could not load NER counts: {e}")

