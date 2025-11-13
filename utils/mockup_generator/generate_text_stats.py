"""Generate text statistics CSV files."""

import pandas as pd
import random
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, OUTPUT_DIR

def generate_text_statistics():
    """Generate text_statistics.csv with text statistics per chapter."""
    print(f"Generating text_statistics.csv for {NUM_STORIES} chapters...")
    
    data = []
    for chapter in range(1, NUM_STORIES + 1):
        total_words = random.randint(200, 800)
        total_sentences = random.randint(15, 40)
        avg_sentence_length = round(total_words / total_sentences, 2) if total_sentences > 0 else 0
        avg_word_length = round(random.uniform(3.0, 6.0), 2)
        
        data.append({
            'chapter': chapter,
            'total_words': total_words,
            'total_sentences': total_sentences,
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'unique_words': random.randint(50, 200)
        })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "text_statistics.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_chapter_similarity():
    """Generate chapter_similarity.csv with similarity scores between chapters."""
    print("Generating chapter_similarity.csv...")
    
    data = []
    # Generate similarity matrix (symmetric)
    for chapter1 in range(1, NUM_STORIES + 1):
        for chapter2 in range(chapter1 + 1, NUM_STORIES + 1):
            # Higher similarity for chapters in same range (simulate clustering)
            if abs(chapter1 - chapter2) <= 2:
                similarity = random.uniform(0.6, 0.9)
            else:
                similarity = random.uniform(0.1, 0.5)
            
            data.append({
                'chapter': chapter1,
                'similar_chapter': chapter2,
                'similarity': round(similarity, 4)
            })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "chapter_similarity.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_text_statistics()
    generate_chapter_similarity()

