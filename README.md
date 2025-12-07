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
├── data/
│   ├── raw/              # Raw search results from DPOR websites
│   ├── cleaned/          # Cleaned and standardized data
│   └── analysis/         # Analysis outputs and reports
├── state_scrapers/       # State-specific search implementations
├── search_dpor_comprehensive.R    # Core search framework
├── search_virginia_dpor.R        # Virginia-specific implementation
├── search_multi_state_dpor.R     # Multi-state wrapper
├── clean_dpor_data.py            # Data cleaning (Python/Hugging Face)
├── analyze_skidmore_connections.R # Connection analysis
├── validate_data_quality.R        # Data quality validation
├── generate_outputs.R            # Output generation
├── dpor_analysis_report.Rmd      # Analysis report template
├── state_dpor_registry.csv       # State registry mapping
└── requirements.txt               # Python dependencies
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
source("search_multi_state_dpor.R")
main_multi_state()
```

This will:
- Search all 10 specified firms across all 50 states
- Search for Caitlin Skidmore across all states
- Save results to `data/raw/`

### 2. Clean Data

```bash
python clean_dpor_data.py
```

This will:
- Standardize firm names using Hugging Face NER
- Normalize addresses
- Parse and standardize dates
- Deduplicate results
- Save cleaned data to `data/cleaned/`

### 3. Analyze Connections

```r
source("analyze_skidmore_connections.R")
main_analysis()
```

This will:
- Identify connections between firms and Caitlin Skidmore
- Generate network analysis
- Save connections to `data/analysis/dpor_skidmore_connections.csv`

### 4. Validate Data Quality

```r
source("validate_data_quality.R")
main_validation()
```

This will:
- Validate license numbers
- Flag duplicates
- Validate addresses and dates
- Generate quality report

### 5. Generate All Outputs

```r
source("generate_outputs.R")
main_outputs()
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

The `state_dpor_registry.csv` file contains:
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
