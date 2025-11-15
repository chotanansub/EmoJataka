"""Generate POS (Part-of-Speech) related CSV files."""

import pandas as pd
import random
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, NUM_CLUSTERS, POS_TAGS, OUTPUT_DIR

def generate_pos_distribution():
    """Generate pos_distribution.csv with overall POS tag distribution."""
    print("Generating pos_distribution.csv...")
    
    data = []
    # Generate frequency for each POS tag
    for pos_tag in POS_TAGS:
        data.append({
            'pos_tag': pos_tag,
            'count': random.randint(100, 1000),
            'percentage': round(random.uniform(5.0, 25.0), 2)
        })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "pos_distribution.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_pos_by_chapter():
    """Generate pos_by_chapter.csv with POS distribution per chapter."""
    print(f"Generating pos_by_chapter.csv for {NUM_STORIES} chapters...")
    
    data = []
    for chapter in range(1, NUM_STORIES + 1):
        for pos_tag in POS_TAGS:
            data.append({
                'chapter': chapter,
                'pos_tag': pos_tag,
                'count': random.randint(10, 100),
                'percentage': round(random.uniform(5.0, 25.0), 2)
            })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "pos_by_chapter.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_pos_by_cluster():
    """Generate pos_by_cluster.csv with POS distribution per cluster."""
    print("Generating pos_by_cluster.csv...")
    
    # Load cluster assignments if available
    try:
        cluster_assignments = pd.read_csv(Path(OUTPUT_DIR) / "cluster_assignments.csv")
        clusters = sorted(cluster_assignments['cluster'].unique())
    except FileNotFoundError:
        clusters = list(range(1, NUM_CLUSTERS + 1))
    
    data = []
    for cluster in clusters:
        for pos_tag in POS_TAGS:
            data.append({
                'cluster': cluster,
                'pos_tag': pos_tag,
                'count': random.randint(50, 500),
                'percentage': round(random.uniform(5.0, 25.0), 2)
            })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "pos_by_cluster.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_pos_distribution()
    generate_pos_by_chapter()
    generate_pos_by_cluster()

