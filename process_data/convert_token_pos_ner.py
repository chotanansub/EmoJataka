"""
Convert token_pos_ner.json to CSV files for POS and NER analysis.

This script processes the token_pos_ner.json file which contains:
- Key: Story title (string)
- Value: List of [token, POS_tag, NER_tag]

Outputs 8 CSV files to data/ directory:
1. ner_entities.csv - Individual named entities with counts
2. ner_by_chapter.csv - Entity type counts per chapter
3. ner_counts.csv - Overall entity type statistics
4. pos_distribution.csv - Overall POS tag distribution
5. pos_by_chapter.csv - POS tag distribution per chapter
6. word_frequencies.csv - Overall word frequencies
7. word_freq_by_cluster.csv - Word frequencies per cluster
8. word_freq_by_emotion.csv - Word frequencies per emotion
"""

import json
import re
import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter


class TokenPosNerConverter:
    """Convert token_pos_ner.json to analysis CSV files."""

    def __init__(self, input_path, output_dir):
        """
        Initialize converter.

        Args:
            input_path: Path to token_pos_ner.json
            output_dir: Directory to save output CSV files
        """
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load data
        with open(self.input_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Create chapter mapping (story title -> chapter number)
        self.story_titles = list(self.data.keys())
        self.title_to_chapter = {title: idx + 1 for idx, title in enumerate(self.story_titles)}

    def extract_entities_from_bio(self, tokens):
        """
        Extract named entities from BIO-tagged tokens.

        Args:
            tokens: List of [token, pos_tag, ner_tag]

        Returns:
            List of (entity_text, entity_type) tuples
        """
        entities = []
        current_entity = []
        current_type = None

        for token, pos_tag, ner_tag in tokens:
            if ner_tag.startswith('B-'):
                # Beginning of new entity
                if current_entity:
                    # Save previous entity
                    entities.append((''.join(current_entity), current_type))
                current_entity = [token]
                current_type = ner_tag[2:]  # Remove 'B-' prefix
            elif ner_tag.startswith('I-'):
                # Inside entity
                if current_entity:
                    current_entity.append(token)
                else:
                    # I- without B- (treat as new entity)
                    current_entity = [token]
                    current_type = ner_tag[2:]  # Remove 'I-' prefix
            else:
                # 'O' or other - end of entity
                if current_entity:
                    entities.append((''.join(current_entity), current_type))
                    current_entity = []
                    current_type = None

        # Don't forget last entity
        if current_entity:
            entities.append((''.join(current_entity), current_type))

        return entities

    def generate_ner_entities(self):
        """Generate ner_entities.csv: chapter, entity, entity_type, count"""
        data_rows = []

        for title, tokens in self.data.items():
            chapter = self.title_to_chapter[title]
            entities = self.extract_entities_from_bio(tokens)

            # Count entities
            entity_counts = Counter(entities)

            for (entity_text, entity_type), count in entity_counts.items():
                data_rows.append({
                    'chapter': chapter,
                    'entity': entity_text,
                    'entity_type': entity_type,
                    'count': count
                })

        df = pd.DataFrame(data_rows)
        df = df.sort_values(['chapter', 'entity_type', 'entity'])
        df.to_csv(self.output_dir / 'ner_entities.csv', index=False)
        print(f"✓ Generated ner_entities.csv ({len(df)} rows)")

    def generate_ner_by_chapter(self):
        """Generate ner_by_chapter.csv: chapter, entity_type, count"""
        data_rows = []

        for title, tokens in self.data.items():
            chapter = self.title_to_chapter[title]
            entities = self.extract_entities_from_bio(tokens)

            # Count entity types
            type_counts = Counter(entity_type for _, entity_type in entities)

            for entity_type, count in type_counts.items():
                data_rows.append({
                    'chapter': chapter,
                    'entity_type': entity_type,
                    'count': count
                })

        df = pd.DataFrame(data_rows)
        df = df.sort_values(['chapter', 'entity_type'])
        df.to_csv(self.output_dir / 'ner_by_chapter.csv', index=False)
        print(f"✓ Generated ner_by_chapter.csv ({len(df)} rows)")

    def generate_ner_counts(self):
        """Generate ner_counts.csv: entity_type, count, percentage"""
        all_entities = []

        for title, tokens in self.data.items():
            entities = self.extract_entities_from_bio(tokens)
            all_entities.extend(entity_type for _, entity_type in entities)

        type_counts = Counter(all_entities)
        total = sum(type_counts.values())

        data_rows = []
        for entity_type, count in type_counts.items():
            percentage = round(100 * count / total, 2) if total > 0 else 0
            data_rows.append({
                'entity_type': entity_type,
                'count': count,
                'percentage': percentage
            })

        df = pd.DataFrame(data_rows)
        df = df.sort_values('count', ascending=False)
        df.to_csv(self.output_dir / 'ner_counts.csv', index=False)
        print(f"✓ Generated ner_counts.csv ({len(df)} rows)")

    def generate_pos_distribution(self):
        """Generate pos_distribution.csv: pos_tag, count, percentage"""
        all_pos_tags = []

        for title, tokens in self.data.items():
            all_pos_tags.extend(pos_tag for _, pos_tag, _ in tokens)

        pos_counts = Counter(all_pos_tags)
        total = sum(pos_counts.values())

        data_rows = []
        for pos_tag, count in pos_counts.items():
            percentage = round(100 * count / total, 2) if total > 0 else 0
            data_rows.append({
                'pos_tag': pos_tag,
                'count': count,
                'percentage': percentage
            })

        df = pd.DataFrame(data_rows)
        df = df.sort_values('count', ascending=False)
        df.to_csv(self.output_dir / 'pos_distribution.csv', index=False)
        print(f"✓ Generated pos_distribution.csv ({len(df)} rows)")

    def generate_pos_by_chapter(self):
        """Generate pos_by_chapter.csv: chapter, pos_tag, count, percentage"""
        data_rows = []

        for title, tokens in self.data.items():
            chapter = self.title_to_chapter[title]
            pos_tags = [pos_tag for _, pos_tag, _ in tokens]
            pos_counts = Counter(pos_tags)
            total = len(pos_tags)

            for pos_tag, count in pos_counts.items():
                percentage = round(100 * count / total, 2) if total > 0 else 0
                data_rows.append({
                    'chapter': chapter,
                    'pos_tag': pos_tag,
                    'count': count,
                    'percentage': percentage
                })

        df = pd.DataFrame(data_rows)
        df = df.sort_values(['chapter', 'pos_tag'])
        df.to_csv(self.output_dir / 'pos_by_chapter.csv', index=False)
        print(f"✓ Generated pos_by_chapter.csv ({len(df)} rows)")

    def generate_word_frequencies(self):
        """Generate word_frequencies.csv: word, frequency, rank"""
        all_tokens = []

        # Extract all Thai tokens from all stories
        for title, tokens in self.data.items():
            for token, pos_tag, ner_tag in tokens:
                # Keep only Thai characters
                if re.match(r'^[\u0E00-\u0E7F]+$', token):
                    all_tokens.append(token)

        # Count token frequencies
        token_counts = Counter(all_tokens)

        # Create DataFrame with rank
        data_rows = []
        for rank, (word, frequency) in enumerate(token_counts.most_common(), 1):
            data_rows.append({
                'word': word,
                'frequency': frequency,
                'rank': rank
            })

        df = pd.DataFrame(data_rows)
        df.to_csv(self.output_dir / 'word_frequencies.csv', index=False)
        print(f"✓ Generated word_frequencies.csv ({len(df)} unique words)")

    def generate_word_freq_by_cluster(self):
        """Generate word_freq_by_cluster.csv: cluster, word, frequency, rank"""
        # Load cluster assignments (using mockup for now)
        cluster_path = self.output_dir / 'mockup' / 'cluster_assignments.csv'

        if not cluster_path.exists():
            print(f"⚠ Skipping word_freq_by_cluster.csv - {cluster_path} not found")
            return

        # Load cluster assignments
        cluster_df = pd.read_csv(cluster_path)
        chapter_to_cluster = dict(zip(cluster_df['chapter'], cluster_df['cluster']))

        # Collect tokens by cluster
        cluster_tokens = defaultdict(list)

        for title, tokens in self.data.items():
            chapter = self.title_to_chapter[title]
            cluster = chapter_to_cluster.get(chapter)

            if cluster is not None:
                for token, pos_tag, ner_tag in tokens:
                    # Keep only Thai characters
                    if re.match(r'^[\u0E00-\u0E7F]+$', token):
                        cluster_tokens[cluster].append(token)

        # Count frequencies per cluster
        data_rows = []
        for cluster in sorted(cluster_tokens.keys()):
            token_counts = Counter(cluster_tokens[cluster])

            for rank, (word, frequency) in enumerate(token_counts.most_common(), 1):
                data_rows.append({
                    'cluster': cluster,
                    'word': word,
                    'frequency': frequency,
                    'rank': rank
                })

        df = pd.DataFrame(data_rows)
        df.to_csv(self.output_dir / 'word_freq_by_cluster.csv', index=False)
        print(f"✓ Generated word_freq_by_cluster.csv ({len(df)} rows)")

    def generate_word_freq_by_emotion(self):
        """Generate word_freq_by_emotion.csv: emotion, word, frequency, rank"""
        # Load emotion scores (using mockup for now)
        emotion_path = self.output_dir / 'mockup' / 'emotion_scores.csv'

        if not emotion_path.exists():
            print(f"⚠ Skipping word_freq_by_emotion.csv - {emotion_path} not found")
            return

        # Load emotion scores and find dominant emotion per chapter
        emotion_df = pd.read_csv(emotion_path)

        # Get dominant emotion for each chapter
        chapter_to_emotion = {}
        for chapter in emotion_df['chapter'].unique():
            chapter_data = emotion_df[emotion_df['chapter'] == chapter]
            # Find emotion with highest score
            emotions = ['joy', 'sadness', 'fear', 'anger', 'surprise', 'disgust']
            max_emotion = max(emotions, key=lambda e: chapter_data[e].values[0] if e in chapter_data.columns else 0)
            chapter_to_emotion[chapter] = max_emotion

        # Collect tokens by emotion
        emotion_tokens = defaultdict(list)

        for title, tokens in self.data.items():
            chapter = self.title_to_chapter[title]
            emotion = chapter_to_emotion.get(chapter)

            if emotion is not None:
                for token, pos_tag, ner_tag in tokens:
                    # Keep only Thai characters
                    if re.match(r'^[\u0E00-\u0E7F]+$', token):
                        emotion_tokens[emotion].append(token)

        # Count frequencies per emotion
        data_rows = []
        for emotion in sorted(emotion_tokens.keys()):
            token_counts = Counter(emotion_tokens[emotion])

            for rank, (word, frequency) in enumerate(token_counts.most_common(), 1):
                data_rows.append({
                    'emotion': emotion,
                    'word': word,
                    'frequency': frequency,
                    'rank': rank
                })

        df = pd.DataFrame(data_rows)
        df.to_csv(self.output_dir / 'word_freq_by_emotion.csv', index=False)
        print(f"✓ Generated word_freq_by_emotion.csv ({len(df)} rows)")

    def convert_all(self):
        """Generate all CSV files."""
        print(f"Converting {len(self.data)} stories from {self.input_path}")
        print(f"Output directory: {self.output_dir}\n")

        print("Generating NER files...")
        self.generate_ner_entities()
        self.generate_ner_by_chapter()
        self.generate_ner_counts()

        print("\nGenerating POS files...")
        self.generate_pos_distribution()
        self.generate_pos_by_chapter()

        print("\nGenerating word frequency files...")
        self.generate_word_frequencies()
        self.generate_word_freq_by_cluster()
        self.generate_word_freq_by_emotion()

        print("\n✓ All files generated successfully!")


def main():
    """Main entry point."""
    # Paths relative to script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    input_path = project_root / 'data' / 'token_pos_ner.json'
    output_dir = project_root / 'data'

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    converter = TokenPosNerConverter(input_path, output_dir)
    converter.convert_all()


if __name__ == '__main__':
    main()
