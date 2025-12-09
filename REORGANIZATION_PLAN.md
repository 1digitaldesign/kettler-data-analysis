# Repository Reorganization Plan

## Goals
1. Improve code organization and readability
2. Create clear entry points for common workflows
3. Organize research outputs by category
4. Consolidate documentation
5. Standardize file paths and references

## Current Issues
- Root-level scripts that should be organized
- Research directory has 61+ files without categorization
- Documentation scattered across multiple locations
- Inconsistent path references
- No clear separation between entry points and library code

## Proposed Structure

```
kettler-data-analysis/
├── README.md                    # Main project overview
├── QUICK_START.md              # Quick start guide
├── requirements.txt            # Python dependencies
├── Makefile                    # Build automation
│
├── bin/                        # Entry point scripts (executables)
│   ├── run_pipeline.R         # Main pipeline runner
│   ├── search_states.R        # Multi-state search
│   ├── analyze_connections.R  # Connection analysis
│   ├── validate_data.R        # Data validation
│   └── generate_reports.R     # Report generation
│
├── scripts/                    # Library scripts (organized by function)
│   ├── search/                # Search scripts
│   ├── analysis/              # Analysis scripts
│   ├── extraction/            # Evidence extraction
│   ├── validation/            # Data validation
│   ├── reporting/             # Report generation
│   ├── etl/                   # ETL and vectorization
│   ├── microservices/         # Microservices
│   └── utils/                 # Utility functions
│
├── data/                       # Data directories
│   ├── source/                # Source data files
│   ├── raw/                   # Raw search results
│   ├── cleaned/               # Cleaned data
│   ├── analysis/              # Analysis outputs
│   ├── scraped/               # Scraped data
│   └── vectors/               # Vector embeddings
│
├── research/                   # Research outputs (organized)
│   ├── connections/           # Connection analyses
│   ├── violations/            # Violation findings
│   ├── anomalies/             # Anomaly reports
│   ├── evidence/              # Evidence summaries
│   ├── verification/          # Verification results
│   ├── timelines/             # Timeline analyses
│   └── summaries/             # Summary reports
│
├── evidence/                   # Source evidence documents
│   ├── pdfs/                 # PDF documents
│   ├── emails/               # Email correspondence
│   ├── legal/                # Legal documents
│   ├── excel/                # Excel files
│   └── scraped/              # Scraped web content
│
├── filings/                    # Filing materials
│   ├── federal/              # Federal filings
│   ├── state/                # State filings
│   └── local/                # Local filings
│
├── docs/                       # Documentation
│   ├── README.md             # Documentation index
│   ├── guides/               # User guides
│   ├── reference/            # Reference materials
│   └── architecture/         # Architecture docs
│
├── config/                     # Configuration files
│   └── templates/            # Configuration templates
│
├── docker/                     # Docker configurations
├── kubernetes/                 # Kubernetes configs
└── outputs/                    # Generated outputs
    ├── reports/              # Generated reports
    └── summaries/            # Summary files
```

## Migration Steps

### Phase 1: Create New Structure
1. Create `bin/` directory for entry points
2. Create `research/` subdirectories
3. Organize `docs/` structure

### Phase 2: Move Files
1. Move root-level scripts to `bin/`
2. Organize research files into subdirectories
3. Move configuration templates

### Phase 3: Update References
1. Update all `source()` calls
2. Update file paths in scripts
3. Update documentation references

### Phase 4: Refactor Code
1. Standardize path handling
2. Create shared utility functions
3. Improve code comments and documentation

### Phase 5: Update Documentation
1. Update README.md
2. Create comprehensive guides
3. Update all cross-references

## File Mapping

### Root Scripts → bin/
- `run_full_pipeline.R` → `bin/run_pipeline.R`
- `search_multi_state_dpor.R` → `bin/search_states.R`
- `analyze_skidmore_connections.R` → `bin/analyze_connections.R`
- `validate_data_quality.R` → `bin/validate_data.R`
- `generate_outputs.R` → `bin/generate_reports.R`
- `organize_evidence.R` → `bin/organize_evidence.R`
- `clean_dpor_data.py` → `bin/clean_data.py`

### Research Files → research/subdirs/
- Connection analyses → `research/connections/`
- Violation findings → `research/violations/`
- Anomaly reports → `research/anomalies/`
- Evidence summaries → `research/evidence/`
- Verification results → `research/verification/`
- Timeline analyses → `research/timelines/`
- Summary reports → `research/summaries/`

### Config Files
- `state_dpor_registry.csv` → `config/state_dpor_registry.csv`
- `config/gcp-env-template.txt` → `config/templates/gcp-env-template.txt`
