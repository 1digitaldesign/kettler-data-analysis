# Scripts Directory

This directory contains all analysis scripts organized by function.

## Directory Structure

```
scripts/
├── extraction/        # Evidence extraction scripts
├── search/           # Search and discovery scripts
├── analysis/         # Analysis scripts
└── legacy/          # Deprecated/legacy scripts
```

## Extraction Scripts (`extraction/`)

### `extract_pdf_evidence.R`
Extracts text, metadata, and entities from PDF files.

**Usage:**
```bash
cd scripts/extraction
Rscript extract_pdf_evidence.R
```

**Outputs:**
- `research/pdf_evidence_extracted.json`
- `research/pdf_evidence_summary.csv`

### `extract_excel_evidence.R`
Extracts data from Excel files (xlsx/xls).

**Usage:**
```bash
cd scripts/extraction
Rscript extract_excel_evidence.R
```

**Outputs:**
- `research/excel_evidence_extracted.json`
- `research/excel_evidence_summary.csv`

### `extract_all_evidence.R`
Master script to extract from all evidence sources.

**Usage:**
```bash
cd scripts/extraction
Rscript extract_all_evidence.R
```

## Search Scripts (`search/`)

### `search_regulatory_agencies.R`
Creates registry of federal, state, and local regulatory agencies.

**Usage:**
```bash
cd scripts/search
Rscript search_regulatory_agencies.R
```

**Outputs:**
- `research/regulatory_agencies_registry.json`
- `filings/federal/federal_agencies.csv`
- `filings/state/state_agencies.csv`
- `filings/local/local_agencies.csv`

## Analysis Scripts (`analysis/`)

### `analyze_fraud_patterns.R`
Identifies fraud indicators and generates filing recommendations.

**Usage:**
```bash
cd scripts/analysis
Rscript analyze_fraud_patterns.R
```

**Outputs:**
- `research/fraud_indicators.json`
- `research/filing_recommendations.json`
- `filings/filing_checklist.csv`

### `analyze_all_evidence.R`
Cross-references all evidence with license data.

**Usage:**
```bash
cd scripts/analysis
Rscript analyze_all_evidence.R
```

**Outputs:**
- `research/all_evidence_summary.json`
- `research/all_entities_extracted.json`

## Legacy Scripts (`legacy/`)

These scripts are deprecated but kept for reference:
- `search_dpor.R` - Initial search script (replaced by `search_dpor_comprehensive.R`)
- `test_virginia_search.R` - Test script (functionality moved to main scripts)

## Root-Level Scripts

These scripts are kept in the root directory for easy access:

- `organize_evidence.R` - Master organization script
- `analyze_skidmore_connections.R` - Connection analysis
- `clean_dpor_data.py` - Data cleaning (Python)
- `validate_data_quality.R` - Data quality validation
- `generate_outputs.R` - Output generation
- `run_full_pipeline.R` - Full pipeline runner
- `demo_analysis_pipeline.R` - Demo pipeline
- `search_dpor_comprehensive.R` - Comprehensive search framework
- `search_multi_state_dpor.R` - Multi-state wrapper
- `search_virginia_dpor.R` - Virginia-specific search

## Dependencies

### R Packages
- `httr`, `rvest` - Web scraping
- `dplyr`, `data.table` - Data manipulation
- `jsonlite` - JSON processing
- `stringr` - String manipulation
- `pdftools` - PDF extraction
- `readxl` - Excel reading

### Python Packages
- `pandas` - Data manipulation
- `transformers` - Hugging Face models
- `torch` - PyTorch (for transformers)

## Running Scripts

### Individual Scripts
```bash
# From script directory
cd scripts/extraction
Rscript extract_pdf_evidence.R

# From project root
Rscript scripts/extraction/extract_pdf_evidence.R
```

### Full Pipeline
```bash
# From project root
Rscript run_full_pipeline.R
```

### Master Organization
```bash
# From project root
Rscript organize_evidence.R
```
