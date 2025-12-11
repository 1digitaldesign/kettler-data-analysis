#!/usr/bin/env python3
"""
ML-based tax structure analysis with clustering, anomaly detection, and classification
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, RESEARCH_DIR
from scripts.analysis.utils.feature_engineering import extract_all_features
from scripts.analysis.utils.ml_utils import (
    normalize_features, find_optimal_clusters_kmeans, prepare_feature_matrix
)

# Try importing ML libraries
try:
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
    from sklearn.ensemble import IsolationForest, RandomForestClassifier
    from sklearn.neighbors import LocalOutlierFactor
    from sklearn.svm import OneClassSVM
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    SKLEARN_AVAILABLE = True
    try:
        from sklearn.cluster import SpectralClustering
        SPECTRAL_AVAILABLE = True
    except ImportError:
        SPECTRAL_AVAILABLE = False
except ImportError:
    SKLEARN_AVAILABLE = False
    SPECTRAL_AVAILABLE = False
    print("Warning: scikit-learn not available. Some ML features will be disabled.")

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Warning: xgboost not available. XGBoost classifier will be disabled.")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("Warning: networkx not available. Network analysis will be disabled.")

try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    print("Warning: umap-learn not available. UMAP visualization will be disabled.")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("Warning: shap not available. SHAP explainability will be disabled.")

# Modern visualization libraries (preferred)
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Info: Plotly not available. Using fallback visualization libraries.")

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib/seaborn not available. Visualizations will be disabled.")


def load_data() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Load enriched entities, violations, and relationship graph"""
    enriched_file = DATA_PROCESSED_DIR / "lariat_enriched.json"
    violations_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    graph_file = DATA_PROCESSED_DIR / "entity_relationships.json"

    with open(enriched_file, 'r') as f:
        enriched_data = json.load(f)

    with open(violations_file, 'r') as f:
        violations_data = json.load(f)

    with open(graph_file, 'r') as f:
        graph_data = json.load(f)

    return (
        enriched_data.get('entities', {}),
        violations_data.get('violations', {}),
        graph_data.get('graph', {})
    )


def perform_kmeans_clustering(features: np.ndarray, n_clusters: int = None) -> Dict[str, Any]:
    """Perform K-Means clustering"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    if n_clusters is None:
        # Find optimal k
        optimal_k_result = find_optimal_clusters_kmeans(features, max_k=min(10, len(features)))
        n_clusters = optimal_k_result.get('optimal_k_silhouette', 3)

    n_clusters = min(n_clusters, len(features))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features)

    silhouette = silhouette_score(features, labels) if len(set(labels)) > 1 else 0.0

    return {
        'n_clusters': int(n_clusters),
        'cluster_labels': labels.tolist(),
        'cluster_centers': kmeans.cluster_centers_.tolist(),
        'silhouette_score': float(silhouette),
        'inertia': float(kmeans.inertia_)
    }


def perform_dbscan_clustering(features: np.ndarray, eps: float = 0.5, min_samples: int = 2) -> Dict[str, Any]:
    """Perform DBSCAN clustering"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(features)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = int(np.sum(labels == -1))

    return {
        'n_clusters': n_clusters,
        'n_noise': n_noise,
        'cluster_labels': labels.tolist(),
        'outliers': np.where(labels == -1)[0].tolist()
    }


def perform_hierarchical_clustering(features: np.ndarray, n_clusters: int = 3) -> Dict[str, Any]:
    """Perform hierarchical clustering"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    n_clusters = min(n_clusters, len(features))

    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hierarchical.fit_predict(features)

    return {
        'n_clusters': int(n_clusters),
        'cluster_assignments': labels.tolist()
    }


def perform_spectral_clustering(features: np.ndarray, n_clusters: int = 3) -> Dict[str, Any]:
    """Perform spectral clustering on entity relationship graph"""
    if not SKLEARN_AVAILABLE or not SPECTRAL_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn spectral clustering not available or no features'}

    n_clusters = min(n_clusters, len(features))

    spectral = SpectralClustering(n_clusters=n_clusters, random_state=42, affinity='rbf')
    labels = spectral.fit_predict(features)

    return {
        'n_clusters': int(n_clusters),
        'cluster_labels': labels.tolist()
    }


def detect_anomalies_isolation_forest(features: np.ndarray, contamination: float = 0.1) -> Dict[str, Any]:
    """Detect anomalies using Isolation Forest"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    predictions = iso_forest.fit_predict(features)
    scores = iso_forest.score_samples(features)

    anomalies = np.where(predictions == -1)[0].tolist()

    return {
        'anomaly_scores': scores.tolist(),
        'anomaly_labels': predictions.tolist(),
        'anomalies_detected': anomalies,
        'n_anomalies': len(anomalies)
    }


def detect_anomalies_lof(features: np.ndarray, n_neighbors: int = 5) -> Dict[str, Any]:
    """Detect anomalies using Local Outlier Factor"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    n_neighbors = min(n_neighbors, len(features) - 1)

    lof = LocalOutlierFactor(n_neighbors=n_neighbors)
    predictions = lof.fit_predict(features)
    scores = lof.negative_outlier_factor_

    anomalies = np.where(predictions == -1)[0].tolist()

    return {
        'lof_scores': scores.tolist(),
        'anomaly_labels': predictions.tolist(),
        'anomalies_detected': anomalies,
        'n_anomalies': len(anomalies)
    }


def detect_anomalies_oneclass_svm(features: np.ndarray, nu: float = 0.1) -> Dict[str, Any]:
    """Detect anomalies using One-Class SVM"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    oc_svm = OneClassSVM(nu=nu, kernel='rbf')
    predictions = oc_svm.fit_predict(features)
    scores = oc_svm.score_samples(features)

    anomalies = np.where(predictions == -1)[0].tolist()

    return {
        'oc_svm_scores': scores.tolist(),
        'anomaly_labels': predictions.tolist(),
        'anomalies_detected': anomalies,
        'n_anomalies': len(anomalies)
    }


def classify_violation_likelihood(features: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
    """Classify violation likelihood using Random Forest"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    if len(set(labels)) < 2:
        return {'error': 'Need at least 2 classes for classification'}

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(features, labels)

    predictions = rf.predict(features)
    probabilities = rf.predict_proba(features)

    feature_importance = {
        f'feature_{i}': float(importance)
        for i, importance in enumerate(rf.feature_importances_)
    }

    # Calculate SHAP values if available
    shap_values = {}
    if SHAP_AVAILABLE:
        try:
            explainer = shap.TreeExplainer(rf)
            shap_vals = explainer.shap_values(features)
            # For binary classification, use the positive class
            if isinstance(shap_vals, list) and len(shap_vals) > 1:
                shap_values = {
                    f'feature_{i}': float(shap_vals[1][0][i]) if len(shap_vals[1]) > 0 else 0.0
                    for i in range(features.shape[1])
                }
            elif isinstance(shap_vals, np.ndarray):
                shap_values = {
                    f'feature_{i}': float(shap_vals[0][i]) if len(shap_vals) > 0 else 0.0
                    for i in range(features.shape[1])
                }
        except Exception as e:
            shap_values = {'error': str(e)}

    return {
        'predictions': predictions.tolist(),
        'probabilities': probabilities.tolist(),
        'feature_importance': feature_importance,
        'shap_values': shap_values,
        'accuracy': float(np.mean(predictions == labels))
    }


def classify_xgboost(features: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
    """Classify using XGBoost"""
    if not XGBOOST_AVAILABLE or len(features) == 0:
        return {'error': 'xgboost not available or no features'}

    if len(set(labels)) < 2:
        return {'error': 'Need at least 2 classes for classification'}

    xgb_model = xgb.XGBClassifier(random_state=42)
    xgb_model.fit(features, labels)

    predictions = xgb_model.predict(features)
    probabilities = xgb_model.predict_proba(features)

    feature_importance = {
        f'feature_{i}': float(importance)
        for i, importance in enumerate(xgb_model.feature_importances_)
    }

    return {
        'predictions': predictions.tolist(),
        'probabilities': probabilities.tolist(),
        'feature_importance': feature_importance,
        'accuracy': float(np.mean(predictions == labels))
    }


def analyze_network(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze entity relationship network"""
    if not NETWORKX_AVAILABLE:
        return {'error': 'networkx not available'}

    G = nx.Graph()

    # Add nodes
    for node in graph.get('nodes', []):
        G.add_node(node.get('id'), **node)

    # Add edges
    for edge in graph.get('edges', []):
        G.add_edge(
            edge.get('source'),
            edge.get('target'),
            **{k: v for k, v in edge.items() if k not in ['source', 'target']}
        )

    if len(G.nodes()) == 0:
        return {'error': 'Empty graph'}

    # Calculate centrality measures
    try:
        pagerank = nx.pagerank(G)
        betweenness = nx.betweenness_centrality(G)
        degree_centrality = nx.degree_centrality(G)
    except:
        return {'error': 'Could not calculate centrality'}

    # Community detection
    try:
        communities = list(nx.community.greedy_modularity_communities(G))
    except:
        communities = []

    return {
        'n_nodes': len(G.nodes()),
        'n_edges': len(G.edges()),
        'pagerank': {str(k): float(v) for k, v in pagerank.items()},
        'betweenness_centrality': {str(k): float(v) for k, v in betweenness.items()},
        'degree_centrality': {str(k): float(v) for k, v in degree_centrality.items()},
        'communities': [list(c) for c in communities],
        'n_communities': len(communities)
    }


def perform_pca(features: np.ndarray, n_components: int = 2) -> Dict[str, Any]:
    """Perform PCA dimensionality reduction"""
    if not SKLEARN_AVAILABLE or len(features) == 0:
        return {'error': 'sklearn not available or no features'}

    n_components = min(n_components, features.shape[1], features.shape[0])

    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(features)

    return {
        'transformed_features': transformed.tolist(),
        'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
        'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist()
    }


def perform_umap(features: np.ndarray, n_components: int = 2) -> Dict[str, Any]:
    """Perform UMAP dimensionality reduction"""
    if not UMAP_AVAILABLE or len(features) == 0:
        return {'error': 'umap not available or no features'}

    reducer = umap.UMAP(n_components=n_components, random_state=42)
    embedding = reducer.fit_transform(features)

    return {
        'umap_embedding': embedding.tolist()
    }


def analyze_time_series_violations(entities: List[Dict[str, Any]],
                                   violations: Dict[str, List]) -> Dict[str, Any]:
    """Analyze violation patterns over time"""
    from datetime import datetime, timedelta
    from collections import defaultdict

    # Extract violation dates
    violation_dates = []
    violation_by_month = defaultdict(int)
    violation_by_year = defaultdict(int)

    for violation_type, violation_list in violations.items():
        for violation in violation_list:
            date_str = violation.get('filing_date') or violation.get('effective_date')
            if date_str:
                try:
                    if isinstance(date_str, str):
                        violation_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        continue
                    violation_dates.append(violation_date)

                    # Group by month and year
                    month_key = violation_date.strftime('%Y-%m')
                    year_key = violation_date.year
                    violation_by_month[month_key] += 1
                    violation_by_year[year_key] += 1
                except Exception as e:
                    continue

    # Calculate trends
    trends = {}
    if len(violation_by_year) > 1:
        years = sorted(violation_by_year.keys())
        counts = [violation_by_year[y] for y in years]

        # Simple linear trend
        if len(counts) > 1:
            trend_slope = (counts[-1] - counts[0]) / len(counts) if len(counts) > 1 else 0
            trends['yearly_trend'] = {
                'slope': float(trend_slope),
                'direction': 'increasing' if trend_slope > 0 else 'decreasing' if trend_slope < 0 else 'stable',
                'years': years,
                'counts': counts
            }

    # Seasonal patterns (by month)
    monthly_patterns = {}
    if violation_by_month:
        months = sorted(violation_by_month.keys())
        month_counts = [violation_by_month[m] for m in months]

        # Extract month numbers for seasonal analysis
        month_numbers = [int(m.split('-')[1]) for m in months]
        monthly_patterns = {
            'months': months,
            'counts': month_counts,
            'month_numbers': month_numbers
        }

    # Entity lifecycle analysis
    lifecycle_stages = defaultdict(int)
    lifecycle_transitions = []

    for entity in entities:
        filing_date_str = entity.get('original_filing_date')
        status = entity.get('status', '').lower()

        if filing_date_str:
            try:
                filing_date = datetime.fromisoformat(filing_date_str)
                current_date = datetime.now()
                days_existed = (current_date - filing_date).days

                # Determine lifecycle stage
                if 'forfeited' in status:
                    lifecycle_stages['forfeited'] += 1
                elif days_existed < 365:
                    lifecycle_stages['new'] += 1
                elif days_existed < 1825:  # 5 years
                    lifecycle_stages['established'] += 1
                else:
                    lifecycle_stages['mature'] += 1

                # Check for forfeiture -> reinstatement pattern
                filing_history = entity.get('filing_history', [])
                has_forfeiture = any('Tax Forfeiture' in str(f) for f in filing_history)
                has_reinstatement = any('Reinstatement' in str(f) for f in filing_history)

                if has_forfeiture and has_reinstatement:
                    lifecycle_transitions.append({
                        'entity_id': entity.get('filing_number'),
                        'pattern': 'forfeiture_reinstatement'
                    })
            except:
                pass

    # Predict future violations (simple trend-based)
    predictions = {}
    if trends.get('yearly_trend'):
        trend_data = trends['yearly_trend']
        if len(trend_data['years']) > 0:
            last_year = trend_data['years'][-1]
            last_count = trend_data['counts'][-1]
            slope = trend_data['slope']

            # Predict next year
            next_year = last_year + 1
            predicted_count = max(0, int(last_count + slope))

            predictions['next_year'] = {
                'year': next_year,
                'predicted_violations': predicted_count,
                'confidence': 'low'  # Simple trend, low confidence
            }

    return {
        'violation_trends': trends,
        'seasonal_patterns': monthly_patterns,
        'lifecycle_analysis': {
            'stages': dict(lifecycle_stages),
            'transitions': lifecycle_transitions,
            'forfeiture_reinstatement_count': len(lifecycle_transitions)
        },
        'predictions': predictions,
        'summary': {
            'total_violations_over_time': len(violation_dates),
            'violation_months': len(violation_by_month),
            'violation_years': len(violation_by_year),
            'entities_in_lifecycle': sum(lifecycle_stages.values())
        }
    }


def generate_visualizations(clustering_results: Dict[str, Any],
                            features: np.ndarray,
                            entity_ids: List[str],
                            network_results: Dict[str, Any],
                            time_series_results: Dict[str, Any],
                            relationship_graph: Dict[str, Any],
                            output_dir: Path) -> Dict[str, str]:
    """Generate visualization plots"""
    visualizations = {}

    if not MATPLOTLIB_AVAILABLE:
        return {'error': 'matplotlib not available'}

    output_dir.mkdir(parents=True, exist_ok=True)

    # Cluster visualization (K-Means)
    if 'kmeans' in clustering_results and 'cluster_labels' in clustering_results['kmeans']:
        try:
            labels = clustering_results['kmeans']['cluster_labels']
            if len(features) >= 2:
                # Use PCA for 2D visualization
                pca = PCA(n_components=2)
                features_2d = pca.fit_transform(features)

                plt.figure(figsize=(10, 8))
                scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1],
                                    c=labels, cmap='viridis', alpha=0.6)
                plt.colorbar(scatter)
                plt.title('K-Means Clustering Visualization (PCA-reduced)')
                plt.xlabel('First Principal Component')
                plt.ylabel('Second Principal Component')

                cluster_file = output_dir / "kmeans_clusters.png"
                plt.savefig(cluster_file, dpi=150, bbox_inches='tight')
                plt.close()
                visualizations['kmeans_cluster_plot'] = str(cluster_file)
        except Exception as e:
            visualizations['kmeans_cluster_plot'] = f'error: {str(e)}'

    # Network visualization
    if NETWORKX_AVAILABLE and relationship_graph:
        try:
            G = nx.Graph()
            # Add nodes
            for node in relationship_graph.get('nodes', []):
                G.add_node(node.get('id'), **node)

            # Add edges
            for edge in relationship_graph.get('edges', []):
                G.add_edge(
                    edge.get('source'),
                    edge.get('target'),
                    **{k: v for k, v in edge.items() if k not in ['source', 'target']}
                )

            if len(G.nodes()) > 0:
                plt.figure(figsize=(12, 10))
                pos = nx.spring_layout(G, k=1, iterations=50)
                nx.draw(G, pos, with_labels=True, node_color='lightblue',
                       node_size=500, font_size=8, font_weight='bold', alpha=0.7)
                plt.title('Entity Relationship Network')

                network_file = output_dir / "network_graph.png"
                plt.savefig(network_file, dpi=150, bbox_inches='tight')
                plt.close()
                visualizations['network_graph'] = str(network_file)
        except Exception as e:
            visualizations['network_graph'] = f'error: {str(e)}'

    # Time series visualization
    if 'violation_trends' in time_series_results:
        trends = time_series_results.get('violation_trends', {})
        if 'yearly_trend' in trends:
            try:
                trend_data = trends['yearly_trend']
                years = trend_data.get('years', [])
                counts = trend_data.get('counts', [])

                if years and counts:
                    plt.figure(figsize=(10, 6))
                    plt.plot(years, counts, marker='o', linewidth=2, markersize=8)
                    plt.title('Violation Trends Over Time')
                    plt.xlabel('Year')
                    plt.ylabel('Number of Violations')
                    plt.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)

                    ts_file = output_dir / "time_series_trends.png"
                    plt.savefig(ts_file, dpi=150, bbox_inches='tight')
                    plt.close()
                    visualizations['time_series_chart'] = str(ts_file)
            except Exception as e:
                visualizations['time_series_chart'] = f'error: {str(e)}'

    return visualizations


def calculate_risk_scores(entities: List[Dict[str, Any]],
                         clustering_results: Dict[str, Any],
                         anomaly_results: Dict[str, Any],
                         classification_results: Dict[str, Any],
                         network_results: Dict[str, Any]) -> Dict[str, float]:
    """Calculate ML-enhanced risk scores"""
    risk_scores = {}

    entity_ids = [e.get('filing_number') for e in entities]

    for i, entity_id in enumerate(entity_ids):
        score = 0.0

        # Anomaly score contribution
        if 'anomaly_scores' in anomaly_results:
            anomaly_score = anomaly_results['anomaly_scores'][i]
            # Normalize to 0-1 range (lower score = higher risk for isolation forest)
            score += (1.0 - min(max(anomaly_score, -1), 1)) / 2.0

        # Clustering contribution (outliers in DBSCAN)
        if 'cluster_labels' in clustering_results.get('dbscan', {}):
            labels = clustering_results['dbscan']['cluster_labels']
            if labels[i] == -1:  # Outlier
                score += 0.3

        # Classification probability
        if 'probabilities' in classification_results:
            probs = classification_results['probabilities'][i]
            if len(probs) > 1:
                score += max(probs)  # Probability of violation class

        # Network centrality
        if 'pagerank' in network_results:
            pagerank = network_results['pagerank'].get(str(entity_id), 0.0)
            score += min(pagerank * 10, 0.2)  # Cap contribution

        risk_scores[entity_id] = min(score, 1.0)  # Cap at 1.0

    return risk_scores


def main():
    """Main ML analysis function"""
    print("=" * 60)
    print("ML-Based Tax Structure Analysis")
    print("=" * 60)

    # Load data
    print("\n1. Loading data...")
    entities_dict, violations, relationship_graph = load_data()

    entities = list(entities_dict.values())
    print(f"   Loaded {len(entities)} entities")

    # Extract features
    print("\n2. Extracting features...")
    feature_matrix, entity_ids = prepare_feature_matrix(
        entities,
        lambda e: extract_all_features(e, relationship_graph, violations)
    )

    if len(feature_matrix) == 0:
        print("Error: No features extracted")
        return

    print(f"   Extracted {feature_matrix.shape[1]} features for {len(feature_matrix)} entities")

    # Normalize features
    print("\n3. Normalizing features...")
    normalized_features, norm_params = normalize_features(feature_matrix)

    # Clustering
    print("\n4. Performing clustering analysis...")
    clustering_results = {}

    kmeans_result = perform_kmeans_clustering(normalized_features)
    clustering_results['kmeans'] = kmeans_result
    print(f"   K-Means: {kmeans_result.get('n_clusters', 0)} clusters, "
          f"silhouette: {kmeans_result.get('silhouette_score', 0):.3f}")

    dbscan_result = perform_dbscan_clustering(normalized_features)
    clustering_results['dbscan'] = dbscan_result
    print(f"   DBSCAN: {dbscan_result.get('n_clusters', 0)} clusters, "
          f"{dbscan_result.get('n_noise', 0)} outliers")

    hierarchical_result = perform_hierarchical_clustering(normalized_features)
    clustering_results['hierarchical'] = hierarchical_result
    print(f"   Hierarchical: {hierarchical_result.get('n_clusters', 0)} clusters")

    if SPECTRAL_AVAILABLE:
        spectral_result = perform_spectral_clustering(normalized_features)
        clustering_results['spectral'] = spectral_result
        if 'error' not in spectral_result:
            print(f"   Spectral: {spectral_result.get('n_clusters', 0)} clusters")
        else:
            print(f"   Spectral: Not available")
    else:
        clustering_results['spectral'] = {'error': 'Spectral clustering not available'}

    # Anomaly detection
    print("\n5. Detecting anomalies...")
    anomaly_results = {}

    iso_result = detect_anomalies_isolation_forest(normalized_features)
    anomaly_results['isolation_forest'] = iso_result
    print(f"   Isolation Forest: {iso_result.get('n_anomalies', 0)} anomalies")

    lof_result = detect_anomalies_lof(normalized_features)
    anomaly_results['lof'] = lof_result
    print(f"   LOF: {lof_result.get('n_anomalies', 0)} anomalies")

    oc_svm_result = detect_anomalies_oneclass_svm(normalized_features)
    anomaly_results['one_class_svm'] = oc_svm_result
    print(f"   One-Class SVM: {oc_svm_result.get('n_anomalies', 0)} anomalies")

    # Classification (create labels from violations)
    print("\n6. Classification analysis...")
    violation_labels = np.array([
        1.0 if any(
            v.get('filing_number') == entity_ids[i]
            for violation_list in violations.values()
            for v in violation_list
        ) else 0.0
        for i in range(len(entity_ids))
    ])

    classification_results = {}

    if len(set(violation_labels)) > 1:
        rf_result = classify_violation_likelihood(normalized_features, violation_labels)
        classification_results['random_forest'] = rf_result
        print(f"   Random Forest accuracy: {rf_result.get('accuracy', 0):.3f}")

        if XGBOOST_AVAILABLE:
            xgb_result = classify_xgboost(normalized_features, violation_labels)
            classification_results['xgboost'] = xgb_result
            print(f"   XGBoost accuracy: {xgb_result.get('accuracy', 0):.3f}")

    # Network analysis
    print("\n7. Network analysis...")
    network_results = analyze_network(relationship_graph)
    if 'n_nodes' in network_results:
        print(f"   Network: {network_results['n_nodes']} nodes, "
              f"{network_results['n_edges']} edges, "
              f"{network_results.get('n_communities', 0)} communities")

    # Dimensionality reduction
    print("\n8. Dimensionality reduction...")
    pca_result = perform_pca(normalized_features)
    if 'transformed_features' in pca_result:
        print(f"   PCA: Explained variance: {sum(pca_result['explained_variance_ratio']):.3f}")

    umap_result = perform_umap(normalized_features) if UMAP_AVAILABLE else {}

    # Time series analysis
    print("\n9. Time series analysis...")
    time_series_results = analyze_time_series_violations(entities, violations)
    if 'summary' in time_series_results:
        ts_summary = time_series_results['summary']
        print(f"   Violations over time: {ts_summary.get('total_violations_over_time', 0)}")
        print(f"   Lifecycle stages: {sum(time_series_results.get('lifecycle_analysis', {}).get('stages', {}).values())} entities")

        trends = time_series_results.get('violation_trends', {})
        if 'yearly_trend' in trends:
            direction = trends['yearly_trend'].get('direction', 'unknown')
            print(f"   Yearly trend: {direction}")

    # Risk scoring
    print("\n10. Calculating risk scores...")
    risk_scores = calculate_risk_scores(
        entities, clustering_results, anomaly_results,
        classification_results, network_results
    )

    # Generate visualizations
    print("\n11. Generating visualizations...")
    viz_dir = RESEARCH_DIR / "texas" / "analysis" / "visualizations"
    visualizations = generate_visualizations(
        clustering_results, normalized_features, entity_ids,
        network_results, time_series_results, relationship_graph, viz_dir
    )
    if visualizations:
        print(f"   Generated {len([v for v in visualizations.values() if 'error' not in str(v)])} visualizations")
    else:
        print("   No visualizations generated")

    # Save results
    output_file = DATA_PROCESSED_DIR / "ml_tax_structure_analysis.json"
    results = {
        'clustering_results': clustering_results,
        'anomaly_detection': anomaly_results,
        'classification': classification_results,
        'network_analysis': network_results,
        'dimensionality_reduction': {
            'pca': pca_result,
            'umap': umap_result
        },
        'time_series_analysis': time_series_results,
        'risk_scores': risk_scores,
        'visualizations': visualizations,
        'feature_normalization': norm_params,
        'summary': {
            'total_entities': len(entities),
            'n_features': feature_matrix.shape[1],
            'n_clusters_kmeans': clustering_results.get('kmeans', {}).get('n_clusters', 0),
            'n_anomalies': anomaly_results.get('isolation_forest', {}).get('n_anomalies', 0),
            'n_communities': network_results.get('n_communities', 0),
            'time_series_violations': time_series_results.get('summary', {}).get('total_violations_over_time', 0)
        },
        'metadata': {
            'generated': datetime.now().isoformat(),
            'source': 'ml_tax_structure_analysis.py',
            'ml_libraries': {
                'sklearn': SKLEARN_AVAILABLE,
                'xgboost': XGBOOST_AVAILABLE,
                'networkx': NETWORKX_AVAILABLE,
                'umap': UMAP_AVAILABLE,
                'shap': SHAP_AVAILABLE,
                'matplotlib': MATPLOTLIB_AVAILABLE
            }
        }
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Save models if possible (simplified - just metadata for now)
    models_dir = RESEARCH_DIR / "texas" / "analysis" / "ml_models"
    models_dir.mkdir(parents=True, exist_ok=True)

    models_metadata = {
        'clustering_models': {
            'kmeans': {'n_clusters': clustering_results.get('kmeans', {}).get('n_clusters', 0)},
            'dbscan': {'n_clusters': clustering_results.get('dbscan', {}).get('n_clusters', 0)},
            'hierarchical': {'n_clusters': clustering_results.get('hierarchical', {}).get('n_clusters', 0)},
            'spectral': {'n_clusters': clustering_results.get('spectral', {}).get('n_clusters', 0)}
        },
        'anomaly_detection_models': {
            'isolation_forest': {'n_anomalies': anomaly_results.get('isolation_forest', {}).get('n_anomalies', 0)},
            'lof': {'n_anomalies': anomaly_results.get('lof', {}).get('n_anomalies', 0)},
            'one_class_svm': {'n_anomalies': anomaly_results.get('one_class_svm', {}).get('n_anomalies', 0)}
        },
        'classification_models': {
            'random_forest': {'accuracy': classification_results.get('random_forest', {}).get('accuracy', 0)},
            'xgboost': {'accuracy': classification_results.get('xgboost', {}).get('accuracy', 0)} if XGBOOST_AVAILABLE else {}
        },
        'metadata': {
            'generated': datetime.now().isoformat(),
            'n_features': feature_matrix.shape[1],
            'n_entities': len(entities)
        }
    }

    models_file = models_dir / "models_metadata.json"
    with open(models_file, 'w') as f:
        json.dump(models_metadata, f, indent=2, default=str)

    print(f"\n✓ ML analysis complete!")
    print(f"  Results saved to: {output_file}")
    print(f"  Models metadata saved to: {models_file}")
    if visualizations:
        print(f"  Visualizations saved to: {viz_dir}")


if __name__ == '__main__':
    main()
