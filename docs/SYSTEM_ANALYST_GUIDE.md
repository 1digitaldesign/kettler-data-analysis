# System Analyst Guide

## System Purpose

Multi-state property management licensing investigation platform. Analyzes connections, violations, and anomalies across 50 states.

## Architecture Overview

**Type:** Python-first microservices architecture
**Pattern:** Unified modules + microservices + API + Web frontend

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

    style E1 fill:#e1f5ff
    style C1 fill:#fff4e1
    style API1 fill:#e3f2fd
    style MS1 fill:#f3e5f5
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

    style A fill:#e8f5e9
    style E fill:#fff3e0
    style G fill:#f3e5f5
```

## Key Components

```mermaid
graph LR
    subgraph "UnifiedAnalyzer"
        UA1[Input: Source Data] --> UA2[Analysis Operations] --> UA3[Output: Results]
    end

    subgraph "UnifiedSearcher"
        US1[Input: Queries] --> US2[Search Operations] --> US3[Output: Results]
    end

    subgraph "ETL Pipeline"
        ETL1[Input: Documents] --> ETL2[Vector Embeddings] --> ETL3[Output: Vector Store]
    end

    subgraph "API Gateway"
        AG1[Input: HTTP Requests] --> AG2[Request Routing] --> AG3[Output: Responses]
    end

    style UA2 fill:#fff4e1
    style US2 fill:#e1f5ff
    style ETL2 fill:#e8f5e9
    style AG2 fill:#f3e5f5
```

**UnifiedAnalyzer** (`scripts/core/unified_analysis.py`)
- Purpose: Analysis operations
- Input: Source data, evidence
- Output: Analysis results

**UnifiedSearcher** (`scripts/core/unified_search.py`)
- Purpose: Search operations
- Input: Search queries
- Output: Search results

**ETL Pipeline** (`scripts/etl/etl_pipeline.py`)
- Purpose: Vector embeddings
- Input: Documents
- Output: Vector store

**API Gateway** (`microservices/api-gateway/`)
- Purpose: Request routing
- Input: HTTP requests
- Output: Service responses

## Entry Points

1. **Pipeline:** `bin/run_pipeline.py`
2. **All Analyses:** `bin/run_all.py`
3. **API:** `api/server.py`
4. **Web:** `web/` (npm run dev)

## Data Locations

**Source:** `data/source/`
**Raw:** `data/raw/` (gitignored)
**Cleaned:** `data/cleaned/` (gitignored)
**Research:** `research/`
**Research:** `research/{category}/`

## Configuration

**State Registry:** `config/state_dpor_registry.csv`
**Environment:** `.env`
**Docker:** `docker-compose.yml`
**Kubernetes:** `kubernetes/`

## Testing

**Unit Tests:** `tests/`
**Microservice Tests:** `microservices/tests/`
**Run:** `python -m pytest tests/`

## Deployment

**Local:** `python bin/run_pipeline.py`
**Docker:** `make up`
**Kubernetes:** `kubectl apply -f kubernetes/`

## Documentation

- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - Architecture details
- [DATA_FLOW.md](DATA_FLOW.md) - Data pipeline
- [COMPONENTS.md](COMPONENTS.md) - Component reference
- [API_REFERENCE.md](API_REFERENCE.md) - API endpoints
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
