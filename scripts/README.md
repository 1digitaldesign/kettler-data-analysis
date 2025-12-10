# Scripts Directory

Python-first analysis scripts organized by function.

## Structure

```
scripts/
├── core/           # Unified modules
├── analysis/       # Analysis scripts
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

## Utilities

- `utils/paths.py` - Path management
- `utils/validate_schema.py` - Schema validation
- `utils/add_metadata.py` - Metadata utility

## Related

- [System Architecture](../docs/SYSTEM_ARCHITECTURE.md)
- [Components](../docs/COMPONENTS.md)
- [Data Flow](../docs/DATA_FLOW.md)
