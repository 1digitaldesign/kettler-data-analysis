# Kettler Data Analysis - DPOR Multi-State License Search

This project searches Department of Professional and Occupational Regulation (DPOR) websites across all 50 states to find license information for specified firms and identify connections with Caitlin Skidmore.

## Overview

The system performs automated searches across state licensing databases to:
1. Find license information for 10 specified property management firms
2. Search for Caitlin Skidmore across all states to find additional connections
3. Analyze connections through principal broker listings, address matching, and license patterns
4. Clean and validate data using Hugging Face transformers
5. Generate comprehensive analysis reports

## Project Structure

```
.
├── bin/                  # Entry point scripts (executables)
│   ├── run_pipeline.R          # Main pipeline runner
│   ├── search_states.R         # Multi-state search
│   ├── analyze_connections.R   # Connection analysis
│   ├── validate_data.R         # Data validation
│   ├── generate_reports.R      # Report generation
│   └── organize_evidence.R     # Evidence organization
│
├── scripts/             # Library scripts (organized by function)
│   ├── search/          # Search and scraping scripts
│   ├── analysis/        # Analysis scripts
│   ├── extraction/      # Evidence extraction
│   ├── validation/      # Data validation
│   ├── reporting/       # Report generation
│   ├── etl/            # ETL and vectorization
│   ├── microservices/  # Microservices
│   └── utils/          # Utility functions
│
├── data/                # Data directories
│   ├── source/         # Source data files
│   ├── raw/            # Raw search results
│   ├── cleaned/        # Cleaned data
│   ├── analysis/       # Analysis outputs
│   ├── scraped/        # Scraped data
│   └── vectors/        # Vector embeddings
│
├── research/            # Research outputs (organized by category)
│   ├── connections/     # Connection analyses
│   ├── violations/     # Violation findings
│   ├── anomalies/      # Anomaly reports
│   ├── evidence/       # Evidence summaries
│   ├── verification/   # Verification results
│   ├── timelines/      # Timeline analyses
│   ├── summaries/      # Summary reports
│   └── search_results/ # Search result files
│
├── evidence/            # Source evidence documents
├── filings/            # Filing materials
├── docs/               # Documentation
├── config/             # Configuration files
└── outputs/            # Generated outputs
```

## Installation

### R Dependencies

```r
install.packages(c("httr", "rvest", "dplyr", "jsonlite", "stringr", "data.table"))
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Search All States for Firms

```r
# Run multi-state search for all firms
source("bin/search_states.R")
main_multi_state()
```

This will:
- Search all 10 specified firms across all 50 states
- Search for Caitlin Skidmore across all states
- Save results to `data/raw/`

### 2. Clean Data

```bash
python bin/clean_data.py
```

This will:
- Standardize firm names using Hugging Face NER
- Normalize addresses
- Parse and standardize dates
- Deduplicate results
- Save cleaned data to `data/cleaned/`

### 3. Analyze Connections

```r
source("bin/analyze_connections.R")
main_analysis()
```

This will:
- Identify connections between firms and Caitlin Skidmore
- Generate network analysis
- Save connections to `data/analysis/dpor_skidmore_connections.csv`

### 4. Validate Data Quality

```r
source("bin/validate_data.R")
main_validation()
```

This will:
- Validate license numbers
- Flag duplicates
- Validate addresses and dates
- Generate quality report

### 5. Generate All Outputs

```r
source("bin/generate_reports.R")
main_outputs()
```

### Quick Start: Run Full Pipeline

```r
# Run the complete pipeline
source("bin/run_pipeline.R")
```

This runs all analysis and generates:
- Connection summaries
- State summaries
- Quality reports
- High-quality record sets

### 6. Generate Report

```r
rmarkdown::render("dpor_analysis_report.Rmd")
```

## Firms Searched

1. Bell Partners Inc
2. Bozzuto Management Company
3. Cortland Management LLC
4. Gables Residential Services Inc
5. Gateway Management Company LLC
6. McCormack Baron Management Inc
7. Burlington Capital Properties LLC
8. Bainbridge Mid Atlantic Management LLC
9. Capreit Residential Management LLC
10. Edgewood Management Corporation

## Output Files

### Analysis Outputs
- `data/analysis/dpor_skidmore_connections.csv` - All identified connections
- `data/analysis/dpor_validated.csv` - Validated data with quality flags
- `data/analysis/analysis_summary.json` - Summary statistics
- `data/analysis/data_quality_report.json` - Quality metrics

### Summary Files
- `dpor_multi_state_summary.csv` - Summary by state
- `dpor_connection_type_summary.csv` - Summary by connection type
- `dpor_high_quality_records.csv` - High-quality records only

## Connection Types Identified

1. **Principal Broker** - Firm lists Caitlin Skidmore as principal broker
2. **Same Address** - Firm shares address with Skidmore licenses
3. **Same Address as Known Firm** - Firm shares address with known Skidmore firms
4. **Known Firm Match** - Firm name matches known Skidmore firms

## Technical Details

### Search Framework
- **Language**: R (primary)
- **Libraries**: httr, rvest, dplyr, jsonlite, stringr
- **Approach**: Form-based and query-based searches
- **Rate Limiting**: 2-second delay between requests

### Data Cleaning
- **Language**: Python
- **Libraries**: Hugging Face transformers, pandas
- **Models**: BERT-based NER for entity extraction
- **Features**: Name standardization, address normalization, date parsing

### Analysis
- **Language**: R
- **Libraries**: dplyr, data.table
- **Methods**: Pattern matching, address clustering, duplicate detection

## State Registry

The `config/state_dpor_registry.csv` file contains:
- State codes and names
- Agency names
- License lookup URLs
- Search type (form-based vs query-based)
- Notes

## Documentation

- **[Documentation Index](docs/INDEX.md)** - Complete documentation index
- **[Filing Guide](docs/guides/FILING_GUIDE.md)** - Guide for filing administrative complaints
- **[Evidence Summary](docs/guides/EVIDENCE_SUMMARY.md)** - Summary of all evidence
- **[Maintenance Guide](docs/MAINTENANCE_GUIDE.md)** - Repository maintenance guide
- **[Project Organization](docs/guides/PROJECT_ORGANIZATION.md)** - Project structure guide

## Notes

- Some DPOR websites may require manual verification
- Rate limiting is implemented to respect server resources
- Search logs are saved to `dpor_search_log.txt`
- Intermediate results are saved frequently for recovery
- Evidence files are organized in `evidence/` subdirectories
- Generated outputs are in `outputs/` directory
- Documentation is organized in `docs/` directory

## License

This project is for research and analysis purposes.
