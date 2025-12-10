# Installation Guide

Step-by-step guide to install and set up the Kettler Data Analysis platform.

## Prerequisites

Before installing, ensure you have:

- Python 3.9 or higher
- pip (Python package manager)
- Git
- 2GB free disk space

## Installation steps

### 1. Clone the repository

```bash
git clone https://github.com/1digitaldesign/kettler-data-analysis.git
cd kettler-data-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs all required Python packages including:
- pandas - Data manipulation
- pathlib - Path handling
- json - JSON processing
- Other dependencies listed in `requirements.txt`

### 3. Verify installation

Run a test to verify everything works:

```bash
python bin/run_pipeline.py --help
```

If you see help text, installation is successful.

## System components

The platform consists of:

- **Entry points** (`bin/`) - Scripts to run analyses
- **Core modules** (`scripts/core/`) - Unified analysis modules
- **Analysis scripts** (`scripts/analysis/`) - Analysis operations
- **ETL pipeline** (`scripts/etl/`) - Data processing
- **Data** (`data/`) - Source and processed data
- **Research** (`research/`) - Research outputs

## Next steps

After installation:

1. Read [QUICK_START.md](QUICK_START.md) for quick start guide
2. Review [README.md](README.md) for system overview
3. Check [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) for architecture details

## Troubleshooting

### Issue: pip command not found

**Solution:** Install pip:
```bash
python -m ensurepip --upgrade
```

### Issue: Permission denied

**Solution:** Use virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Package installation fails

**Solution:** Upgrade pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Related documentation

- [Quick Start Guide](QUICK_START.md) - Get started quickly
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md) - Architecture details
- [Documentation Index](docs/INDEX.md) - All documentation
