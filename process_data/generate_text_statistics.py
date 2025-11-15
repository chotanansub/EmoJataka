"""
Generate text_statistics.csv from token_pos_ner.json.

This script calculates word statistics for each story:
- Total words (tokens)
- Unique words

Output: data/text_statistics.csv
"""

import json
import re
import pandas as pd
from pathlib import Path
from collections import Counter


def generate_text_statistics(input_path: Path, output_dir: Path):
    """
    Generate text statistics from token_pos_ner.json.

    Args:
        input_path: Path to token_pos_ner.json
        output_dir: Directory to save output CSV
    """
    print(f"Loading data from {input_path}...")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Processing {len(data)} stories...")

    # Create chapter mapping
    story_titles = list(data.keys())
    title_to_chapter = {title: idx + 1 for idx, title in enumerate(story_titles)}

    stats_data = []

    for title, tokens in data.items():
        chapter = title_to_chapter[title]

        # Extract Thai tokens only
        thai_tokens = []
        for token, pos_tag, ner_tag in tokens:
            if re.match(r'^[\u0E00-\u0E7F]+$', token):
                thai_tokens.append(token)

        # Calculate statistics
        total_words = len(thai_tokens)
        unique_words = len(set(thai_tokens))

        stats_data.append({
            'chapter': chapter,
            'total_words': total_words,
            'unique_words': unique_words
        })

    # Create DataFrame
    df = pd.DataFrame(stats_data)
    df = df.sort_values('chapter')

    # Save to CSV
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'text_statistics.csv'
    df.to_csv(output_path, index=False)

    print(f"\n✓ Generated text_statistics.csv ({len(df)} stories)")
    print(f"  Saved to: {output_path}")
    print(f"\nStatistics Summary:")
    print(f"  Total words across all stories: {df['total_words'].sum():,}")
    print(f"  Average words per story: {df['total_words'].mean():.1f}")
    print(f"  Min words: {df['total_words'].min()}")
    print(f"  Max words: {df['total_words'].max()}")
    print(f"  Average unique words: {df['unique_words'].mean():.1f}")

    return df


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    input_path = project_root / 'data' / 'token_pos_ner.json'
    output_dir = project_root / 'data'

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    generate_text_statistics(input_path, output_dir)


if __name__ == '__main__':
    main()
