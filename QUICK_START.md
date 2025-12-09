# Quick Start

## Install

```bash
pip install -r requirements.txt
cp .env.example .env  # Configure as needed
```

## Run

```bash
# Full pipeline
python bin/run_pipeline.py

# Individual
python bin/run_all.py
python bin/analyze_connections.py
python bin/validate_data.py
python bin/generate_reports.py

# Web
cd web && npm run dev

# API
cd api && python server.py
```

## Structure

- `bin/` - Entry scripts
- `scripts/core/` - Unified modules
- `data/` - Data files
- `research/` - Outputs by category

## Config

- `config/state_dpor_registry.csv` - State registry
- `.env` - Environment variables (GCP, HuggingFace)
