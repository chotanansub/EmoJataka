"""Generate base jataka_stories.csv file."""

import pandas as pd
import random
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, STORY_TITLES, THAI_SAMPLE_WORDS, OUTPUT_DIR

def generate_story_text(chapter_num: int) -> str:
    """Generate a sample Thai story text."""
    # Create a simple story text with Thai words
    words_per_sentence = random.randint(8, 15)
    num_sentences = random.randint(5, 10)
    
    sentences = []
    for _ in range(num_sentences):
        sentence_words = random.choices(THAI_SAMPLE_WORDS, k=words_per_sentence)
        sentence = " ".join(sentence_words)
        sentences.append(sentence)
    
    return " ".join(sentences) + "."

def generate_jataka_stories():
    """Generate jataka_stories.csv with chapter, title, and text."""
    print(f"Generating jataka_stories.csv with {NUM_STORIES} chapters...")
    
    data = []
    for i in range(1, NUM_STORIES + 1):
        title = STORY_TITLES[i % len(STORY_TITLES)] if i <= len(STORY_TITLES) else f"เรื่องที่ {i}"
        text = generate_story_text(i)
        
        data.append({
            'chapter': i,
            'title': title,
            'text': text
        })
    
    df = pd.DataFrame(data)
    
    # Create output directory if it doesn't exist
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    filepath = output_path / "jataka_stories.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_jataka_stories()

