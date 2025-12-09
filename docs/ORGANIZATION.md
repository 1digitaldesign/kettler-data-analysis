# Organization

## Structure

```
bin/              # Entry points
scripts/          # Library code
  core/           # Unified modules
  analysis/       # Analysis
  extraction/     # Evidence extraction
  etl/            # ETL/vectorization
data/             # Data directories
research/         # Outputs by category
  connections/    # Connection analyses
  violations/     # Violation findings
  anomalies/      # Anomaly reports
  evidence/       # Evidence summaries
  verification/   # Verification results
  timelines/      # Timeline analyses
config/           # Configuration
```

## Paths

Use `scripts/utils/paths.py`:

```python
from scripts.utils.paths import (
    DATA_SOURCE_DIR, RESEARCH_CONNECTIONS_DIR,
    RESEARCH_VIOLATIONS_DIR, RESEARCH_EVIDENCE_DIR
)
```

## Entry Points

- `bin/run_pipeline.py` - Full pipeline
- `bin/run_all.py` - All analyses
- `bin/analyze_connections.py` - Connections
- `bin/validate_data.py` - Validation
- `bin/generate_reports.py` - Reports
