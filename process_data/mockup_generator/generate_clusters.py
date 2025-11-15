"""Generate cluster-related CSV files."""

import pandas as pd
import random
import numpy as np
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import NUM_STORIES, NUM_CLUSTERS, EMOTIONS, OUTPUT_DIR

def generate_cluster_assignments():
    """Generate cluster_assignments.csv with cluster assignments per chapter."""
    print(f"Generating cluster_assignments.csv for {NUM_STORIES} chapters...")
    
    data = []
    # Assign chapters to clusters (roughly balanced)
    chapters_per_cluster = NUM_STORIES // NUM_CLUSTERS
    
    for chapter in range(1, NUM_STORIES + 1):
        # Assign to cluster (0-indexed, but we'll use 1-indexed for display)
        cluster = min((chapter - 1) // (chapters_per_cluster + 1), NUM_CLUSTERS - 1) + 1
        data.append({
            'chapter': chapter,
            'cluster': cluster
        })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "cluster_assignments.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_cluster_emotions():
    """Generate cluster_emotions.csv with average emotions per cluster."""
    print("Generating cluster_emotions.csv...")
    
    # Load cluster assignments and emotion scores
    try:
        cluster_assignments = pd.read_csv(Path(OUTPUT_DIR) / "cluster_assignments.csv")
        emotion_scores = pd.read_csv(Path(OUTPUT_DIR) / "emotion_scores.csv")
        
        # Merge to get emotions per cluster
        merged = cluster_assignments.merge(emotion_scores, on='chapter')
        
        # Calculate average emotions per cluster
        cluster_emotions = merged.groupby('cluster')[EMOTIONS].mean().reset_index()
        cluster_emotions = cluster_emotions.round(4)
        
        df = cluster_emotions
    except FileNotFoundError:
        # Generate random cluster emotions if files don't exist
        data = []
        for cluster in range(1, NUM_CLUSTERS + 1):
            row = {'cluster': cluster}
            for emotion in EMOTIONS:
                row[emotion] = round(random.uniform(0.0, 1.0), 4)
            data.append(row)
        df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "cluster_emotions.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

def generate_cluster_visualization():
    """Generate cluster_visualization.csv with 2D coordinates for visualization."""
    print("Generating cluster_visualization.csv...")
    
    # Load cluster assignments
    try:
        cluster_assignments = pd.read_csv(Path(OUTPUT_DIR) / "cluster_assignments.csv")
    except FileNotFoundError:
        # Generate cluster assignments if not available
        cluster_assignments = generate_cluster_assignments()
    
    data = []
    for _, row in cluster_assignments.iterrows():
        chapter = row['chapter']
        cluster = row['cluster']
        
        # Generate 2D coordinates (simulate dimensionality reduction)
        # Each cluster has a center, with some variance
        cluster_centers = {
            1: (0.3, 0.3),
            2: (0.7, 0.3),
            3: (0.5, 0.7)
        }
        
        center_x, center_y = cluster_centers.get(cluster, (0.5, 0.5))
        
        # Add some noise around the center
        x = center_x + random.uniform(-0.2, 0.2)
        y = center_y + random.uniform(-0.2, 0.2)
        
        data.append({
            'chapter': chapter,
            'x': round(x, 4),
            'y': round(y, 4),
            'cluster': cluster
        })
    
    df = pd.DataFrame(data)
    
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / "cluster_visualization.csv"
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✓ Saved {filepath}")
    
    return df

if __name__ == "__main__":
    generate_cluster_assignments()
    generate_cluster_emotions()
    generate_cluster_visualization()

