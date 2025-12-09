# Repository Diagrams

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
    
    style ROOT fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    style DATA fill:#e8f5e9,stroke:#388e3c
    style RESEARCH fill:#f3e5f5,stroke:#7b1fa2
    style SCRIPTS fill:#fff3e0,stroke:#f57c00
    style BIN fill:#e1f5fe,stroke:#0277bd
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
    
    style START fill:#c8e6c9
    style SOURCE fill:#e8f5e9
    style CLEANED fill:#fff3e0
    style OUTPUT fill:#f3e5f5
    style END fill:#c8e6c9
```

## Component Relationships

```mermaid
graph LR
    subgraph "Entry Layer"
        A[bin/run_pipeline.py]
        B[bin/run_all.py]
        C[bin/analyze_connections.py]
        D[bin/validate_data.py]
    end
    
    subgraph "Core Modules"
        E[UnifiedAnalyzer]
        F[UnifiedSearcher]
        G[UnifiedValidator]
        H[UnifiedReporter]
        I[UnifiedInvestigator]
        J[UnifiedScraper]
    end
    
    subgraph "Data Sources"
        K[data/source/]
        L[data/cleaned/]
        M[data/scraped/]
    end
    
    subgraph "Research Outputs"
        N[research/connections/]
        O[research/summaries/]
        P[research/verification/]
        Q[research/violations/]
    end
    
    A --> E
    B --> E
    C --> E
    D --> G
    
    E --> F
    E --> G
    E --> H
    E --> I
    E --> J
    
    K --> E
    L --> E
    M --> J
    
    E --> N
    E --> O
    G --> P
    I --> Q
    
    style A fill:#e1f5ff
    style E fill:#fff4e1
    style K fill:#e8f5e9
    style N fill:#f3e5f5
```

## File Type Distribution

```mermaid
pie title File Types in Repository
    "Python Scripts" : 45
    "JSON Data" : 25
    "Markdown Docs" : 15
    "CSV Data" : 10
    "Other" : 5
```

## Research Output Categories

```mermaid
mindmap
  root((Research Outputs))
    Connections
      dpor_skidmore_connections.csv
      connection_matrix.json
      nexus_patterns_analysis.json
    Violations
      all_violations_compiled.json
      hyland_upl_investigation.json
      news_violations_search.json
    Anomalies
      all_anomalies_consolidated.json
      fraud_indicators.json
      additional_anomalies.json
    Summaries
      analysis_summary.json
      data_quality_report.json
      filing_recommendations.json
    Verification
      dpor_validated.csv
      kettler_verification.json
      hyland_verification.json
    Timelines
      timeline_analysis.json
      lease_abnormalities_detailed.json
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
    ETL --> VECTORS
    CORE --> RESEARCH
    ANALYSIS --> RESEARCH
    
    style WEB fill:#e3f2fd
    style CORE fill:#fff3e0
    style SOURCE fill:#e8f5e9
    style RESEARCH fill:#f3e5f5
```

## Usage

These diagrams are rendered automatically in:
- GitHub (native Mermaid support)
- GitLab (native Mermaid support)
- VS Code (with Mermaid extension)
- Most modern markdown viewers

To view locally, use a markdown viewer that supports Mermaid.js or visit the repository on GitHub/GitLab.
