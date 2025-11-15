"""Story display component."""

import streamlit as st
import pandas as pd
from typing import Optional, Dict

def display_story_info(
    story_data: pd.Series,
    chapter_col: str = "chapter",
    title_col: Optional[str] = None,
    text_col: Optional[str] = None
):
    """
    Display story information.
    
    Args:
        story_data: Series or dict with story data
        chapter_col: Column name for chapter number
        title_col: Column name for title
        text_col: Column name for text content
    """
    if isinstance(story_data, pd.Series):
        story_dict = story_data.to_dict()
    else:
        story_dict = story_data
    
    # Display chapter info
    if chapter_col in story_dict:
        st.subheader(f"Chapter {story_dict[chapter_col]}")
    
    if title_col and title_col in story_dict:
        st.markdown(f"**Title:** {story_dict[title_col]}")
    
    # Display full text
    if text_col and text_col in story_dict:
        with st.expander("📖 Story Text", expanded=False):
            text = str(story_dict[text_col])
            st.text(text)
            st.caption(f"Total: {len(text)} characters")

def display_emotion_words(
    emotion_words_df: pd.DataFrame,
    chapter_id: Optional[int] = None,
    max_words: int = 20
):
    """
    Display emotion words found in a chapter.
    
    Args:
        emotion_words_df: DataFrame with emotion words
        chapter_id: Chapter ID to filter
        max_words: Maximum number of words to display
    """
    if emotion_words_df.empty:
        st.info("No emotion words found.")
        return
    
    # Filter by chapter if provided
    if chapter_id is not None and 'chapter' in emotion_words_df.columns:
        filtered = emotion_words_df[emotion_words_df['chapter'] == chapter_id]
    else:
        filtered = emotion_words_df
    
    if filtered.empty:
        st.info("No emotion words found for this chapter.")
        return
    
    # Display top words
    st.subheader("🔍 Emotion Words Found")
    
    # Group by emotion if possible
    if 'emotion' in filtered.columns:
        for emotion in filtered['emotion'].unique():
            emotion_words = filtered[filtered['emotion'] == emotion]
            if 'word' in emotion_words.columns:
                words = emotion_words['word'].head(max_words).tolist()
                st.markdown(f"**{emotion.title()}:** {', '.join(words)}")
    elif 'word' in filtered.columns:
        words = filtered['word'].head(max_words).tolist()
        st.markdown(f"**Words:** {', '.join(words)}")

def display_similar_stories(
    similarity_df: pd.DataFrame,
    chapter_id: int,
    stories_df: pd.DataFrame,
    top_n: int = 5
):
    """
    Display similar stories based on emotion similarity.
    
    Args:
        similarity_df: DataFrame with similarity scores
        chapter_id: Current chapter ID
        stories_df: DataFrame with story information
        top_n: Number of similar stories to show
    """
    if similarity_df.empty:
        return
    
    st.subheader("📚 Similar Stories")
    
    # Find similar chapters
    if 'chapter' in similarity_df.columns and 'similarity' in similarity_df.columns:
        similar = similarity_df[similarity_df['chapter'] == chapter_id].nlargest(top_n, 'similarity')
        
        if not similar.empty:
            for idx, row in similar.iterrows():
                similar_chapter = row.get('similar_chapter', row.get('chapter_2', 'N/A'))
                similarity_score = row.get('similarity', 0)
                
                # Get story info
                story_info = stories_df[stories_df.get('chapter', stories_df.index) == similar_chapter]
                if not story_info.empty:
                    title = story_info.iloc[0].get('title', f"Chapter {similar_chapter}")
                    st.markdown(f"- **Chapter {similar_chapter}:** {title} (similarity: {similarity_score:.3f})")
        else:
            st.info("No similar stories found.")
    else:
        st.info("Similarity data not available.")

