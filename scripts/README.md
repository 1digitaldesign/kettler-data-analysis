# Scripts Directory

Python-first analysis scripts organized by function.

## Structure

```
scripts/
├── core/           # Unified modules (UnifiedAnalyzer, UnifiedSearcher, etc.)
├── analysis/       # Analysis scripts
├── extraction/     # Evidence extraction
├── etl/            # ETL and vectorization
├── microservices/  # Microservice implementations
├── architecture/   # Architecture patterns
└── utils/          # Utilities (paths, helpers)
```

## Core Modules (`core/`)

**UnifiedAnalyzer** - Analysis operations
**UnifiedSearcher** - Search operations
**UnifiedValidator** - Validation
**UnifiedReporter** - Report generation
**UnifiedInvestigator** - Investigation
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
