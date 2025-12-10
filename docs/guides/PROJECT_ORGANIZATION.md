# Project Organization

## Structure

```mermaid
graph TB
    ROOT[Project Root] --> BIN[bin/<br/>Entry Scripts]
    ROOT --> SCRIPTS[scripts/<br/>Library Code]
    ROOT --> DATA[data/<br/>Data]
    ROOT --> RESEARCH[research/<br/>Research Outputs]
    ROOT --> EVIDENCE[evidence/<br/>Source Documents]
    ROOT --> FILINGS[filings/<br/>Filing Materials]

    SCRIPTS --> CORE[core/<br/>Unified Modules]
    SCRIPTS --> ANALYSIS[analysis/<br/>Analysis]
    SCRIPTS --> EXTRACTION[extraction/<br/>Evidence Extraction]

    DATA --> SOURCE[source/]
    DATA --> RAW[raw/]
    DATA --> CLEANED[cleaned/]

    RESEARCH --> CONN[connections/]
    RESEARCH --> VIOL[violations/]
    RESEARCH --> ANOM[anomalies/]

    style ROOT fill:#D1C4E9
    style DATA fill:#C8E6C9
    style RESEARCH fill:#E1BEE7
```

**Text Structure:**

```
bin/              # Entry scripts
scripts/          # Library code
  core/           # Unified modules
  analysis/       # Analysis
  extraction/     # Evidence extraction
data/             # Data
research/         # Outputs by category
evidence/         # Source documents
filings/          # Filing materials
```

## Data Flow

```mermaid
flowchart LR
    A[Source] --> B[Raw]
    B --> C[Cleaned]
    C --> D[Analysis]
    D --> E[Research Outputs]

    A --> A1[data/source/]
    B --> B1[data/raw/]
    C --> C1[data/cleaned/]
    D --> D1[scripts/core/]
    E --> E1[research/]

    style A fill:#C8E6C9
    style C fill:#FFF9C4
    style E fill:#E1BEE7
```

**Text Flow:**

Source → Raw → Cleaned → Analysis → Research Outputs

## Research Categories

- `connections/` - Connection analyses
- `violations/` - Violation findings
- `anomalies/` - Anomaly reports
- `evidence/` - Evidence summaries
- `verification/` - Verification results
- `timelines/` - Timeline analyses
