# System Components

## Component Hierarchy

```mermaid
graph TB
    subgraph "Entry Points"
        E1[run_pipeline.py]
        E2[run_all.py]
        E3[analyze_connections.py]
        E4[validate_data.py]
        E5[generate_reports.py]
        E6[organize_evidence.py]
        E7[clean_data.py]
    end

    subgraph "Core Modules"
        C1[UnifiedAnalyzer]
        C2[UnifiedSearcher]
        C3[UnifiedValidator]
        C4[UnifiedReporter]
        C5[UnifiedInvestigator]
        C6[UnifiedScraper]
    end

    subgraph "Supporting Scripts"
        S1[Analysis Scripts]
        S2[Extraction Scripts]
        S3[ETL Pipeline]
    end

    E1 --> C1
    E2 --> C1
    E3 --> C1
    E4 --> C3
    E5 --> C4
    E6 --> C5
    E7 --> C1

    C1 --> S1
    C2 --> S2
    C1 --> S3

    style E1 fill:#B3E5FC
    style C1 fill:#FFF9C4
    style S1 fill:#C8E6C9
```

## Entry Points (`bin/`)

- `run_pipeline.py` - Full pipeline
- `run_all.py` - All analyses
- `analyze_connections.py` - Connections
- `validate_data.py` - Validation
- `generate_reports.py` - Reports
- `organize_evidence.py` - Evidence
- `clean_data.py` - Data cleaning

## Core Modules (`scripts/core/`)

```mermaid
graph LR
    A[UnifiedAnalyzer] --> B[Analysis Operations]
    C[UnifiedSearcher] --> D[Search Operations]
    E[UnifiedValidator] --> F[Validation]
    G[UnifiedReporter] --> H[Report Generation]
    I[UnifiedInvestigator] --> J[Investigation]
    K[UnifiedScraper] --> L[Web Scraping]

    B --> M[research/connections/]
    B --> N[research/anomalies/]
    D --> O[research/search_results/]
    F --> P[research/verification/]
    H --> Q[research/summaries/]
    J --> R[research/violations/]

    style A fill:#FFF9C4
    style C fill:#B3E5FC
    style E fill:#C8E6C9
    style G fill:#E1BEE7
    style I fill:#F8BBD0
    style K fill:#FFE0B2
```

- `unified_analysis.py` - UnifiedAnalyzer
- `unified_search.py` - UnifiedSearcher
- `unified_validation.py` - UnifiedValidator
- `unified_reporting.py` - UnifiedReporter
- `unified_investigation.py` - UnifiedInvestigator
- `unified_scraping.py` - UnifiedScraper

## Analysis (`scripts/analysis/`)

- `analyze_fraud_patterns.py` - Fraud detection
- `analyze_str_listings.py` - STR analysis

## Extraction (`scripts/extraction/`)

- `extract_pdf_evidence.py` - PDF extraction
- `extract_excel_evidence.py` - Excel extraction
- `extract_all_evidence.py` - Master extraction

## ETL (`scripts/etl/`)

- `etl_pipeline.py` - Main pipeline
- `vector_embeddings.py` - Vector generation
- `vector_api_server.py` - Vector API

## API (`api/`)

- `server.py` - FastAPI server
- Endpoints for all operations

## Web (`web/`)

- React/TypeScript frontend
- Components for analysis, search, visualization

## Microservices (`microservices/`)

- `api-gateway/` - Request routing
- `analysis-service/` - Analysis processing
- `vector-service/` - Vector operations
- `validation-service/` - Validation
- `scraping-service/` - Web scraping
- `gis-service/` - GIS operations
- `acris-service/` - ACRIS operations
- `data-service/` - Data operations

## Data (`data/`)

- `source/` - Source data
- `raw/` - Raw results
- `cleaned/` - Cleaned data
- `analysis/` - Analysis outputs
- `vectors/` - Vector embeddings

## Research (`research/`)

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
    Evidence
      pdf_evidence_extracted.json
      excel_evidence_extracted.json
    Search Results
      dpor_search_results.json
      virginia_bar_search_results.json
```

- `connections/` - Connection analyses
- `violations/` - Violation findings
- `anomalies/` - Anomaly reports
- `evidence/` - Evidence summaries
- `verification/` - Verification results
- `timelines/` - Timeline analyses

## Configuration (`config/`)

- `state_dpor_registry.csv` - State registry
- `templates/` - Config templates
