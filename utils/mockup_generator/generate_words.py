"""Generate word frequency related CSV files."""

import pandas as pd
import random
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, NUM_CLUSTERS, EMOTIONS, OUTPUT_DIR, THAI_SAMPLE_WORDS

def generate_word_frequencies():
    """Generate word_frequencies.csv with overall word frequencies."""
    print("Generating word_frequencies.csv...")
    
    data = []
    # Use sample words and add some variations
    all_words = THAI_SAMPLE_WORDS + [f"คำ{i}" for i in range(1, 50)]
    
    for word in all_words[:30]:  # Top 30 words
        data.append({
            'word': word,
            'frequency': random.randint(10, 500),
            'rank': len(data) + 1
        })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "word_frequencies.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_word_freq_by_cluster():
    """Generate word_freq_by_cluster.csv with word frequencies per cluster."""
    print("Generating word_freq_by_cluster.csv...")
    
    # Load cluster assignments if available
    try:
        cluster_assignments = pd.read_csv(Path(OUTPUT_DIR) / "cluster_assignments.csv")
        clusters = sorted(cluster_assignments['cluster'].unique())
    except FileNotFoundError:
        clusters = list(range(1, NUM_CLUSTERS + 1))
    
    data = []
    all_words = THAI_SAMPLE_WORDS + [f"คำ{i}" for i in range(1, 30)]
    
    for cluster in clusters:
        for word in all_words[:20]:  # Top 20 words per cluster
            data.append({
                'cluster': cluster,
                'word': word,
                'frequency': random.randint(5, 200),
                'rank': len([d for d in data if d.get('cluster') == cluster]) + 1
            })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "word_freq_by_cluster.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_word_freq_by_emotion():
    """Generate word_freq_by_emotion.csv with word frequencies per emotion."""
    print("Generating word_freq_by_emotion.csv...")
    
    # Sample emotion-related words
    emotion_words_map = {
        "trust": ["เชื่อ", "ไว้วางใจ", "ศรัทธา", "เชื่อถือ", "วางใจ"],
        "joy": ["สุข", "ยินดี", "ดีใจ", "เบิกบาน", "ร่าเริง"],
        "anger": ["โกรธ", "โมโห", "ขุ่นเคือง", "โกรธา", "เดือดดาล"],
        "anticipation": ["คาดหวัง", "รอคอย", "คาดการณ์", "หวัง", "รอ"],
        "fear": ["กลัว", "หวาดกลัว", "วิตก", "กังวล", "หวั่น"],
        "disgust": ["รังเกียจ", "ขยะแขยง", "เกลียด", "ไม่ชอบ", "รังเกียจ"],
        "surprise": ["ประหลาดใจ", "แปลกใจ", "ตกใจ", "น่าประหลาด", "อัศจรรย์"],
        "sadness": ["เศร้า", "เสียใจ", "ทุกข์", "โศก", "หดหู่"]
    }
    
    data = []
    for emotion in EMOTIONS:
        words = emotion_words_map.get(emotion, ["คำ"])
        # Add some generic words too
        all_words = words + [f"{emotion}_word{i}" for i in range(1, 10)]
        
        for word in all_words[:15]:  # Top 15 words per emotion
            data.append({
                'emotion': emotion,
                'word': word,
                'frequency': random.randint(5, 150),
                'rank': len([d for d in data if d.get('emotion') == emotion]) + 1
            })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "word_freq_by_emotion.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_word_frequencies()
    generate_word_freq_by_cluster()
    generate_word_freq_by_emotion()

