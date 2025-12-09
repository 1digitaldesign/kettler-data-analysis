# Repository Organization Guide

**Last Updated:** December 9, 2025

## Overview

This repository has been reorganized for improved clarity, maintainability, and ease of use. All scripts, data, and research outputs are now organized into logical directories with clear purposes.

## Directory Structure

### `/bin` - Entry Point Scripts

Executable scripts that serve as main entry points for common workflows:

- `run_pipeline.R` - Complete pipeline execution
- `search_states.R` - Multi-state license search
- `analyze_connections.R` - Connection analysis
- `validate_data.R` - Data quality validation
- `generate_reports.R` - Report generation
- `organize_evidence.R` - Evidence organization
- `clean_data.py` - Data cleaning (Python)

**Usage:** Run these scripts directly from the project root:
```bash
Rscript bin/run_pipeline.R
python bin/clean_data.py
```

### `/scripts` - Library Scripts

Organized by function:

- **`search/`** - Search and scraping scripts
- **`analysis/`** - Analysis and pattern detection
- **`extraction/`** - Evidence extraction from PDFs/Excel
- **`validation/`** - Data validation scripts
- **`reporting/`** - Report generation
- **`etl/`** - ETL and vectorization
- **`microservices/`** - Microservice implementations
- **`utils/`** - Utility functions (including `paths.R`)

### `/data` - Data Directories

- **`source/`** - Original source data files
- **`raw/`** - Raw search results (gitignored)
- **`cleaned/`** - Cleaned and standardized data (gitignored)
- **`analysis/`** - Analysis outputs (gitignored)
- **`scraped/`** - Scraped web data
- **`vectors/`** - Vector embeddings and metadata

### `/research` - Research Outputs

Organized by category:

- **`connections/`** - Connection analyses (Skidmore, Hyland, etc.)
- **`violations/`** - Violation findings and UPL evidence
- **`anomalies/`** - Anomaly reports and fraud indicators
- **`evidence/`** - Evidence summaries and extracted data
- **`verification/`** - License verification results
- **`timelines/`** - Timeline analyses
- **`summaries/`** - Summary reports and findings
- **`search_results/`** - Raw search result files

### `/config` - Configuration Files

- `state_dpor_registry.csv` - State registry mapping
- `templates/` - Configuration templates

### `/docs` - Documentation

- `guides/` - User guides
- `reference/` - Reference materials
- `architecture/` - Architecture documentation

## Path Management

All scripts use centralized path management via `scripts/utils/paths.R`:

```r
# Load paths utility
source("scripts/utils/paths.R")

# Use predefined paths
firms_file <- file.path(DATA_SOURCE_DIR, "skidmore_all_firms_complete.csv")
research_file <- file.path(RESEARCH_CONNECTIONS_DIR, "caitlin_skidmore_connections.json")
```

## Migration Notes

### Updated File Locations

**Scripts moved:**
- `run_full_pipeline.R` → `bin/run_pipeline.R`
- `search_multi_state_dpor.R` → `bin/search_states.R`
- `analyze_skidmore_connections.R` → `bin/analyze_connections.R`
- `validate_data_quality.R` → `bin/validate_data.R`
- `generate_outputs.R` → `bin/generate_reports.R`
- `organize_evidence.R` → `bin/organize_evidence.R`
- `clean_dpor_data.py` → `bin/clean_data.py`
- `search_dpor_comprehensive.R` → `scripts/search/`
- `search_virginia_dpor.R` → `scripts/search/`

**Config moved:**
- `state_dpor_registry.csv` → `config/state_dpor_registry.csv`

**Research files organized:**
- Connection analyses → `research/connections/`
- Violation findings → `research/violations/`
- Anomaly reports → `research/anomalies/`
- Evidence summaries → `research/evidence/`
- Verification results → `research/verification/`
- Timeline analyses → `research/timelines/`
- Summary reports → `research/summaries/`
- Search results → `research/search_results/`

## Updating Scripts

When updating scripts that reference files:

1. **Use path utilities:**
   ```r
   source("scripts/utils/paths.R")
   file_path <- file.path(RESEARCH_CONNECTIONS_DIR, "file.json")
   ```

2. **Update source() calls:**
   ```r
   # Old
   source("search_dpor_comprehensive.R")
   
   # New
   source_script("search/search_dpor_comprehensive.R")
   ```

3. **Update file paths:**
   ```r
   # Old
   file.path("research", "caitlin_skidmore_connections.json")
   
   # New
   file.path(RESEARCH_CONNECTIONS_DIR, "caitlin_skidmore_connections.json")
   ```

## Benefits

1. **Clear separation** between entry points (`bin/`) and library code (`scripts/`)
2. **Organized research** outputs by category for easy navigation
3. **Centralized paths** reduce path-related bugs
4. **Better discoverability** of scripts and data
5. **Easier maintenance** with logical grouping

## Quick Reference

**Run main pipeline:**
```bash
Rscript bin/run_pipeline.R
```

**Search states:**
```bash
Rscript bin/search_states.R
```

**Analyze connections:**
```bash
Rscript bin/analyze_connections.R
```

**Clean data:**
```bash
python bin/clean_data.py
```

**Find connection analyses:**
```bash
ls research/connections/
```

**Find violation evidence:**
```bash
ls research/violations/
```
