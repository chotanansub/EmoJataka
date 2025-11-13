# Jataka Tales Emotion Analysis

A Streamlit-based interactive dashboard for analyzing emotions in 300 Jataka tales (Buddhist stories) using the NRC Emotion Lexicon.

## Project Overview

This project analyzes emotions in 313 chapters of Jataka tales written in Thai language. The analysis includes:

- **8 Basic Emotions**: trust, joy, anger, anticipation, fear, disgust, surprise, sadness
- **Analysis Levels**: Overall, cluster-level (K-means), and chapter-level
- **Additional Analysis**: POS tagging, NER, word frequency, text statistics

## Features

### 📊 Five Main Pages

1. **🏠 Overview**: Dataset statistics and overall emotion distribution
2. **🌟 Emotion Analysis**: Detailed emotion profiles with star plots and bar charts
   - All stories combined
   - By story group (cluster)
   - Individual story analysis
3. **🎭 Story Groups**: K-means cluster visualization and comparison
4. **📖 Story Explorer**: Search and explore individual chapters
5. **📊 Text Insights**: Word clouds, POS tags, and named entities

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd EmoJataka
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment (optional):
```bash
cp .env.example .env
# Edit .env to set DATA_MODE=mockup (or adaptive/real) as needed
```

## Running the App

### Using Real Data

Place your data files in the `data/` directory:
- `jataka_stories.csv`
- `emotion_scores.csv`
- `cluster_assignments.csv`
- `cluster_emotions.csv`
- `overall_emotions.csv`
- And other required CSV files (see `instruction/project_structure.md`)

Then run:
```bash
streamlit run app/app.py
```

### Using Mockup Data

1. Generate mockup data (if generators are available):
```bash
python utils/mockup_generator/generate_all.py
```

2. Set environment variable:
```bash
export DATA_MODE=mockup  # or set to adaptive for automatic fallback
# legacy: export USE_MOCKUP=true
```

3. Run the app:
```bash
streamlit run app/app.py
```

## Project Structure

```
EmoJataka/
├── app/
│   ├── app.py                 # Main Streamlit app
│   ├── pages/                 # Streamlit pages
│   ├── components/            # Reusable components
│   └── assets/                # CSS styles
├── src/
│   ├── utils/                 # Data loading utilities
│   └── visualization/         # Visualization modules
├── data/                      # Data files (CSV)
│   └── mockup/                # Mockup data for testing
├── utils/                     # Utility scripts
└── docs/                      # Documentation
```

## Data Files

The app expects the following CSV files in the `data/` directory:

- **Core Data**:
  - `jataka_stories.csv`: Story text and metadata
  - `emotion_scores.csv`: Emotion scores per chapter
  - `cluster_assignments.csv`: Cluster assignments
  - `cluster_emotions.csv`: Average emotions per cluster
  - `overall_emotions.csv`: Overall emotion statistics

- **Additional Data**:
  - `text_statistics.csv`: Text statistics
  - `pos_distribution.csv`, `pos_by_chapter.csv`, `pos_by_cluster.csv`: POS tagging results
  - `ner_entities.csv`, `ner_by_chapter.csv`, `ner_counts.csv`: NER results
  - `word_frequencies.csv`, `word_freq_by_cluster.csv`, `word_freq_by_emotion.csv`: Word frequencies
  - `emotion_words_found.csv`: Emotion words found in text
  - `chapter_similarity.csv`: Chapter similarity matrix
  - `cluster_visualization.csv`: 2D coordinates for cluster visualization

## Configuration

The app uses environment variables for configuration:

- `DATA_MODE`: Controls where data is loaded from (defaults to `adaptive` when not set). Options:
  - `real` (default): load only from `data/`
  - `mockup`: load only from `data/mockup/`
  - `adaptive`: prefer `data/` when the file exists, otherwise fall back to `data/mockup/`
- `USE_MOCKUP`: Legacy flag (still supported). When `true`, behaves like `DATA_MODE=mockup`.

## Technologies Used

- **Streamlit**: Web app framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **WordCloud**: Word cloud generation
- **Matplotlib**: Plotting support

## Development

### Adding New Pages

1. Create a new file in `app/pages/`
2. Use `st.set_page_config()` to configure the page
3. The page will automatically appear in the Streamlit sidebar

### Adding New Visualizations

Add new visualization functions to `src/visualization/` modules.

### Data Loading

Use functions from `src/utils/data_loader.py` to load data. The loader respects the `DATA_MODE` setting (with optional per-call overrides) and can automatically fall back to mockup data when `DATA_MODE=adaptive`.

## Acknowledgments

- NRC Emotion Lexicon for emotion detection
- PyThaiNLP for Thai language processing
- Jataka tales dataset
