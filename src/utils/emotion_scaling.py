"""Emotion score scaling utilities for visualization enhancement.

This module provides scaling methods to highlight differences in emotion scores,
which are probability distributions that often cluster tightly around 0.125 (1/8).
"""

from typing import Dict, Tuple


# Baseline for uniform distribution across 8 emotions
UNIFORM_BASELINE = 0.125

# Global min/max values observed across all 314 chapters
# These are used for consistent scaling across the entire dataset
GLOBAL_EMOTION_MIN = 0.104088  # Minimum score observed (disgust in chapter 64)
GLOBAL_EMOTION_MAX = 0.177014  # Maximum score observed (trust in chapter 64)

# Scaling strength parameter for min-max method
# - strength < 1.0 (e.g., 0.5): Makes differences MORE prominent (square root effect)
# - strength = 1.0: No change (linear scaling)
# - strength > 1.0 (e.g., 2.0): Makes differences LESS prominent (square effect)
# Recommended values: 0.3-0.7 for highlighting top emotions
MINMAX_SCALING_STRENGTH = 1  # Adjust this value to control peak prominence


def scale_emotion_scores(
    emotion_scores: Dict[str, float],
    method: str = 'minmax'
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Scale emotion scores to highlight differences between emotions.

    Args:
        emotion_scores: Dictionary mapping emotion names to raw scores
        method: Scaling method to use:
            - 'minmax': Min-max normalization within chapter (0-1 range)
            - 'baseline': Percentage above/below uniform baseline (0.125)
            - 'raw': No scaling (returns original scores)

    Returns:
        Tuple of (scaled_scores, raw_scores) dictionaries
    """
    if not emotion_scores:
        return {}, {}

    # Keep raw scores for reference
    raw_scores = emotion_scores.copy()

    if method == 'raw':
        return raw_scores, raw_scores

    elif method == 'minmax':
        # Global min-max normalization: scale using global min/max across ALL chapters
        # This ensures consistent scaling - only the true global extremes get 0.0 or 1.0

        # Step 1: Normalize to 0-1 range using global min/max
        normalized = {
            emotion: (score - GLOBAL_EMOTION_MIN) / (GLOBAL_EMOTION_MAX - GLOBAL_EMOTION_MIN)
            for emotion, score in emotion_scores.items()
        }

        # Step 2: Apply power transformation to adjust peak prominence
        # Values < 1.0 make high values higher and low values lower (more separation)
        # Values > 1.0 compress the differences
        scaled = {
            emotion: max(0.0, min(1.0, value ** MINMAX_SCALING_STRENGTH))
            for emotion, value in normalized.items()
        }

        return scaled, raw_scores

    elif method == 'baseline':
        # Show percentage above/below uniform distribution
        # Normalize to 0-1 range for visualization
        # Max observed score is ~0.177, min is ~0.104
        # Range from baseline: -0.021 to +0.052

        max_deviation = 0.052  # Maximum observed deviation above baseline

        scaled = {}
        for emotion, score in emotion_scores.items():
            deviation = score - UNIFORM_BASELINE
            # Normalize: 0 = at baseline, 1 = maximum above baseline
            if deviation >= 0:
                scaled[emotion] = min(1.0, deviation / max_deviation)
            else:
                # Below baseline: map to 0-0.5 range
                # Minimum observed is -0.021 below baseline
                scaled[emotion] = max(0.0, 0.5 + (deviation / 0.021) * 0.5)

        return scaled, raw_scores

    else:
        # Default to raw if unknown method
        return raw_scores, raw_scores


def get_scaling_description(method: str) -> str:
    """
    Get a human-readable description of the scaling method.

    Args:
        method: The scaling method name

    Returns:
        Description string for UI display
    """
    descriptions = {
        'minmax': (
            "**Highlight Differences (Min-Max)**: Scales emotions using global min/max "
            "values across all 314 chapters (0.104-0.177). Scores close to 1.0 indicate "
            "emotions near the dataset maximum, while scores near 0.0 are near the minimum. "
            "Provides consistent comparison across all stories."
        ),
        'baseline': (
            "**Above/Below Baseline**: Shows how much each emotion deviates from "
            "uniform distribution (12.5%). Values near 0.5 are close to baseline, "
            "1.0 means highly over-represented, 0.0 means highly under-represented."
        ),
        'raw': (
            "**Raw Scores**: Original probability scores as predicted by the model. "
            "All emotions sum to 1.0 (100%). Small visual differences due to tight "
            "clustering around 0.125 (12.5%)."
        )
    }
    return descriptions.get(method, "Unknown scaling method")


def format_score_display(
    emotion: str,
    scaled_score: float,
    raw_score: float,
    method: str
) -> str:
    """
    Format score display for hover text and labels.

    Args:
        emotion: Emotion name
        scaled_score: Scaled score value
        raw_score: Original raw score
        method: Scaling method used

    Returns:
        Formatted string for display
    """
    emotion_display = emotion.title()

    if method == 'raw':
        return f"{emotion_display}: {raw_score:.4f}"
    else:
        return f"{emotion_display}: {scaled_score:.3f} (raw: {raw_score:.4f})"
