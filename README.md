# Kettler Data Analysis

Property management licensing investigation platform. Python-first architecture.

## Quick Start

```bash
pip install -r requirements.txt
python bin/run_pipeline.py
```

## Structure

```
bin/              # Entry points
scripts/core/     # Unified modules
scripts/analysis/ # Analysis scripts
scripts/etl/      # ETL pipeline
data/             # Data (source, raw, cleaned, analysis)
research/         # Outputs (connections, violations, anomalies, evidence)
api/              # FastAPI server
web/              # React frontend
```

## Usage

**Pipeline:**
```bash
python bin/run_pipeline.py
```

**Individual:**
```bash
python bin/run_all.py
python bin/analyze_connections.py
python bin/validate_data.py
python bin/generate_reports.py
```

**Unified modules:**
```python
from scripts.core.unified_analysis import UnifiedAnalyzer
analyzer = UnifiedAnalyzer()
analyzer.load_all_data()
analyzer.analyze_all()
```

**Web:**
```bash
cd web && npm run dev  # http://localhost:3000
```

**API:**
```bash
cd api && python server.py  # http://localhost:8000/docs
```

## Key Files

- `data/source/skidmore_all_firms_complete.json` - Firm data (38 firms)
- `research/connections/` - Connection analyses
- `research/violations/` - Violation findings
- `research/anomalies/` - Anomaly reports
- `config/state_dpor_registry.csv` - State registry

## Features

- Multi-state license search
- Connection mapping
- Anomaly detection
- Evidence extraction (PDF/Excel)
- Vector embeddings
- Timeline analysis

## Docs

- [QUICK_START.md](QUICK_START.md)
- [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md)
- [docs/ORGANIZATION.md](docs/ORGANIZATION.md)
