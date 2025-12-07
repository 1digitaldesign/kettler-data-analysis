# Repository Maintenance Guide

**Last Updated:** December 7, 2025

## Repository Structure

```
kettler-data-analysis/
├── data/                    # Data directories (gitignored contents)
│   ├── raw/                # Raw search results
│   ├── cleaned/            # Cleaned data
│   └── analysis/           # Analysis outputs
│
├── evidence/               # Source evidence documents
│   ├── emails/            # Email correspondence
│   ├── legal_documents/    # Legal notices and documents
│   ├── linkedin_profiles/ # LinkedIn profile pages
│   ├── airbnb/            # Airbnb-related documents
│   ├── accommodation_forms/ # Accommodation request forms
│   ├── correspondence/    # Other correspondence
│   ├── excel_files/       # Excel spreadsheets
│   └── pdfs/              # Original PDFs (backup)
│
├── filings/                # Administrative filing materials
│   ├── federal/           # Federal agency information
│   ├── state/             # State agency information
│   ├── local/             # Local agency information
│   ├── filing_checklist.csv
│   ├── filing_evidence_package.json
│   └── executive_summary.md
│
├── research/               # Research and analysis outputs
│   ├── pdf_evidence_extracted.json
│   ├── pdf_evidence_summary.csv
│   ├── excel_evidence_extracted.json
│   ├── excel_evidence_summary.csv
│   ├── all_evidence_summary.json
│   ├── all_entities_extracted.json
│   ├── fraud_indicators.json
│   ├── filing_recommendations.json
│   └── regulatory_agencies_registry.json
│
├── scripts/                # Analysis scripts
│   ├── extraction/        # Evidence extraction scripts
│   │   ├── extract_pdf_evidence.R
│   │   ├── extract_excel_evidence.R
│   │   └── extract_all_evidence.R
│   ├── search/            # Search and discovery scripts
│   │   └── search_regulatory_agencies.R
│   ├── analysis/          # Analysis scripts
│   │   ├── analyze_fraud_patterns.R
│   │   └── analyze_all_evidence.R
│   └── legacy/            # Deprecated/legacy scripts
│
├── docs/                   # Documentation
│   ├── guides/            # User guides
│   │   ├── FILING_GUIDE.md
│   │   ├── EVIDENCE_SUMMARY.md
│   │   ├── PROJECT_ORGANIZATION.md
│   │   └── README_FILINGS.md
│   ├── reference/         # Reference materials
│   │   └── kettler-filings-quick-reference.md
│   └── MAINTENANCE_GUIDE.md (this file)
│
├── outputs/                # Generated outputs
│   ├── reports/           # Generated reports
│   │   └── dpor_analysis_report.html
│   └── summaries/         # Summary CSV files
│       ├── dpor_multi_state_summary.csv
│       ├── dpor_connection_type_summary.csv
│       └── dpor_high_quality_records.csv
│
├── .gitignore             # Git ignore rules
├── README.md              # Main project README
├── organize_evidence.R     # Master organization script
├── requirements.txt       # Python dependencies
└── state_dpor_registry.csv # State registry
```

## Maintenance Tasks

### Daily/Weekly Tasks

1. **Update Evidence Files**
   ```bash
   # Add new evidence files to appropriate subdirectories
   # Run extraction scripts
   cd scripts/extraction
   Rscript extract_pdf_evidence.R
   Rscript extract_excel_evidence.R
   ```

2. **Update Analysis**
   ```bash
   # Run analysis scripts
   cd scripts/analysis
   Rscript analyze_all_evidence.R
   ```

3. **Regenerate Filing Package**
   ```bash
   # Update filing package with new evidence
   Rscript organize_evidence.R
   ```

### Monthly Tasks

1. **Review and Clean Output Files**
   - Archive old reports in `outputs/reports/`
   - Review summary files in `outputs/summaries/`
   - Remove duplicate or outdated files

2. **Update Documentation**
   - Review and update guides in `docs/guides/`
   - Update `README.md` if project structure changes
   - Update `MAINTENANCE_GUIDE.md` as needed

3. **Review Evidence Organization**
   - Ensure all evidence files are in correct subdirectories
   - Remove duplicates
   - Verify extraction scripts are working

### Quarterly Tasks

1. **Archive Old Data**
   - Move old data files to archive
   - Clean up `data/raw/` and `data/cleaned/` directories
   - Archive old research outputs

2. **Update Dependencies**
   - Review and update R packages
   - Review and update Python packages in `requirements.txt`
   - Test scripts with updated dependencies

3. **Code Review**
   - Review scripts in `scripts/` for improvements
   - Move deprecated scripts to `scripts/legacy/`
   - Update script documentation

## File Naming Conventions

### Scripts
- Use descriptive names: `extract_pdf_evidence.R`
- Use lowercase with underscores
- Group by function: `extraction/`, `analysis/`, `search/`

### Evidence Files
- Keep original filenames when possible
- Organize by type in subdirectories
- Use descriptive subdirectory names

### Output Files
- Use descriptive names: `dpor_analysis_report.html`
- Include date if time-sensitive: `evidence_summary_2025-12-07.json`
- Group by type: `reports/`, `summaries/`

### Documentation
- Use UPPERCASE for main guides: `FILING_GUIDE.md`
- Use descriptive names: `MAINTENANCE_GUIDE.md`
- Group in `docs/guides/` or `docs/reference/`

## Adding New Evidence

1. **Place files in appropriate subdirectory:**
   - Emails → `evidence/emails/`
   - Legal documents → `evidence/legal_documents/`
   - Excel files → `evidence/excel_files/`
   - etc.

2. **Run extraction scripts:**
   ```bash
   cd scripts/extraction
   Rscript extract_pdf_evidence.R
   Rscript extract_excel_evidence.R
   ```

3. **Update analysis:**
   ```bash
   cd scripts/analysis
   Rscript analyze_all_evidence.R
   ```

4. **Regenerate filing package:**
   ```bash
   Rscript organize_evidence.R
   ```

## Script Maintenance

### Active Scripts
- `scripts/extraction/extract_pdf_evidence.R` - PDF extraction
- `scripts/extraction/extract_excel_evidence.R` - Excel extraction
- `scripts/extraction/extract_all_evidence.R` - Master extraction
- `scripts/search/search_regulatory_agencies.R` - Agency registry
- `scripts/analysis/analyze_fraud_patterns.R` - Fraud analysis
- `scripts/analysis/analyze_all_evidence.R` - Evidence analysis
- `organize_evidence.R` - Master organization

### Legacy Scripts
- `scripts/legacy/search_dpor.R` - Initial search script (deprecated)
- `scripts/legacy/test_virginia_search.R` - Test script (deprecated)

### Root-Level Scripts
- `analyze_skidmore_connections.R` - Connection analysis
- `clean_dpor_data.py` - Data cleaning
- `validate_data_quality.R` - Data validation
- `generate_outputs.R` - Output generation
- `run_full_pipeline.R` - Full pipeline runner
- `demo_analysis_pipeline.R` - Demo pipeline

## Documentation Maintenance

### Guides (`docs/guides/`)
- `FILING_GUIDE.md` - How to file administrative complaints
- `EVIDENCE_SUMMARY.md` - Summary of all evidence
- `PROJECT_ORGANIZATION.md` - Project structure guide
- `README_FILINGS.md` - Quick start for filings

### Reference (`docs/reference/`)
- `kettler-filings-quick-reference.md` - Quick reference guide

### Main Documentation
- `README.md` - Main project documentation
- `docs/MAINTENANCE_GUIDE.md` - This file

## Data Management

### Data Directories
- `data/raw/` - Raw search results (gitignored)
- `data/cleaned/` - Cleaned data (gitignored)
- `data/analysis/` - Analysis outputs (gitignored)

### Research Directory
- `research/` - Contains extracted and analyzed evidence
- JSON files for structured data
- CSV files for summaries

### Outputs Directory
- `outputs/reports/` - Generated HTML reports
- `outputs/summaries/` - Summary CSV files

## Git Workflow

### Files to Commit
- Scripts in `scripts/`
- Documentation in `docs/`
- Configuration files (`.gitignore`, `requirements.txt`)
- Registry files (`state_dpor_registry.csv`)
- Evidence organization structure (directories, not contents)

### Files to Ignore (via .gitignore)
- `data/raw/*`, `data/cleaned/*`, `data/analysis/*`
- `*.log`, `*.RData`, `*.Rhistory`
- `__pycache__/`, `*.pyc`
- Evidence file contents (not structure)

## Troubleshooting

### Extraction Scripts Not Working
1. Check R packages are installed
2. Verify file paths are correct
3. Check file permissions
4. Review error messages in console

### Analysis Scripts Failing
1. Verify input files exist
2. Check JSON structure matches expected format
3. Review data types and column names
4. Check for missing dependencies

### Organization Script Issues
1. Verify evidence directory structure
2. Check file paths in scripts
3. Review cross-reference logic
4. Check for missing data files

## Best Practices

1. **Keep Scripts Modular**
   - One script per function
   - Clear input/output
   - Well-documented

2. **Maintain Documentation**
   - Update guides when structure changes
   - Document script purposes
   - Keep README current

3. **Organize Files Systematically**
   - Use consistent naming
   - Group related files
   - Keep structure logical

4. **Version Control**
   - Commit script changes
   - Don't commit data files
   - Use meaningful commit messages

5. **Regular Cleanup**
   - Remove duplicate files
   - Archive old outputs
   - Update deprecated scripts

## Quick Reference

### Key Commands
```bash
# Extract all evidence
cd scripts/extraction && Rscript extract_all_evidence.R

# Analyze evidence
cd scripts/analysis && Rscript analyze_all_evidence.R

# Organize evidence
Rscript organize_evidence.R

# Run full pipeline
Rscript run_full_pipeline.R
```

### Key Directories
- Evidence: `evidence/`
- Scripts: `scripts/`
- Documentation: `docs/`
- Research: `research/`
- Filings: `filings/`
- Outputs: `outputs/`

### Key Files
- Main README: `README.md`
- Filing Guide: `docs/guides/FILING_GUIDE.md`
- Evidence Summary: `docs/guides/EVIDENCE_SUMMARY.md`
- Filing Package: `filings/filing_evidence_package.json`
