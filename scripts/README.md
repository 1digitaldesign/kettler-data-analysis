# Scripts Directory

**AI-Powered** Python-first analysis scripts organized by function with advanced machine learning capabilities.

## Structure

```
scripts/
├── core/           # Unified modules
├── analysis/       # AI/ML analysis scripts
│   ├── advanced_ml_pipeline.py      # TensorFlow ML pipeline
│   ├── ml_tax_structure_analysis.py # Clustering & anomaly detection
│   ├── embedding_violation_analysis.py # Vector similarity
│   ├── graph_theory_analysis.py     # NetworkX analysis
│   └── utils/
│       └── advanced_visualizations.py # Plotly/Bokeh/Altair
├── extraction/     # Evidence extraction
├── etl/            # ETL and vectorization
├── utils/          # Utilities
└── automation/     # Browser automation
```

## Core Modules

**UnifiedAnalyzer** (`core/unified_analysis.py`) - Analysis operations
**UnifiedInvestigator** (`core/unified_investigation.py`) - Investigation
**UnifiedSearcher** - Search operations
**UnifiedValidator** - Validation
**UnifiedReporter** - Report generation
**UnifiedScraper** - Web scraping

## Usage

```python
from scripts.core import UnifiedAnalyzer

analyzer = UnifiedAnalyzer()
analyzer.load_all_data()
results = analyzer.analyze_all()
```

## Entry Points

Use `bin/` scripts to run analyses:
- `bin/run_pipeline.py` - Full pipeline
- `bin/run_all.py` - All analyses
- `bin/analyze_connections.py` - Connections
- `bin/validate_data.py` - Validation
- `bin/clean_data.py` - Data cleaning
- `bin/generate_reports.py` - Reports
- `bin/organize_evidence.py` - Evidence

## AI/ML Analysis Scripts

**Advanced ML Pipeline** (`analysis/advanced_ml_pipeline.py`)
- TensorFlow-optimized parallel processing
- Sentence Transformers for embeddings
- Vector similarity analysis

**ML Tax Structure Analysis** (`analysis/ml_tax_structure_analysis.py`)
- K-Means, DBSCAN, Hierarchical, Spectral clustering
- Isolation Forest, LOF, One-Class SVM anomaly detection
- Random Forest, XGBoost classification
- SHAP explainability

**Embedding Analysis** (`analysis/embedding_violation_analysis.py`)
- Cosine similarity calculations
- Address/agent clustering
- Violation pattern clustering

**Graph Theory Analysis** (`analysis/graph_theory_analysis.py`)
- NetworkX graph construction
- Community detection (Louvain)
- Centrality measures (PageRank, betweenness, degree)

**Advanced Visualizations** (`analysis/utils/advanced_visualizations.py`)
- Plotly interactive charts
- Bokeh browser visualizations
- Altair statistical plots
- HTML dashboard generation

## Utilities

- `utils/paths.py` - Path management
- `utils/validate_schema.py` - Schema validation
- `utils/add_metadata.py` - Metadata utility
- `analysis/utils/advanced_visualizations.py` - Modern visualization tools

## Related

- [System Architecture](../docs/SYSTEM_ARCHITECTURE.md) - Complete architecture (includes components and data flow)
- [Documentation Index](../docs/INDEX.md) - All documentation
- [README](../README.md) - Main project overview
