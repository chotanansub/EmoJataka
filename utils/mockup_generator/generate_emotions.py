"""Generate emotion-related CSV files."""

import pandas as pd
import random
import numpy as np
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, EMOTIONS, OUTPUT_DIR

def generate_emotion_scores():
    """Generate emotion_scores.csv with emotion scores per chapter."""
    print(f"Generating emotion_scores.csv for {NUM_STORIES} chapters...")
    
    data = []
    for chapter in range(1, NUM_STORIES + 1):
        row = {'chapter': chapter}
        # Generate random emotion scores (0-1 range)
        for emotion in EMOTIONS:
            row[emotion] = round(random.uniform(0.0, 1.0), 4)
        data.append(row)
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "emotion_scores.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_overall_emotions():
    """Generate overall_emotions.csv with average emotion scores."""
    print("Generating overall_emotions.csv...")
    
    # Load emotion scores to calculate averages
    try:
        emotion_scores = pd.read_csv(Path(OUTPUT_DIR) / "emotion_scores.csv")
        data = {}
        for emotion in EMOTIONS:
            if emotion in emotion_scores.columns:
                data[emotion] = round(emotion_scores[emotion].mean(), 4)
            else:
                data[emotion] = round(random.uniform(0.0, 1.0), 4)
    except FileNotFoundError:
        # Generate random averages if emotion_scores doesn't exist
        data = {emotion: round(random.uniform(0.0, 1.0), 4) for emotion in EMOTIONS}
    
    df = pd.DataFrame([data])
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "overall_emotions.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_emotion_words_found():
    """Generate emotion_words_found.csv with emotion words found in text."""
    print("Generating emotion_words_found.csv...")
    
    # Sample Thai emotion words (simplified)
    emotion_words_map = {
        "trust": ["เชื่อ", "ไว้วางใจ", "ศรัทธา", "เชื่อถือ"],
        "joy": ["สุข", "ยินดี", "ดีใจ", "เบิกบาน"],
        "anger": ["โกรธ", "โมโห", "ขุ่นเคือง", "โกรธา"],
        "anticipation": ["คาดหวัง", "รอคอย", "คาดการณ์", "หวัง"],
        "fear": ["กลัว", "หวาดกลัว", "วิตก", "กังวล"],
        "disgust": ["รังเกียจ", "ขยะแขยง", "เกลียด", "ไม่ชอบ"],
        "surprise": ["ประหลาดใจ", "แปลกใจ", "ตกใจ", "น่าประหลาด"],
        "sadness": ["เศร้า", "เสียใจ", "ทุกข์", "โศก"]
    }
    
    data = []
    for chapter in range(1, NUM_STORIES + 1):
        # Randomly assign some emotion words to each chapter
        for emotion in EMOTIONS:
            num_words = random.randint(0, 3)
            words = random.sample(emotion_words_map.get(emotion, ["คำ"]), min(num_words, len(emotion_words_map.get(emotion, ["คำ"]))))
            
            for word in words:
                data.append({
                    'chapter': chapter,
                    'emotion': emotion,
                    'word': word,
                    'count': random.randint(1, 5)
                })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "emotion_words_found.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_emotion_scores()
    generate_overall_emotions()
    generate_emotion_words_found()

