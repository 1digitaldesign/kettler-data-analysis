#!/usr/bin/env python3
"""
ML utility functions for violation analysis
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional


def normalize_features(feature_matrix: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Normalize feature matrix"""
    mean = np.mean(feature_matrix, axis=0)
    std = np.std(feature_matrix, axis=0)

    # Avoid division by zero
    std = np.where(std == 0, 1.0, std)

    normalized = (feature_matrix - mean) / std

    normalization_params = {
        'mean': mean.tolist(),
        'std': std.tolist()
    }

    return normalized, normalization_params


def calculate_silhouette_score_simple(labels: np.ndarray, features: np.ndarray) -> float:
    """Simple silhouette score calculation"""
    try:
        from sklearn.metrics import silhouette_score
        return float(silhouette_score(features, labels))
    except ImportError:
        # Fallback: return 0 if sklearn not available
        return 0.0


def find_optimal_clusters_kmeans(features: np.ndarray, max_k: int = 10) -> Dict[str, Any]:
    """Find optimal number of clusters using elbow method"""
    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score

        inertias = []
        silhouette_scores = []
        k_range = range(2, min(max_k + 1, len(features)))

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(features)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(features, labels))

        # Find elbow (simplified: minimum of second derivative approximation)
        if len(inertias) > 2:
            diffs = np.diff(inertias)
            second_diffs = np.diff(diffs)
            optimal_k_idx = np.argmax(second_diffs) + 2  # +2 because of double diff
            optimal_k = k_range[optimal_k_idx] if optimal_k_idx < len(k_range) else k_range[-1]
        else:
            optimal_k = k_range[0]

        # Also check silhouette score
        best_silhouette_idx = np.argmax(silhouette_scores)
        optimal_k_silhouette = k_range[best_silhouette_idx]

        return {
            'optimal_k_elbow': int(optimal_k),
            'optimal_k_silhouette': int(optimal_k_silhouette),
            'inertias': [float(x) for x in inertias],
            'silhouette_scores': [float(x) for x in silhouette_scores],
            'k_range': list(k_range)
        }
    except ImportError:
        return {'error': 'sklearn not available'}


def prepare_feature_matrix(entities: List[Dict[str, Any]],
                          feature_extractor) -> Tuple[np.ndarray, List[str]]:
    """Prepare feature matrix from entities"""
    feature_vectors = []
    entity_ids = []

    for entity in entities:
        features = feature_extractor(entity)
        if features:
            feature_vectors.append(list(features.values()))
            entity_ids.append(entity.get('filing_number', ''))

    if not feature_vectors:
        return np.array([]), []

    return np.array(feature_vectors), entity_ids
