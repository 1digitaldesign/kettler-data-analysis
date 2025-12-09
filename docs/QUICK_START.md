# Quick Start Guide

**For installation, see [INSTALLATION.md](../INSTALLATION.md)**

## For New Users

### 1. Understanding the Project
- Read [README.md](../README.md) for project overview
- Review [REPOSITORY_STRUCTURE.md](../REPOSITORY_STRUCTURE.md) for structure
- See [SYSTEM_ARCHITECTURE.md](../SYSTEM_ARCHITECTURE.md) for architecture

### 2. Filing Administrative Complaints
- See [FILING_GUIDE.md](guides/FILING_GUIDE.md) for complete instructions
- Check [kettler-filings-quick-reference.md](reference/kettler-filings-quick-reference.md) for quick reference
- Review `filings/filing_checklist.csv` for filing status

### 3. Finding Evidence
- See [EVIDENCE_SUMMARY.md](guides/EVIDENCE_SUMMARY.md) for evidence overview
- Check `research/evidence/` for extracted evidence summaries
- Review `filings/filing_evidence_package.json` for complete package

### 4. Running Analysis
- See [scripts/README.md](../scripts/README.md) for script documentation
- Run `python bin/run_pipeline.py` for full pipeline
- Run `python bin/organize_evidence.py` to organize evidence

## For Maintainers

### 1. Daily Tasks
- Add new evidence files to `evidence/` subdirectories
- Run extraction scripts: `scripts/extraction/extract_pdf_evidence.R`
- Update analysis: `scripts/analysis/analyze_all_evidence.R`

### 2. Weekly Tasks
- Review and clean output files in `outputs/`
- Update documentation as needed
- Review evidence organization

### 3. Monthly Tasks
- Archive old reports
- Update dependencies
- Review script organization

See [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) for detailed procedures.

## Key Files

### Documentation
- Main README: `README.md`
- Documentation Index: `docs/INDEX.md`
- Filing Guide: `docs/guides/FILING_GUIDE.md`
- Maintenance Guide: `docs/MAINTENANCE_GUIDE.md`

### Evidence
- Evidence Directory: `evidence/` (organized by type)
- Extracted Data: `research/pdf_evidence_extracted.json`
- Summary: `research/all_evidence_summary.json`

### Filings
- Checklist: `filings/filing_checklist.csv`
- Evidence Package: `filings/filing_evidence_package.json`
- Executive Summary: `filings/executive_summary.md`

### Scripts
- Master Organization: `organize_evidence.R`
- Extraction: `scripts/extraction/`
- Analysis: `scripts/analysis/`
- Search: `scripts/search/`

## Common Tasks

### Extract New Evidence
```bash
cd scripts/extraction
Rscript extract_pdf_evidence.R
Rscript extract_excel_evidence.R
```

### Analyze Evidence
```bash
cd scripts/analysis
Rscript analyze_all_evidence.R
```

### Organize All Evidence
```bash
Rscript organize_evidence.R
```

### Run Full Pipeline
```bash
Rscript run_full_pipeline.R
```

## Getting Help

- **Documentation:** See `docs/INDEX.md` for complete index
- **Scripts:** See `scripts/README.md` for script documentation
- **Maintenance:** See `docs/MAINTENANCE_GUIDE.md` for maintenance procedures
- **Filing:** See `docs/guides/FILING_GUIDE.md` for filing instructions
