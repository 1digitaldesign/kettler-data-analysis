# Data Flow

## Pipeline

```mermaid
flowchart LR
    A[Source Data<br/>data/source/] --> B[Extraction<br/>scripts/extraction/]
    B --> C[Raw Data<br/>data/raw/]
    C --> D[Cleaning<br/>bin/clean_data.py]
    D --> E[Cleaned Data<br/>data/cleaned/]
    E --> F[Analysis<br/>scripts/core/]
    F --> G[Research Outputs<br/>research/]

    G --> H[connections/]
    G --> I[summaries/]
    G --> J[verification/]
    G --> K[violations/]
    G --> L[anomalies/]
    G --> M[timelines/]

    style A fill:#C8E6C9
    style E fill:#FFF9C4
    style G fill:#E1BEE7
    style H fill:#D1C4E9
    style I fill:#D1C4E9
    style J fill:#D1C4E9
    style K fill:#D1C4E9
    style L fill:#D1C4E9
    style M fill:#D1C4E9
```

## Text Pipeline

```
1. Source Data (data/source/)
   ↓
2. Extraction (scripts/extraction/)
   ↓
3. Raw Data (data/raw/)
   ↓
4. Cleaning (bin/clean_data.py)
   ↓
5. Cleaned Data (data/cleaned/)
   ↓
6. Analysis (scripts/core/, scripts/analysis/)
   ↓
7. Research Outputs (research/{category}/)
```

## Data Types

**Source:**
- `data/source/skidmore_all_firms_complete.json` - 38 firms
- `data/source/skidmore_individual_licenses.json` - Individual licenses

**Raw:**
- `data/raw/` - Search results (gitignored)

**Cleaned:**
- `data/cleaned/` - Standardized data (gitignored)

**Research:**
- `research/connections/dpor_skidmore_connections.csv` - Connections
- `research/verification/dpor_validated.csv` - Validated data
- `research/summaries/analysis_summary.json` - Summary

**Research:**
- `research/connections/` - Connection analyses
- `research/violations/` - Violation findings
- `research/anomalies/` - Anomaly reports
- `research/evidence/` - Evidence summaries

## Processing Steps

1. **Load** - Read source data
2. **Extract** - Extract from PDFs/Excel
3. **Transform** - Clean and standardize
4. **Analyze** - Run analyses
5. **Store** - Save to research outputs
