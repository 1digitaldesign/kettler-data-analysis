# System Architecture

![Architecture](https://img.shields.io/badge/architecture-unified-blue)
![Status](https://img.shields.io/badge/status-operational-brightgreen)

Complete system architecture documentation including components, data flow, repository structure, and visual diagrams.

## Overview

Multi-state property management licensing investigation platform with Python-first architecture, unified core modules, and comprehensive data governance.

| Aspect | Description |
|--------|-------------|
| **Type** | Python-first microservices architecture |
| **Pattern** | Unified modules + microservices + API + Web frontend |
| **Language** | Python 3.14+ (primary), R (deprecated) |
| **Data Flow** | Source → Extract → Clean → Analyze → Research Outputs |

---

## Architecture diagram

```mermaid
graph TB
    subgraph "Entry Layer"
        E1[run_pipeline.py]
        E2[run_all.py]
        E3[analyze_connections.py]
        E4[validate_data.py]
    end

    subgraph "Core Layer"
        C1[UnifiedAnalyzer]
        C2[UnifiedSearcher]
        C3[UnifiedValidator]
        C4[UnifiedReporter]
        C5[UnifiedInvestigator]
    end

    subgraph "Data Layer"
        D1[Source Data]
        D2[Cleaned Data]
        D3[Research Outputs]
    end

    E1 --> C1
    E2 --> C1
    E3 --> C1
    E4 --> C3
    C1 --> D1
    C1 --> D2
    C1 --> D3

    style E1 fill:#B3E5FC
    style C1 fill:#FFF9C4
    style D1 fill:#C8E6C9
```

---

## Component hierarchy

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

---

## Data flow pipeline

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

### Processing steps

1. **Source Data** (`data/source/`)
   - Authoritative data from Virginia DPOR and multi-state searches
   - 38 firms, 40+ individual licenses

2. **Extraction** (`scripts/extraction/`)
   - PDF text extraction
   - Excel data extraction
   - Entity extraction

3. **Raw Data** (`data/raw/`)
   - Unprocessed search results
   - Temporary storage

4. **Cleaning** (`bin/clean_data.py`)
   - Name standardization
   - Address normalization
   - Date parsing
   - Deduplication

5. **Cleaned Data** (`data/cleaned/`)
   - Validated, normalized data
   - Ready for analysis

6. **Analysis** (`scripts/core/`)
   - Connection analysis
   - Violation detection
   - Anomaly identification

7. **Research Outputs** (`research/`)
   - Connections, violations, anomalies
   - Evidence summaries
   - Complaint packages

---

## Repository structure

```mermaid
graph TB
    ROOT[Repository Root] --> BIN[bin/<br/>Entry Points]
    ROOT --> SCRIPTS[scripts/<br/>Library]
    ROOT --> DATA[data/<br/>Data]
    ROOT --> RESEARCH[research/<br/>Research]
    ROOT --> DOCS[docs/<br/>Documentation]

    SCRIPTS --> CORE[core/<br/>Unified Modules]
    SCRIPTS --> UTILS[utils/<br/>Utilities]

    DATA --> SOURCE[source/<br/>Authoritative]
    DATA --> CLEANED[cleaned/<br/>Processed]

    RESEARCH --> CONNECTIONS[connections/]
    RESEARCH --> VIOLATIONS[violations/]
    RESEARCH --> REPORTS[reports/]

    style ROOT fill:#D1C4E9
    style DATA fill:#C8E6C9
    style RESEARCH fill:#E1BEE7
    style SCRIPTS fill:#B2DFDB
```

### Directory organization

**Entry Points** (`bin/`)
- `run_pipeline.py` - Full pipeline execution
- `run_all.py` - All analyses
- `analyze_connections.py` - Connection analysis
- `validate_data.py` - Data validation
- `generate_reports.py` - Report generation
- `organize_evidence.py` - Evidence organization
- `clean_data.py` - Data cleaning

**Scripts** (`scripts/`)
- `core/` - Unified modules (Analyzer, Searcher, Validator, Reporter, Investigator)
- `utils/` - Utility functions (paths, validation, metadata)
- `etl/` - ETL pipeline for vector embeddings

**Data** (`data/`)
- `source/` - Authoritative source data
- `cleaned/` - Cleaned and validated data
- `vectors/` - Vector embeddings
- Schema and metadata files

**Research** (`research/`)
- `connections/` - Connection analyses
- `violations/` - Violation findings
- `reports/` - Summary reports
- `va_dpor_complaint/` - Complaint package
- `license_searches/` - Multi-state search results

**Documentation** (`docs/`)
- System documentation
- Architecture guides
- Documentation index

---

## Key components

<details>
<summary><b>UnifiedAnalyzer</b> (`scripts/core/unified_analysis.py`)</summary>

**Purpose:** Unified analysis module consolidating multiple analysis scripts.

**Features:**
- Fraud pattern analysis
- Nexus pattern analysis
- Timeline analysis
- Anomaly consolidation
- Evidence analysis
- Connection matrix creation
- Shared resources analysis

**Input:** Source and cleaned data  
**Output:** Analysis results in `research/`

</details>

<details>
<summary><b>UnifiedInvestigator</b> (`scripts/core/unified_investigation.py`)</summary>

**Purpose:** Unified investigation module for regulatory compliance investigations.

**Features:**
- UPL investigation
- STR regulations research
- Zoning compliance checks
- Management chain audits

**Input:** Research data and evidence  
**Output:** Investigation results

</details>

<details>
<summary><b>SchemaValidator</b> (`scripts/utils/validate_schema.py`)</summary>

**Purpose:** Validates data against JSON Schema definitions.

**Features:**
- JSON Schema validation (Draft-07)
- FK/PK integrity checks
- Field validation
- Quality reporting

**Input:** Data files  
**Output:** Validation reports

</details>

---

## Entry points

| Script | Purpose | Output |
|--------|---------|--------|
| `bin/run_pipeline.py` | Full pipeline | All outputs |
| `bin/run_all.py` | All analyses | Research outputs |
| `bin/analyze_connections.py` | Connections | `research/connections/` |
| `bin/validate_data.py` | Validation | `research/verification/` |
| `bin/generate_reports.py` | Reports | `research/reports/` |

---

## Data organization

### Data structure

All data follows normalized schema with **Primary Keys (PK)** and **Foreign Keys (FK)**:

```
FIRMS {
    string firm_license PK
    string firm_name
    string principal_broker
    string individual_license FK
}

INDIVIDUAL_LICENSES {
    string license_number PK
    string name
    string state
}

CONNECTIONS {
    string connection_id PK
    string firm_license FK
    string license_number FK
    string connection_type
}
```

> 📘 See [data/schema.json](../data/schema.json) for complete schema definition and [data/DATA_DICTIONARY.md](../data/DATA_DICTIONARY.md) for field definitions.

### Data governance

The repository follows industry best practices for data governance:

- **[Data Catalog](../data/DATA_CATALOG.md)** - Comprehensive catalog of all data assets
- **[Data Governance](../data/GOVERNANCE.md)** - Governance framework including policies, roles, compliance
- **Data Classification** - Public, Internal, Confidential, Restricted levels
- **Quality Management** - Quality metrics, monitoring, and improvement processes

---

## System diagrams

### Component relationships

```mermaid
graph LR
    A[UnifiedAnalyzer] --> B[UnifiedSearcher]
    A --> C[UnifiedValidator]
    A --> D[UnifiedReporter]
    A --> E[UnifiedInvestigator]

    B --> F[Data Sources]
    C --> G[Schema Validation]
    D --> H[Report Generation]
    E --> I[Investigation]

    style A fill:#FFF9C4
    style B fill:#B3E5FC
    style C fill:#C8E6C9
```

### Data transformation pipeline

```mermaid
flowchart TD
    S[Source Data] --> E[Extract]
    E --> T[Transform]
    T --> L[Load]
    L --> A[Analyze]
    A --> R[Research Outputs]

    style S fill:#C8E6C9
    style T fill:#FFF9C4
    style R fill:#E1BEE7
```

---

## Documentation connections

This document connects to:
- 📋 [Data Dictionary](../data/DATA_DICTIONARY.md) - Field definitions
- 📊 [Schema](../data/schema.json) - Complete schema
- 📚 [Data Catalog](../data/DATA_CATALOG.md) - Data asset catalog and discoverability
- 🛡️ [Data Governance](../data/GOVERNANCE.md) - Governance framework and policies
- 🔄 [Documentation Index](INDEX.md) - Complete documentation index
- 📁 [Repository Structure](REPOSITORY_STRUCTURE.md) - File organization
- 📑 [Documentation Graph](DOCUMENTATION_GRAPH.md) - Complete documentation network

---

**Last Updated:** 2025-12-10  
**Architecture Version:** 1.0.0
