# Quick Start Guide

**Last Updated:** December 9, 2025

## Getting Started

### Prerequisites

1. **R** (version 4.0+)
2. **Python** (version 3.8+)
3. **Required R packages:**
   ```r
   install.packages(c("dplyr", "jsonlite", "stringr", "httr", "rvest", "data.table"))
   ```

4. **Required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Pipeline

**Option 1: Run complete pipeline**
```bash
Rscript bin/run_pipeline.R
```

**Option 2: Run individual steps**

1. **Search states:**
   ```bash
   Rscript bin/search_states.R
   ```

2. **Clean data:**
   ```bash
   python bin/clean_data.py
   ```

3. **Analyze connections:**
   ```bash
   Rscript bin/analyze_connections.R
   ```

4. **Validate data:**
   ```bash
   Rscript bin/validate_data.R
   ```

5. **Generate reports:**
   ```bash
   Rscript bin/generate_reports.R
   ```

6. **Organize evidence:**
   ```bash
   Rscript bin/organize_evidence.R
   ```

## Directory Structure Quick Reference

- **`bin/`** - Entry point scripts (run these)
- **`scripts/`** - Library scripts (used by bin scripts)
- **`data/`** - Data files
  - `source/` - Original source data
  - `raw/` - Raw search results
  - `cleaned/` - Cleaned data
  - `analysis/` - Analysis outputs
- **`research/`** - Research outputs
  - `connections/` - Connection analyses
  - `violations/` - Violation findings
  - `anomalies/` - Anomaly reports
  - `evidence/` - Evidence summaries
  - `verification/` - Verification results
- **`config/`** - Configuration files
- **`docs/`** - Documentation

## Common Tasks

### Find Connection Analyses
```bash
ls research/connections/
```

### Find Violation Evidence
```bash
ls research/violations/
```

### View Evidence Summaries
```bash
ls research/evidence/
```

### Check Verification Results
```bash
ls research/verification/
```

## Configuration

### State Registry
Located at: `config/state_dpor_registry.csv`

### Environment Variables
Copy `.env.example` to `.env` and configure:
- GCP credentials (for Google Drive API)
- Hugging Face tokens (for data cleaning)

## Documentation

- **[README.md](README.md)** - Main project documentation
- **[ORGANIZATION.md](docs/ORGANIZATION.md)** - Repository organization guide
- **[Filing Guide](docs/guides/FILING_GUIDE.md)** - Administrative filing guide
- **[Evidence Summary](docs/guides/EVIDENCE_SUMMARY.md)** - Evidence overview

## Troubleshooting

### Scripts Not Found
If you get "script not found" errors:
1. Ensure you're running from the project root directory
2. Check that `bin/` directory exists
3. Verify file permissions

### Path Errors
If you get path-related errors:
1. Check that `scripts/utils/paths.R` exists
2. Ensure you're running scripts from project root
3. Verify directory structure matches expected layout

### Missing Data Files
If data files aren't found:
1. Check `data/source/` for source files
2. Run search scripts to generate raw data
3. Run cleaning script to generate cleaned data
