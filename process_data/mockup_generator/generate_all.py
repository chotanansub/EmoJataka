"""Generate all mockup data files."""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generate_base import generate_jataka_stories
from generate_emotions import (
    generate_emotion_scores,
    generate_overall_emotions,
    generate_emotion_words_found
)
from generate_clusters import (
    generate_cluster_assignments,
    generate_cluster_emotions,
    generate_cluster_visualization
)
from generate_text_stats import (
    generate_text_statistics,
    generate_chapter_similarity
)
from generate_pos import (
    generate_pos_distribution,
    generate_pos_by_chapter,
    generate_pos_by_cluster
)
from generate_ner import (
    generate_ner_entities,
    generate_ner_by_chapter,
    generate_ner_counts
)
from generate_words import (
    generate_word_frequencies,
    generate_word_freq_by_cluster,
    generate_word_freq_by_emotion
)

def generate_all():
    """Generate all mockup data files in the correct order."""
    print("=" * 60)
    print("Generating all mockup data files...")
    print("=" * 60)
    
    # Step 1: Generate base stories (needed by other generators)
    print("\n[Step 1/8] Generating base stories...")
    generate_jataka_stories()
    
    # Step 2: Generate emotion data
    print("\n[Step 2/8] Generating emotion data...")
    generate_emotion_scores()
    generate_overall_emotions()
    generate_emotion_words_found()
    
    # Step 3: Generate cluster data
    print("\n[Step 3/8] Generating cluster data...")
    generate_cluster_assignments()
    generate_cluster_emotions()
    generate_cluster_visualization()
    
    # Step 4: Generate text statistics
    print("\n[Step 4/8] Generating text statistics...")
    generate_text_statistics()
    generate_chapter_similarity()
    
    # Step 5: Generate POS data
    print("\n[Step 5/8] Generating POS data...")
    generate_pos_distribution()
    generate_pos_by_chapter()
    generate_pos_by_cluster()
    
    # Step 6: Generate NER data
    print("\n[Step 6/8] Generating NER data...")
    generate_ner_entities()
    generate_ner_by_chapter()
    generate_ner_counts()
    
    # Step 7: Generate word frequency data
    print("\n[Step 7/8] Generating word frequency data...")
    generate_word_frequencies()
    generate_word_freq_by_cluster()
    generate_word_freq_by_emotion()
    
    print("\n" + "=" * 60)
    print("✓ All mockup data files generated successfully!")
    print("=" * 60)
    print(f"\nFiles saved to: data/mockup/")
    print("\nTo use mockup data, set USE_MOCKUP=true in your environment:")
    print("  export USE_MOCKUP=true")
    print("  streamlit run app/app.py")

if __name__ == "__main__":
    generate_all()

