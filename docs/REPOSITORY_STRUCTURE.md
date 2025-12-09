# Repository Structure

## Top-Level Organization

```
.
├── bin/              # Entry points
├── scripts/          # Library code
│   ├── core/         # Unified modules
│   ├── analysis/     # Analysis
│   ├── extraction/   # Evidence extraction
│   ├── etl/          # ETL pipeline
│   ├── microservices/# Microservice code
│   └── utils/        # Utilities
├── api/              # FastAPI server
├── web/              # React frontend
├── microservices/    # Microservice implementations
├── data/             # Data directories
│   ├── source/       # Source data
│   ├── raw/          # Raw results
│   ├── cleaned/      # Cleaned data
│   ├── analysis/     # Analysis outputs
│   └── vectors/      # Vector embeddings
├── research/         # Research outputs
│   ├── connections/  # Connection analyses
│   ├── violations/   # Violation findings
│   ├── anomalies/    # Anomaly reports
│   ├── evidence/     # Evidence summaries
│   └── verification/ # Verification results
├── config/           # Configuration
├── docs/             # Documentation
├── evidence/         # Source documents
├── filings/          # Filing materials
├── tests/            # Tests
├── docker/           # Docker configs
└── kubernetes/       # Kubernetes configs
```

## Component Organization

**Entry Layer:** `bin/` - Scripts to run
**Core Layer:** `scripts/core/` - Unified modules
**Analysis:** `scripts/analysis/` - Analysis scripts
**Extraction:** `scripts/extraction/` - Evidence extraction
**ETL:** `scripts/etl/` - ETL pipeline
**API:** `api/` - FastAPI server
**Web:** `web/` - React frontend
**Microservices:** `microservices/` - Service implementations

## Data Organization

**Source:** `data/source/` - Authoritative data
**Raw:** `data/raw/` - Unprocessed results
**Cleaned:** `data/cleaned/` - Standardized data
**Research:** `research/` - All research outputs (connections, summaries, verification, etc.)
**Research:** `research/{category}/` - Categorized outputs

## Documentation

**System:** `SYSTEM_ARCHITECTURE.md`, `DATA_FLOW.md`, `COMPONENTS.md`
**Guides:** `docs/guides/`
**Reference:** `docs/reference/`
**Archive:** `docs/archive/`
