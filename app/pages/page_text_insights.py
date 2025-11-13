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
    load_pos_distribution, load_pos_by_chapter, load_pos_by_cluster,
    load_ner_entities, load_ner_by_chapter, load_ner_counts,
    load_cluster_assignments
)
from visualization.wordcloud_gen import wordcloud_from_dataframe, wordcloud_from_dict
from visualization.charts import create_pos_distribution_chart, create_ner_distribution_chart
import pandas as pd

st.set_page_config(
    page_title="Text Insights - Jataka Emotion Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Text Insights")
st.markdown("---")

# Create tabs
tab1, tab2, tab3 = st.tabs(["☁️ Word Clouds", "📝 Language Patterns", "🏷️ Named Entities"])

# Tab 1: Word Clouds
with tab1:
    st.header("☁️ Word Clouds")
    
    try:
        word_freq = load_word_frequencies()
        
        if not word_freq.empty:
            # Overall word cloud
            st.subheader("Overall Word Cloud")
            
            # Determine column names
            word_col = 'word' if 'word' in word_freq.columns else word_freq.columns[0]
            freq_col = 'frequency' if 'frequency' in word_freq.columns else word_freq.columns[1]
            
            if word_col in word_freq.columns and freq_col in word_freq.columns:
                # Limit to top words
                top_words = word_freq.nlargest(100, freq_col)
                word_dict = dict(zip(top_words[word_col], top_words[freq_col]))
                
                # Generate word cloud
                img_base64 = wordcloud_from_dict(word_dict)
                st.image(f"data:image/png;base64,{img_base64}", use_container_width=True)
            else:
                st.warning("Word frequency data format not recognized.")
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
                
                cluster_words = word_freq_cluster[
                    word_freq_cluster['cluster'] == selected_cluster
                ]
                
                if not cluster_words.empty:
                    word_col = 'word' if 'word' in cluster_words.columns else cluster_words.columns[0]
                    freq_col = 'frequency' if 'frequency' in cluster_words.columns else cluster_words.columns[1]
                    
                    if word_col in cluster_words.columns and freq_col in cluster_words.columns:
                        top_words = cluster_words.nlargest(100, freq_col)
                        word_dict = dict(zip(top_words[word_col], top_words[freq_col]))
                        
                        img_base64 = wordcloud_from_dict(word_dict)
                        st.image(f"data:image/png;base64,{img_base64}", use_container_width=True)
                    else:
                        st.warning("Word frequency data format not recognized.")
                else:
                    st.info(f"No word frequency data for cluster {selected_cluster}.")
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
                    
                    emotion_words = word_freq_emotion[
                        word_freq_emotion['emotion'] == selected_emotion
                    ]
                    
                    if not emotion_words.empty:
                        word_col = 'word' if 'word' in emotion_words.columns else emotion_words.columns[0]
                        freq_col = 'frequency' if 'frequency' in emotion_words.columns else emotion_words.columns[1]
                        
                        if word_col in emotion_words.columns and freq_col in emotion_words.columns:
                            top_words = emotion_words.nlargest(100, freq_col)
                            word_dict = dict(zip(top_words[word_col], top_words[freq_col]))
                            
                            img_base64 = wordcloud_from_dict(word_dict)
                            st.image(f"data:image/png;base64,{img_base64}", use_container_width=True)
                        else:
                            st.warning("Word frequency data format not recognized.")
                    else:
                        st.info(f"No word frequency data for emotion {selected_emotion}.")
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
    
    # Sentence length distribution
    st.subheader("Sentence Length Distribution")
    
    try:
        from utils.data_loader import load_text_statistics
        text_stats = load_text_statistics()
        
        if not text_stats.empty:
            if 'avg_sentence_length' in text_stats.columns:
                import plotly.express as px
                
                fig = px.histogram(
                    text_stats,
                    x='avg_sentence_length',
                    nbins=30,
                    title="Distribution of Average Sentence Length",
                    labels={'avg_sentence_length': 'Average Sentence Length (words)', 'count': 'Number of Chapters'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.metric(
                    "Average Sentence Length",
                    f"{text_stats['avg_sentence_length'].mean():.1f} words"
                )
            else:
                st.info("Sentence length data not available in text statistics.")
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

