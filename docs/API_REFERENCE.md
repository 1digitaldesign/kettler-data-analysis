# API Reference

## API Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Frontend]
        CLI[CLI Tools]
    end

    subgraph "API Gateway"
        API[FastAPI Server<br/>localhost:8000]
    end

    subgraph "Endpoints"
        E1[Analysis Endpoints]
        E2[Search Endpoints]
        E3[Data Endpoints]
        E4[Validation Endpoints]
    end

    subgraph "Core Services"
        C1[UnifiedAnalyzer]
        C2[UnifiedSearcher]
        C3[UnifiedValidator]
    end

    WEB --> API
    CLI --> API
    API --> E1
    API --> E2
    API --> E3
    API --> E4
    E1 --> C1
    E2 --> C2
    E3 --> C1
    E4 --> C3

    style WEB fill:#F8BBD0
    style API fill:#B3E5FC
    style E1 fill:#FFF9C4
    style E2 fill:#FFF9C4
    style E3 fill:#FFF9C4
    style E4 fill:#FFF9C4
    style C1 fill:#C8E6C9
    style C2 fill:#C8E6C9
    style C3 fill:#C8E6C9
```

## Endpoints

**Base URL:** `http://localhost:8000`

### Analysis Endpoints

```mermaid
flowchart LR
    A[POST /api/analyze/connections] --> B[Analyze Connections]
    C[POST /api/analyze/anomalies] --> D[Detect Anomalies]
    E[GET /api/analysis/results] --> F[Get Results]

    B --> G[research/connections/]
    D --> H[research/anomalies/]
    F --> I[research/summaries/]

    style A fill:#FFF9C4
    style C fill:#FFF9C4
    style E fill:#FFF9C4
    style G fill:#E1BEE7
    style H fill:#E1BEE7
    style I fill:#E1BEE7
```

- `POST /api/analyze/connections` - Analyze connections
- `POST /api/analyze/anomalies` - Detect anomalies
- `GET /api/analysis/results` - Get analysis results

### Search Endpoints

```mermaid
flowchart LR
    A[POST /api/search/vector] --> B[Vector Search]
    C[POST /api/search/query] --> D[Query Search]

    B --> E[data/vectors/]
    D --> F[research/search_results/]

    style A fill:#B3E5FC
    style C fill:#B3E5FC
    style E fill:#C8E6C9
    style F fill:#E1BEE7
```

- `POST /api/search/vector` - Vector search
- `POST /api/search/query` - Query search

### Data Endpoints

```mermaid
flowchart LR
    A[GET /api/data/firms] --> B[Get Firms]
    C[GET /api/data/connections] --> D[Get Connections]
    E[POST /api/data/validate] --> F[Validate Data]

    B --> G[data/source/]
    D --> H[research/connections/]
    F --> I[research/verification/]

    style A fill:#C8E6C9
    style C fill:#C8E6C9
    style E fill:#C8E6C9
    style G fill:#C5E1A5
    style H fill:#E1BEE7
    style I fill:#E1BEE7
```

- `GET /api/data/firms` - Get firms
- `GET /api/data/connections` - Get connections
- `POST /api/data/validate` - Validate data

## API Documentation

**Interactive Docs:** `http://localhost:8000/docs`

Swagger UI provides interactive API documentation with:
- Endpoint descriptions
- Request/response schemas
- Try-it-out functionality
- Authentication options
