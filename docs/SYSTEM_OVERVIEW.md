# System Overview

## Purpose

Multi-state property management licensing investigation platform.

## Architecture Layers

```mermaid
graph TB
    subgraph "Layer 1: Entry"
        L1[bin/ Scripts]
    end

    subgraph "Layer 2: Core"
        L2[scripts/core/<br/>Unified Modules]
    end

    subgraph "Layer 3: Analysis"
        L3[scripts/analysis/]
    end

    subgraph "Layer 4: ETL"
        L4[scripts/etl/<br/>Vector Embeddings]
    end

    subgraph "Layer 5: API"
        L5[api/<br/>FastAPI Server]
    end

    subgraph "Layer 6: Web"
        L6[web/<br/>React Frontend]
    end

    subgraph "Layer 7: Microservices"
        L7[microservices/]
    end

    subgraph "Layer 8: Data"
        L8[data/<br/>research/]
    end

    L1 --> L2
    L2 --> L3
    L2 --> L4
    L5 --> L2
    L6 --> L5
    L5 --> L7
    L2 --> L8
    L3 --> L8
    L4 --> L8

    style L1 fill:#B3E5FC
    style L2 fill:#FFF9C4
    style L5 fill:#F8BBD0
    style L8 fill:#C8E6C9
```

1. **Entry Layer** - `bin/` scripts
2. **Core Layer** - `scripts/core/` unified modules
3. **Analysis Layer** - `scripts/analysis/`
4. **ETL Layer** - `scripts/etl/`
5. **API Layer** - `api/`
6. **Web Layer** - `web/`
7. **Microservices** - `microservices/`
8. **Data Layer** - `data/`, `research/`

## Key Components

**UnifiedAnalyzer** - Analysis operations
**UnifiedSearcher** - Search operations
**UnifiedValidator** - Validation
**ETL Pipeline** - Vector embeddings
**API Gateway** - Request routing
**Analysis Service** - Distributed processing

## Data Flow

```mermaid
flowchart LR
    A[Source] --> B[Extract]
    B --> C[Clean]
    C --> D[Analyze]
    D --> E[Research Outputs]

    A --> A1[data/source/]
    B --> B1[scripts/extraction/]
    C --> C1[data/cleaned/]
    D --> D1[scripts/core/]
    E --> E1[research/]

    style A fill:#C8E6C9
    style C fill:#FFF9C4
    style E fill:#E1BEE7
```

**Text Flow:**

Source → Extract → Clean → Analyze → Research Outputs

## Entry Points

- `bin/run_pipeline.py` - Full pipeline
- `bin/run_all.py` - All analyses
- `api/server.py` - API server
- `web/` - Web application
