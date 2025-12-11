#!/usr/bin/env python3
"""
Generate comprehensive ML-enhanced violation report
Combines all analysis results into JSON report and Markdown summary
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, RESEARCH_DIR


def load_all_analysis_results() -> Dict[str, Any]:
    """Load all analysis results"""
    results = {}

    # Load violations
    violations_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    if violations_file.exists():
        with open(violations_file, 'r') as f:
            results['violations'] = json.load(f)

    # Load embedding analysis
    embedding_file = DATA_PROCESSED_DIR / "embedding_similarity_analysis.json"
    if embedding_file.exists():
        with open(embedding_file, 'r') as f:
            results['embedding'] = json.load(f)

    # Load cross-referenced data
    crossref_file = DATA_PROCESSED_DIR / "cross_referenced_violations.json"
    if crossref_file.exists():
        with open(crossref_file, 'r') as f:
            results['cross_reference'] = json.load(f)

    # Load ML analysis
    ml_file = DATA_PROCESSED_DIR / "ml_tax_structure_analysis.json"
    if ml_file.exists():
        with open(ml_file, 'r') as f:
            results['ml_analysis'] = json.load(f)

    # Load enriched entities
    enriched_file = DATA_PROCESSED_DIR / "lariat_enriched.json"
    if enriched_file.exists():
        with open(enriched_file, 'r') as f:
            results['entities'] = json.load(f)

    return results


def generate_executive_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate executive summary"""
    violations = results.get('violations', {}).get('summary', {})
    ml_summary = results.get('ml_analysis', {}).get('summary', {})
    embedding_summary = results.get('embedding', {}).get('summary', {})

    total_violations = violations.get('total_violations', 0)
    high_severity = violations.get('high_severity', 0)
    entities_with_violations = violations.get('entities_with_violations', 0)

    # Calculate ML risk score range
    risk_scores = results.get('ml_analysis', {}).get('risk_scores', {})
    risk_values = list(risk_scores.values()) if risk_scores else []

    ml_risk_range = {
        'min': min(risk_values) if risk_values else 0.0,
        'max': max(risk_values) if risk_values else 0.0,
        'mean': sum(risk_values) / len(risk_values) if risk_values else 0.0
    }

    anomalies_detected = ml_summary.get('n_anomalies', 0)

    # Determine risk level
    if high_severity > 0 or anomalies_detected > 0 or ml_risk_range['mean'] > 0.5:
        risk_level = 'HIGH'
    elif total_violations > 0 or ml_risk_range['mean'] > 0.3:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'

    return {
        'total_violations': total_violations,
        'high_risk_entities': len([v for v in risk_values if v > 0.7]) if risk_values else 0,
        'violation_clusters': embedding_summary.get('address_clusters', 0) + \
                            embedding_summary.get('agent_clusters', 0),
        'ml_risk_score_range': ml_risk_range,
        'anomalies_detected': anomalies_detected,
        'risk_level': risk_level
    }


def generate_detailed_findings(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate detailed findings"""
    violations = results.get('violations', {}).get('violations', {})
    ml_analysis = results.get('ml_analysis', {})
    embedding = results.get('embedding', {})
    crossref = results.get('cross_reference', {})

    # Violations by entity
    violations_by_entity = {}
    for violation_type, violation_list in violations.items():
        for violation in violation_list:
            filing_num = violation.get('filing_number')
            if filing_num:
                if filing_num not in violations_by_entity:
                    violations_by_entity[filing_num] = []
                violations_by_entity[filing_num].append({
                    'type': violation_type,
                    'violation': violation
                })

    # Clustering results with interpretations
    clustering = ml_analysis.get('clustering_results', {})

    # Add cluster interpretations
    cluster_interpretations = {}
    if 'kmeans' in clustering:
        kmeans_data = clustering['kmeans']
        cluster_interpretations['kmeans'] = {
            'n_clusters': kmeans_data.get('n_clusters', 0),
            'silhouette_score': kmeans_data.get('silhouette_score', 0.0),
            'interpretation': f"K-Means identified {kmeans_data.get('n_clusters', 0)} distinct tax structure groups"
        }

    if 'dbscan' in clustering:
        dbscan_data = clustering['dbscan']
        cluster_interpretations['dbscan'] = {
            'n_clusters': dbscan_data.get('n_clusters', 0),
            'n_outliers': dbscan_data.get('n_noise', 0),
            'interpretation': f"DBSCAN found {dbscan_data.get('n_clusters', 0)} clusters and {dbscan_data.get('n_noise', 0)} outliers"
        }

    clustering['cluster_interpretations'] = cluster_interpretations

    # ML predictions
    ml_predictions = {
        'violation_likelihood': {},
        'anomaly_scores': {},
        'risk_scores': ml_analysis.get('risk_scores', {}),
        'feature_importance': ml_analysis.get('classification', {}).get('random_forest', {}).get('feature_importance', {}),
        'shap_values': ml_analysis.get('classification', {}).get('random_forest', {}).get('shap_values', {})
    }

    # Network analysis
    network_analysis = ml_analysis.get('network_analysis', {})

    # Time series analysis
    time_series_analysis = ml_analysis.get('time_series_analysis', {})

    return {
        'violations_by_entity': violations_by_entity,
        'clustering_results': clustering,
        'ml_predictions': ml_predictions,
        'network_analysis': network_analysis,
        'time_series_analysis': time_series_analysis,
        'violation_clusters': embedding.get('violation_clusters', []),
        'similarity_analysis': embedding.get('similarity_analysis', {}),
        'risk_assessment': {
            'risk_scores': ml_analysis.get('risk_scores', {}),
            'high_risk_entities': [
                {'entity_id': k, 'risk_score': v}
                for k, v in ml_analysis.get('risk_scores', {}).items()
                if v > 0.7
            ]
        },
        'visualizations': ml_analysis.get('visualizations', {})
    }


def generate_recommendations(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate recommendations based on findings"""
    recommendations = []

    violations = results.get('violations', {}).get('summary', {})
    ml_summary = results.get('ml_analysis', {}).get('summary', {})
    anomalies = ml_summary.get('n_anomalies', 0)

    if violations.get('total_violations', 0) > 0:
        recommendations.append({
            'priority': 'HIGH',
            'recommendation': 'Investigate tax forfeiture events for potential tax evasion',
            'details': f"{violations.get('total_violations', 0)} violations identified"
        })

    if anomalies > 0:
        recommendations.append({
            'priority': 'HIGH',
            'recommendation': 'Review ML-detected anomalies for unusual tax structures',
            'details': f"{anomalies} anomalies detected by Isolation Forest and LOF"
        })

    risk_scores = results.get('ml_analysis', {}).get('risk_scores', {})
    high_risk = [k for k, v in risk_scores.items() if v > 0.7]
    if high_risk:
        recommendations.append({
            'priority': 'HIGH',
            'recommendation': 'Prioritize investigation of high-risk entities',
            'details': f"{len(high_risk)} entities with ML risk score > 0.7"
        })

    clustering = results.get('ml_analysis', {}).get('clustering_results', {})
    dbscan = clustering.get('dbscan', {})
    if dbscan.get('n_noise', 0) > 0:
        recommendations.append({
            'priority': 'MEDIUM',
            'recommendation': 'Examine DBSCAN outliers for potential shell companies',
            'details': f"{dbscan.get('n_noise', 0)} outliers detected"
        })

    return recommendations


def generate_markdown_summary(results: Dict[str, Any], output_path: Path):
    """Generate Markdown summary report"""
    exec_summary = generate_executive_summary(results)
    detailed = generate_detailed_findings(results)
    recommendations = generate_recommendations(results)

    md_content = f"""# ML-Enhanced Violation Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Total Violations**: {exec_summary['total_violations']}
- **High-Risk Entities**: {exec_summary['high_risk_entities']}
- **Violation Clusters**: {exec_summary['violation_clusters']}
- **Anomalies Detected**: {exec_summary['anomalies_detected']}
- **Risk Level**: {exec_summary['risk_level']}
- **ML Risk Score Range**: {exec_summary['ml_risk_score_range']['min']:.3f} - {exec_summary['ml_risk_score_range']['max']:.3f} (mean: {exec_summary['ml_risk_score_range']['mean']:.3f})

## Key Findings

### Violations by Type

"""

    violations = results.get('violations', {}).get('violations', {})
    for violation_type, violation_list in violations.items():
        md_content += f"- **{violation_type}**: {len(violation_list)} violations\n"

    md_content += "\n### ML Analysis Results\n\n"

    ml_summary = results.get('ml_analysis', {}).get('summary', {})
    md_content += f"- **Clusters (K-Means)**: {ml_summary.get('n_clusters_kmeans', 0)}\n"
    md_content += f"- **Anomalies Detected**: {ml_summary.get('n_anomalies', 0)}\n"
    md_content += f"- **Network Communities**: {ml_summary.get('n_communities', 0)}\n"

    # Add visualization references
    ml_analysis = results.get('ml_analysis', {})
    visualizations = ml_analysis.get('visualizations', {})
    if visualizations and 'error' not in str(visualizations):
        md_content += "\n### Visualizations\n\n"
        if 'kmeans_cluster_plot' in visualizations:
            md_content += f"- [K-Means Cluster Plot](visualizations/kmeans_clusters.png)\n"
        if 'network_graph' in visualizations:
            md_content += f"- [Network Graph](visualizations/network_graph.png)\n"
        if 'time_series_chart' in visualizations:
            md_content += f"- [Time Series Trends](visualizations/time_series_trends.png)\n"

    # Add visualization references
    visualizations = results.get('ml_analysis', {}).get('visualizations', {})
    if visualizations:
        md_content += "\n### Visualizations\n\n"
        for viz_name, viz_path in visualizations.items():
            if 'error' not in str(viz_path):
                md_content += f"- **{viz_name.replace('_', ' ').title()}**: `{viz_path}`\n"

    md_content += "\n### High-Risk Entities\n\n"
    high_risk = detailed.get('risk_assessment', {}).get('high_risk_entities', [])
    for entity in high_risk[:10]:  # Top 10
        md_content += f"- Entity {entity.get('entity_id')}: Risk Score {entity.get('risk_score', 0):.3f}\n"

    md_content += "\n## Recommendations\n\n"
    for i, rec in enumerate(recommendations, 1):
        md_content += f"{i}. **[{rec['priority']}]** {rec['recommendation']}\n"
        md_content += f"   - {rec['details']}\n\n"

    with open(output_path, 'w') as f:
        f.write(md_content)


def main():
    """Main report generation function"""
    print("=" * 60)
    print("ML-Enhanced Violation Report Generation")
    print("=" * 60)

    # Load all results
    print("\n1. Loading analysis results...")
    results = load_all_analysis_results()

    if not results:
        print("Error: No analysis results found. Run analysis scripts first.")
        return

    print("   Loaded results from:")
    for key in results.keys():
        print(f"     - {key}")

    # Generate executive summary
    print("\n2. Generating executive summary...")
    exec_summary = generate_executive_summary(results)
    print(f"   Total violations: {exec_summary['total_violations']}")
    print(f"   Risk level: {exec_summary['risk_level']}")

    # Generate detailed findings
    print("\n3. Generating detailed findings...")
    detailed = generate_detailed_findings(results)

    # Generate recommendations
    print("\n4. Generating recommendations...")
    recommendations = generate_recommendations(results)
    print(f"   Generated {len(recommendations)} recommendations")

    # Create output directories
    output_dir = RESEARCH_DIR / "texas" / "analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    viz_dir = output_dir / "visualizations"
    viz_dir.mkdir(parents=True, exist_ok=True)

    models_dir = output_dir / "ml_models"
    models_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON report
    print("\n5. Saving JSON report...")
    json_file = output_dir / "ml_comprehensive_violations_analysis.json"
    # Determine which ML models were actually used
    ml_analysis_data = results.get('ml_analysis', {})
    ml_libs = ml_analysis_data.get('metadata', {}).get('ml_libraries', {})

    ml_models_used = []
    if ml_analysis_data.get('clustering_results', {}).get('kmeans'):
        ml_models_used.append('kmeans')
    if ml_analysis_data.get('clustering_results', {}).get('dbscan'):
        ml_models_used.append('dbscan')
    if ml_analysis_data.get('clustering_results', {}).get('hierarchical'):
        ml_models_used.append('hierarchical')
    if ml_analysis_data.get('clustering_results', {}).get('spectral'):
        ml_models_used.append('spectral')
    if ml_analysis_data.get('anomaly_detection', {}).get('isolation_forest'):
        ml_models_used.append('isolation_forest')
    if ml_analysis_data.get('anomaly_detection', {}).get('lof'):
        ml_models_used.append('lof')
    if ml_analysis_data.get('anomaly_detection', {}).get('one_class_svm'):
        ml_models_used.append('one_class_svm')
    if ml_analysis_data.get('classification', {}).get('random_forest'):
        ml_models_used.append('random_forest')
    if ml_analysis_data.get('classification', {}).get('xgboost'):
        ml_models_used.append('xgboost')

    clustering_algorithms = ['kmeans', 'dbscan', 'hierarchical']
    if ml_analysis_data.get('clustering_results', {}).get('spectral'):
        clustering_algorithms.append('spectral')

    report = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'sources': ['embeddings', 'raw_text', 'research_data'],
            'analysis_version': '3.0',
            'ml_models_used': ml_models_used,
            'clustering_algorithms': clustering_algorithms
        },
        'executive_summary': exec_summary,
        'detailed_findings': detailed,
        'recommendations': recommendations
    }

    with open(json_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"   Saved to: {json_file}")

    # Generate Markdown summary
    print("\n6. Generating Markdown summary...")
    md_file = output_dir / "ml_violations_summary.md"
    generate_markdown_summary(results, md_file)
    print(f"   Saved to: {md_file}")

    print("\n" + "=" * 60)
    print("Report generation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
