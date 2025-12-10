# System Architecture

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

## Components

```
┌─────────────────────────────────────────────────────────┐
│                    Entry Layer                           │
│  bin/run_pipeline.py, bin/run_all.py                    │
└────────────────────┬──────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼──────┐ ┌───▼──────┐
│   Core        │ │   API    │ │   Web    │
│   Modules     │ │  Server  │ │   App    │
│               │ │          │ │          │
│ unified_*     │ │ FastAPI  │ │ React    │
└───────┬───────┘ └────┬─────┘ └────┬─────┘
        │              │             │
        └──────────────┼─────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼──────┐ ┌─────▼──────┐
│   Analysis    │ │   ETL     │ │ Microservices│
│   Layer       │ │  Pipeline │ │             │
│               │ │           │ │             │
│ scripts/      │ │ vectors/  │ │ api-gateway │
│ analysis/     │ │           │ │ analysis-*  │
└───────┬───────┘ └─────┬─────┘ └─────┬──────┘
        │                │             │
        └────────────────┼────────────┘
                          │
                ┌─────────▼─────────┐
                │   Data Layer       │
                │                    │
                │ data/source/       │
                │ data/raw/          │
                │ data/cleaned/      │
                │ research/          │
                │ research/          │
                └────────────────────┘
```

## Layers

**Entry Layer** (`bin/`)
- Entry point scripts
- Pipeline orchestration

**Core Layer** (`scripts/core/`)
- UnifiedAnalyzer
- UnifiedSearcher
- UnifiedValidator
- UnifiedReporter

**Analysis Layer** (`scripts/analysis/`)
- Analysis scripts
- Pattern detection

**ETL Layer** (`scripts/etl/`)
- Vector embeddings
- Data transformation

**API Layer** (`api/`)
- FastAPI REST API
- Endpoints for all operations

**Web Layer** (`web/`)
- React frontend
- Interactive analysis

**Microservices** (`microservices/`)
- API Gateway
- Analysis Service
- Vector Service
- Validation Service

**Data Layer** (`data/`, `research/`)
- Source data
- Processed data
- Analysis outputs

## Data Flow

```
Source Data → Extraction → Cleaning → Analysis → Research Outputs
     ↓            ↓           ↓          ↓            ↓
  data/      scripts/    data/     scripts/    research/
  source/    extraction/ cleaned/  analysis/   {category}/
```

## Component Responsibilities

**UnifiedAnalyzer** - Analysis operations
**UnifiedSearcher** - Search operations
**UnifiedValidator** - Data validation
**UnifiedReporter** - Report generation
**ETL Pipeline** - Vector embeddings and transformation
**API Gateway** - Request routing
**Analysis Service** - Distributed analysis

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

See [data/schema.json](../data/schema.json) for complete schema definition and [data/DATA_DICTIONARY.md](../data/DATA_DICTIONARY.md) for field definitions.
