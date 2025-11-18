"""Emotion score scaling utilities for visualization enhancement.

This module provides scaling methods to highlight differences in emotion scores,
which are probability distributions that often cluster tightly around 0.125 (1/8).
"""

from typing import Dict, Tuple


# Baseline for uniform distribution across 8 emotions
UNIFORM_BASELINE = 0.125


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
        # Min-max normalization: scale to 0-1 range within this chapter
        min_score = min(emotion_scores.values())
        max_score = max(emotion_scores.values())

        # Handle edge case where all scores are identical
        if max_score == min_score:
            scaled = {emotion: 0.5 for emotion in emotion_scores}
        else:
            scaled = {
                emotion: (score - min_score) / (max_score - min_score)
                for emotion, score in emotion_scores.items()
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
            "**Highlight Differences (Min-Max)**: Scales emotions within each chapter "
            "so the highest emotion = 1.0 and lowest = 0.0. Best for seeing relative "
            "importance of emotions within a story."
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
