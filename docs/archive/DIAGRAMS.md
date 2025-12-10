# Repository Diagrams

![Diagrams](https://img.shields.io/badge/diagrams-mermaid-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)

Visual representations of the repository structure, data flow, and system architecture.

## Repository Structure

```mermaid
graph TB
    subgraph "Repository Root"
        ROOT[kettler-data-analysis]
    end

    subgraph "Entry Points"
        ROOT --> BIN[bin/<br/>Python Entry Scripts]
    end

    subgraph "Code Library"
        ROOT --> SCRIPTS[scripts/]
        SCRIPTS --> CORE[core/<br/>Unified Modules]
        SCRIPTS --> ANALYSIS[analysis/<br/>Analysis Scripts]
        SCRIPTS --> EXTRACTION[extraction/<br/>Evidence Extraction]
        SCRIPTS --> ETL[etl/<br/>ETL Pipeline]
        SCRIPTS --> UTILS[utils/<br/>Path Utilities]
    end

    subgraph "Data Directories"
        ROOT --> DATA[data/]
        DATA --> SOURCE[source/<br/>Authoritative Data]
        DATA --> RAW[raw/<br/>Raw Search Results]
        DATA --> CLEANED[cleaned/<br/>Cleaned Data]
        DATA --> SCRAPED[scraped/<br/>Scraped Data]
        DATA --> VECTORS[vectors/<br/>Vector Embeddings]
    end

    subgraph "Research Outputs"
        ROOT --> RESEARCH[research/]
        RESEARCH --> CONNECTIONS[connections/<br/>Connection Analyses]
        RESEARCH --> VIOLATIONS[violations/<br/>Violation Findings]
        RESEARCH --> ANOMALIES[anomalies/<br/>Anomaly Reports]
        RESEARCH --> EVIDENCE[evidence/<br/>Evidence Summaries]
        RESEARCH --> VERIFICATION[verification/<br/>Verification Results]
        RESEARCH --> SUMMARIES[summaries/<br/>Summary Reports]
        RESEARCH --> TIMELINES[timelines/<br/>Timeline Analyses]
        RESEARCH --> SEARCH[search_results/<br/>Search Results]
    end

    subgraph "Services"
        ROOT --> API[api/<br/>FastAPI Server]
        ROOT --> WEB[web/<br/>React Frontend]
        ROOT --> MICRO[microservices/<br/>Microservice Impl]
    end

    style ROOT fill:#D1C4E9,stroke:#9575CD,stroke-width:3px
    style DATA fill:#C8E6C9,stroke:#81C784
    style RESEARCH fill:#E1BEE7,stroke:#BA68C8
    style SCRIPTS fill:#B2DFDB,stroke:#4DB6AC
    style BIN fill:#B3E5FC,stroke:#4FC3F7
```

## Data Flow Pipeline

```mermaid
flowchart TD
    START([Start Pipeline]) --> SOURCE[Load Source Data<br/>data/source/]

    SOURCE --> EXTRACT[Extract Evidence<br/>scripts/extraction/]
    EXTRACT --> RAW[Raw Data<br/>data/raw/]

    RAW --> CLEAN[Clean Data<br/>bin/clean_data.py]
    CLEAN --> CLEANED[Cleaned Data<br/>data/cleaned/]

    CLEANED --> ANALYZE[Analyze<br/>scripts/core/]

    ANALYZE --> CONN[Connections<br/>research/connections/]
    ANALYZE --> VALID[Validation<br/>research/verification/]
    ANALYZE --> SUMMARY[Summaries<br/>research/summaries/]
    ANALYZE --> VIOL[Violations<br/>research/violations/]
    ANALYZE --> ANOM[Anomalies<br/>research/anomalies/]
    ANALYZE --> TIME[Timelines<br/>research/timelines/]

    CONN --> OUTPUT[Research Outputs]
    VALID --> OUTPUT
    SUMMARY --> OUTPUT
    VIOL --> OUTPUT
    ANOM --> OUTPUT
    TIME --> OUTPUT

    OUTPUT --> END([Complete])

    style START fill:#C8E6C9
    style SOURCE fill:#C5E1A5
    style CLEANED fill:#FFF9C4
    style OUTPUT fill:#E1BEE7
    style END fill:#C8E6C9
```

## Component Relationships

```mermaid
graph LR
    A[Entry Points] --> B[Core Modules]
    B --> C[Analysis Scripts]
    B --> D[ETL Pipeline]
    C --> E[Research Outputs]
    D --> E

    style A fill:#B3E5FC
    style B fill:#FFF9C4
    style C fill:#C8E6C9
    style D fill:#E1BEE7
    style E fill:#F8BBD0
```

## System Architecture Layers

```mermaid
graph TB
    subgraph "Presentation Layer"
        WEB[Web Frontend<br/>React/TypeScript]
        API[API Server<br/>FastAPI]
    end

    subgraph "Application Layer"
        BIN[Entry Scripts<br/>bin/]
        CORE[Core Modules<br/>scripts/core/]
    end

    subgraph "Data Processing Layer"
        ETL[ETL Pipeline<br/>scripts/etl/]
        ANALYSIS[Analysis Scripts<br/>scripts/analysis/]
        EXTRACTION[Extraction<br/>scripts/extraction/]
    end

    subgraph "Data Layer"
        SOURCE[Source Data<br/>data/source/]
        PROCESSED[Processed Data<br/>data/cleaned/]
        VECTORS[Vector Store<br/>data/vectors/]
    end

    subgraph "Output Layer"
        RESEARCH[Research Outputs<br/>research/]
    end

    WEB --> API
    API --> BIN
    BIN --> CORE
    CORE --> ETL
    CORE --> ANALYSIS
    CORE --> EXTRACTION
    ETL --> SOURCE
    ANALYSIS --> PROCESSED
    EXTRACTION --> SOURCE
    PROCESSED --> VECTORS
    ANALYSIS --> RESEARCH
    ETL --> RESEARCH

    style WEB fill:#E1BEE7
    style API fill:#E1BEE7
    style BIN fill:#B3E5FC
    style CORE fill:#FFF9C4
    style ETL fill:#C8E6C9
    style ANALYSIS fill:#C8E6C9
    style EXTRACTION fill:#C8E6C9
    style SOURCE fill:#C5E1A5
    style PROCESSED fill:#FFF9C4
    style VECTORS fill:#D1C4E9
    style RESEARCH fill:#E1BEE7
```

## Entity-Relationship Diagram (FK/PK Relationships)

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
        string firm_license PK "10-digit license"
        string firm_name
        string address
        string state
        string principal_broker
        string individual_license FK "optional"
        date initial_cert_date
        date expiration_date
    }

    INDIVIDUAL_LICENSES {
        string license_number PK "10-digit license"
        string name
        string address
        string state
        string license_type
        date expiration_date
    }

    CONNECTIONS {
        string connection_id PK "auto-generated"
        string firm_license FK "optional"
        string license_number FK "optional"
        string connection_type
        string connection_detail
        string state
        boolean verified
    }

    RESEARCH_OUTPUTS {
        string research_id PK "auto-generated"
        string file_path
        string category
        string firm_license FK "optional"
        string license_number FK "optional"
        date analysis_date
        string status
    }

    VIOLATIONS {
        string violation_id PK "auto-generated"
        string violation_type
        string firm_license FK "optional"
        string license_number FK "optional"
        string severity
        string description
        array evidence_files
    }

    EVIDENCE {
        string evidence_id PK "auto-generated"
        string file_path
        string evidence_type
        string violation_id FK "optional"
        object extracted_data
        date extraction_date
    }
```

## Usage

<details>
<summary><b>Viewing Diagrams</b></summary>

These diagrams are rendered automatically in:
- ✅ GitHub (native Mermaid support)
- ✅ GitLab (native Mermaid support)
- ✅ VS Code (with Mermaid extension)
- ✅ Most modern markdown viewers

To view locally, use a markdown viewer that supports Mermaid.js or visit the repository on GitHub/GitLab.

</details>

## Related

- [System Architecture](../SYSTEM_ARCHITECTURE.md) - Complete architecture
- [Repository Structure](../REPOSITORY_STRUCTURE.md) - Structure details
