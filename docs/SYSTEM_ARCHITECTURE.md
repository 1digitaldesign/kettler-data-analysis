# System Architecture

![Architecture](https://img.shields.io/badge/architecture-python--first-blue)
![Status](https://img.shields.io/badge/status-operational-brightgreen)

## Overview

Python-first data analysis platform with microservices architecture.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Entry Layer"
        A[bin/run_pipeline.py] --> B[bin/run_all.py]
        A --> C[bin/analyze_connections.py]
        A --> D[bin/validate_data.py]
    end

    subgraph "Core Modules"
        E[UnifiedAnalyzer] --> F[UnifiedSearcher]
        E --> G[UnifiedValidator]
        E --> H[UnifiedReporter]
        E --> I[UnifiedInvestigator]
        E --> J[UnifiedScraper]
    end

    subgraph "Data Layer"
        K[data/source/] --> L[data/raw/]
        L --> M[data/cleaned/]
        M --> N[data/vectors/]
    end

    subgraph "Research Layer"
        O[research/connections/] --> P[research/violations/]
        O --> Q[research/anomalies/]
        O --> R[research/summaries/]
        O --> S[research/verification/]
        O --> T[research/timelines/]
    end

    B --> E
    C --> E
    D --> G
    E --> O
    G --> S
    H --> R

    style A fill:#B3E5FC
    style E fill:#FFF9C4
    style K fill:#C8E6C9
    style O fill:#E1BEE7
```

## Layers

<details>
<summary><b>Entry Layer</b> (`bin/`)</summary>

- Entry point scripts
- Pipeline orchestration

**Scripts:**
- `run_pipeline.py` - Full pipeline
- `run_all.py` - All analyses
- `analyze_connections.py` - Connections
- `validate_data.py` - Validation

</details>

<details>
<summary><b>Core Layer</b> (`scripts/core/`)</summary>

- UnifiedAnalyzer - Analysis operations
- UnifiedSearcher - Search operations
- UnifiedValidator - Validation
- UnifiedReporter - Report generation
- UnifiedInvestigator - Investigation
- UnifiedScraper - Web scraping

</details>

<details>
<summary><b>Analysis Layer</b> (`scripts/analysis/`)</summary>

- Analysis scripts
- Pattern detection
- Fraud analysis

</details>

<details>
<summary><b>ETL Layer</b> (`scripts/etl/`)</summary>

- Vector embeddings
- Data transformation
- Pipeline orchestration

</details>

<details>
<summary><b>API Layer</b> (`api/`)</summary>

- FastAPI REST API
- Endpoints for all operations
- Interactive API docs

</details>

<details>
<summary><b>Web Layer</b> (`web/`)</summary>

- React frontend
- Interactive analysis
- Data visualization

</details>

<details>
<summary><b>Microservices</b> (`microservices/`)</summary>

- API Gateway
- Analysis Service
- Vector Service
- Validation Service

</details>

<details>
<summary><b>Data Layer</b> (`data/`, `research/`)</summary>

- Source data
- Processed data
- Analysis outputs

</details>

## Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **UnifiedAnalyzer** | Analysis operations |
| **UnifiedSearcher** | Search operations |
| **UnifiedValidator** | Data validation |
| **UnifiedReporter** | Report generation |
| **ETL Pipeline** | Vector embeddings and transformation |
| **API Gateway** | Request routing |
| **Analysis Service** | Distributed analysis |

## Integration Points

- Core modules → Data layer
- API → Core modules
- Web → API
- Microservices → Core modules
- ETL → Vector storage

## Data Schema (ER Diagram)

```mermaid
erDiagram
    FIRMS ||--o{ CONNECTIONS : "has"
    INDIVIDUAL_LICENSES ||--o{ CONNECTIONS : "has"
    FIRMS ||--o| INDIVIDUAL_LICENSES : "principal_broker"
    FIRMS ||--o{ RESEARCH_OUTPUTS : "analyzed_in"
    INDIVIDUAL_LICENSES ||--o{ RESEARCH_OUTPUTS : "analyzed_in"
    FIRMS ||--o{ VIOLATIONS : "violates"
    INDIVIDUAL_LICENSES ||--o{ VIOLATIONS : "violates"
    VIOLATIONS ||--o{ EVIDENCE : "supported_by"

    FIRMS {
        string firm_license PK
        string firm_name
        string address
        string state
        string principal_broker
        string individual_license FK
    }

    INDIVIDUAL_LICENSES {
        string license_number PK
        string name
        string address
        string state
        string license_type
    }

    CONNECTIONS {
        string connection_id PK
        string firm_license FK
        string license_number FK
        string connection_type
        boolean verified
    }

    RESEARCH_OUTPUTS {
        string research_id PK
        string file_path
        string category
        string firm_license FK
        string license_number FK
    }

    VIOLATIONS {
        string violation_id PK
        string violation_type
        string firm_license FK
        string license_number FK
        string severity
    }

    EVIDENCE {
        string evidence_id PK
        string file_path
        string evidence_type
        string violation_id FK
    }
```

> 📘 See [data/schema.json](../data/schema.json) for complete schema definition and [data/DATA_DICTIONARY.md](../data/DATA_DICTIONARY.md) for field definitions.
