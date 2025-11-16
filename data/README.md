# Data Directory

This directory contains the datasets used by the EmoJataka application.

## Data Loading Behavior

The app uses **adaptive mode** by default:
1. First tries to load from `data/` (real data)
2. Falls back to `data/mockup/` if file not found

## Real Data Files (Included in Git)

✅ Available:
- `jataka_stories.csv` - Main Jataka stories dataset
- `text_statistics.csv` - Text statistics per chapter
- `pos_distribution.csv` - Part-of-speech distribution
- `pos_by_chapter.csv` - POS tags by chapter
- `ner_entities.csv` - Named entity recognition results
- `ner_by_chapter.csv` - NER by chapter
- `ner_counts.csv` - NER counts
- `word_frequencies.csv` - Overall word frequencies
- `word_freq_by_cluster.csv` - Word frequencies by cluster
- `word_freq_by_emotion.csv` - Word frequencies by emotion
- `word_freq_by_pos.csv` - Word frequencies by POS tag
- `word_freq_by_ner.csv` - Word frequencies by NER type

⚠️ Missing (falls back to mockup):
- `emotion_scores.csv` - Emotion scores per chapter
- `cluster_assignments.csv` - Cluster assignments
- `cluster_emotions.csv` - Emotion statistics by cluster
- `overall_emotions.csv` - Overall emotion statistics
- `emotion_words_found.csv` - Emotion words found in text
- `chapter_similarity.csv` - Chapter similarity matrix
- `cluster_visualization.csv` - 2D cluster visualization coordinates
- `pos_by_cluster.csv` - POS distribution by cluster

## Mockup Data

The `mockup/` directory contains placeholder data for development and testing.
These files are small placeholders used when real data is not available.

## Generating Missing Data Files

To generate the missing real data files, you need to run the data processing pipeline.
The missing files are typically generated from emotion analysis and clustering steps.
