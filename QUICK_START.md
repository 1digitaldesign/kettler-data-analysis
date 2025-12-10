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
3. **Connection analysis** - Analyzes connections
4. **Data validation** - Validates data quality
5. **Report generation** - Generates reports

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
