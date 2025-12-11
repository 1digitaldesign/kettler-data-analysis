# Quick Start Guide

Get started with the Kettler Data Analysis platform in minutes.

## About this guide

This guide helps you get started quickly. It covers the essential steps to run your first analysis.

## Prerequisites

- Python 3.14+ installed
- Repository cloned
- Dependencies installed (see [INSTALLATION.md](INSTALLATION.md))

## Quick start steps

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the pipeline

```bash
python bin/run_pipeline.py
```

This runs the complete data processing pipeline.

### Step 3: View results

Results are saved in:
- `research/` - Research outputs
- `data/cleaned/` - Cleaned data
- `outputs/reports/` - Generated reports

## Common tasks

### Run full pipeline

```bash
python bin/run_pipeline.py
```

### Run AI/ML Analysis

```bash
# Advanced ML pipeline with TensorFlow
python scripts/analysis/advanced_ml_pipeline.py

# ML tax structure analysis (clustering, anomaly detection)
python scripts/analysis/ml_tax_structure_analysis.py

# Embedding-based similarity analysis
python scripts/analysis/embedding_violation_analysis.py

# Graph theory network analysis
python scripts/analysis/graph_theory_analysis.py

# Complete violation analysis pipeline
python scripts/analysis/run_complete_violation_analysis.py
```

### Run individual analysis

```bash
python bin/analyze_connections.py
```

### Validate data

```bash
python bin/validate_data.py
```

### Generate reports

```bash
python bin/generate_reports.py
```

## What happens when you run

The pipeline performs these steps:

1. **Data extraction** - Extracts data from sources
2. **Data cleaning** - Cleans and normalizes data
3. **AI/ML Analysis** - ML-enhanced analysis with clustering, anomaly detection, and classification
4. **Connection analysis** - Graph theory and network analysis
5. **Vector embeddings** - Semantic similarity matching
6. **Data validation** - Validates data quality
7. **Visualization generation** - Creates interactive Plotly/Bokeh charts
8. **Report generation** - Generates ML-enhanced reports

## Next steps

After running your first analysis:

- Review [README.md](README.md) for system overview
- Check [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) for complete architecture (includes data flow and components)

## Getting help

- Check [INSTALLATION.md](INSTALLATION.md) for installation issues
- Review [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) for architecture
- See [Documentation Index](docs/INDEX.md) for all documentation

## Related documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md) - Architecture details
- [Documentation Index](docs/INDEX.md) - All documentation
