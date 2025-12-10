# System Analyst Guide

![Guide](https://img.shields.io/badge/guide-system%20analyst-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)

## System Purpose

Multi-state property management licensing investigation platform. Analyzes connections, violations, and anomalies across 50 states.

## Architecture Overview

| Aspect | Description |
|--------|-------------|
| **Type** | Python-first microservices architecture |
| **Pattern** | Unified modules + microservices + API + Web frontend |
| **Language** | Python (primary), R (deprecated) |

## Component Map

```mermaid
graph TD
    subgraph "Entry Layer"
        E1[run_pipeline.py]
        E2[run_all.py]
    end

    subgraph "Core Layer"
        C1[UnifiedAnalyzer]
        C2[UnifiedSearcher]
        C3[UnifiedValidator]
        C4[UnifiedReporter]
    end

    subgraph "Analysis Layer"
        A1[Analysis Scripts]
    end

    subgraph "ETL Layer"
        ETL1[Vector Embeddings]
    end

    subgraph "API Layer"
        API1[FastAPI Server]
    end

    subgraph "Web Layer"
        WEB1[React Frontend]
    end

    subgraph "Microservices"
        MS1[API Gateway]
        MS2[Analysis Service]
        MS3[Vector Service]
    end

    E1 --> C1
    E2 --> C1
    C1 --> C2
    C1 --> C3
    C1 --> C4
    C1 --> A1
    C1 --> ETL1
    API1 --> C1
    API1 --> WEB1
    API1 --> MS1
    MS1 --> MS2
    MS1 --> MS3

    style E1 fill:#B3E5FC
    style C1 fill:#FFF9C4
    style API1 fill:#F8BBD0
    style MS1 fill:#E1BEE7
```

## Data Flow

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

    style A fill:#C8E6C9
    style E fill:#FFF9C4
    style G fill:#E1BEE7
```

## Key Components

<details>
<summary><b>UnifiedAnalyzer</b></summary>

**Input:** Source Data
**Operations:** Analysis operations
**Output:** Results

**Features:**
- ✅ Connection analysis
- ✅ Pattern detection
- ✅ Anomaly identification

</details>

<details>
<summary><b>UnifiedSearcher</b></summary>

**Input:** Queries
**Operations:** Search operations
**Output:** Results

**Features:**
- ✅ Multi-state license searches
- ✅ Database queries
- ✅ Web scraping

</details>

<details>
<summary><b>UnifiedValidator</b></summary>

**Input:** Data
**Operations:** Validation
**Output:** Validation reports

**Features:**
- ✅ Schema validation
- ✅ FK/PK integrity checks
- ✅ Data quality reports

</details>

## Entry Points

| Script | Purpose | Output |
|--------|---------|--------|
| `bin/run_pipeline.py` | Full pipeline | All outputs |
| `bin/run_all.py` | All analyses | Research outputs |
| `bin/analyze_connections.py` | Connections | `research/connections/` |
| `bin/validate_data.py` | Validation | `research/verification/` |

## Data Organization

<details>
<summary><b>Source Data</b> (`data/source/`)</summary>

- `skidmore_all_firms_complete.json` - 38 firms
- `skidmore_individual_licenses.json` - Individual licenses

</details>

<details>
<summary><b>Cleaned Data</b> (`data/cleaned/`)</summary>

- `firms.json` - Cleaned firm data
- `individual_licenses.json` - Cleaned license data

</details>

<details>
<summary><b>Research Outputs</b> (`research/`)</summary>

- `connections/` - Connection analyses
- `violations/` - Violation findings
- `anomalies/` - Anomaly reports
- `evidence/` - Evidence summaries
- `verification/` - Verification results
- `summaries/` - Summary reports
- `timelines/` - Timeline analyses

</details>

## Quick Reference

**Run Pipeline:**
```bash
python bin/run_pipeline.py
```

**Validate Schema:**
```bash
python scripts/utils/validate_schema.py --file data/cleaned/firms.json
```

**Load Data:**
```python
from scripts.core import UnifiedAnalyzer
analyzer = UnifiedAnalyzer()
analyzer.load_all_data()
```

## Related Documentation

- [System Architecture](SYSTEM_ARCHITECTURE.md) - Architecture details
- [Data Flow](DATA_FLOW.md) - Pipeline documentation
- [Components](COMPONENTS.md) - Component reference
- [Repository Structure](REPOSITORY_STRUCTURE.md) - Structure details
