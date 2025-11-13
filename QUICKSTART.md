# Quick Start Guide

## Running the Streamlit App

### Option 1: With Real Data

1. Place your CSV data files in the `data/` directory
2. Run the app:
```bash
streamlit run app/app.py
```

### Option 2: With Mockup Data

1. Set environment variable:
```bash
export USE_MOCKUP=true
```

2. Run the app:
```bash
streamlit run app/app.py
```

## Expected Data Files

The app expects CSV files in `data/` (or `data/mockup/` if `USE_MOCKUP=true`):

### Required Core Files:
- `jataka_stories.csv` - Story text and metadata (columns: chapter, title, text)
- `emotion_scores.csv` - Emotion scores per chapter (columns: chapter, trust, joy, anger, anticipation, fear, disgust, surprise, sadness)
- `cluster_assignments.csv` - Cluster assignments (columns: chapter, cluster)
- `cluster_emotions.csv` - Average emotions per cluster (columns: cluster, trust, joy, ...)
- `overall_emotions.csv` - Overall emotion statistics (columns: trust, joy, ...)

### Optional Files (for full functionality):
- `text_statistics.csv` - Text statistics
- `pos_distribution.csv` - POS tag distribution
- `ner_entities.csv` - Named entities
- `word_frequencies.csv` - Word frequencies
- `cluster_visualization.csv` - 2D coordinates for scatter plot (columns: chapter, x, y, cluster)
- And others as specified in `instruction/project_structure.md`

## App Structure

- **Main App**: `app/app.py` - Landing page
- **Pages**: `app/pages/` - Five main pages:
  1. `page_overview.py` - Overview and statistics
  2. `page_emotion_analysis.py` - Emotion analysis with tabs
  3. `page_story_groups.py` - Cluster visualization
  4. `page_story_explorer.py` - Individual story explorer
  5. `page_text_insights.py` - Word clouds, POS, NER

## Troubleshooting

### Import Errors
If you see import errors, make sure you're running from the project root:
```bash
cd /path/to/EmoJataka
streamlit run app/app.py
```

### Missing Data Files
The app will show informative messages if data files are missing. You can:
1. Generate mockup data (if generators are available)
2. Set `USE_MOCKUP=true` to use mockup data
3. Add your real data files to the `data/` directory

### Page Not Showing
Streamlit automatically detects pages in `app/pages/`. If a page doesn't appear:
- Check that the file is in `app/pages/`
- Check for syntax errors in the page file
- Restart the Streamlit server

## Next Steps

1. Review the README.md for detailed documentation
2. Check `instruction/` directory for project context
3. Customize visualizations in `src/visualization/`
4. Add your data files to `data/`

