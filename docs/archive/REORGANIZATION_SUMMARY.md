# Repository Reorganization Summary

**Date:** December 9, 2025

## Overview

The repository has been comprehensively reorganized to improve:
- **Clarity**: Clear separation between entry points and library code
- **Organization**: Research files organized by category
- **Maintainability**: Centralized path management
- **Discoverability**: Logical directory structure

## Major Changes

### 1. Created `/bin` Directory

All main entry point scripts moved to `bin/`:

| Old Location | New Location |
|-------------|--------------|
| `run_full_pipeline.R` | `bin/run_pipeline.R` |
| `search_multi_state_dpor.R` | `bin/search_states.R` |
| `analyze_skidmore_connections.R` | `bin/analyze_connections.R` |
| `validate_data_quality.R` | `bin/validate_data.R` |
| `generate_outputs.R` | `bin/generate_reports.R` |
| `organize_evidence.R` | `bin/organize_evidence.R` |
| `clean_dpor_data.py` | `bin/clean_data.py` |

### 2. Organized `/research` Directory

Research files organized into subdirectories:

- **`connections/`** - Connection analyses
  - `caitlin_skidmore_connections.json`
  - `hyland_skidmore_connections.json`
  - `connection_matrix.json`
  - `real_nexus_analysis.json`
  - `nexus_patterns_analysis.json`
  - `shared_resources_analysis.json`

- **`violations/`** - Violation findings
  - `all_violations_compiled.json`
  - `hyland_upl_investigation.json`
  - `upl_evidence_extracted.json`
  - `news_violations_search.json`
  - `HYLAND_UPL_EVIDENCE.md`

- **`anomalies/`** - Anomaly reports
  - `all_anomalies_consolidated.json`
  - `all_anomalies_updated.json`
  - `additional_anomalies.json`
  - `fraud_indicators.json`

- **`evidence/`** - Evidence summaries
  - `all_evidence_summary.json`
  - `all_entities_extracted.json`
  - `all_individuals_identified.json`
  - `pdf_evidence_extracted.json`
  - `pdf_evidence_summary.csv`
  - `excel_evidence_extracted.json`
  - `excel_evidence_summary.csv`
  - `email_domain_analysis.json`
  - `str_listings_analysis.json`
  - `alexandria_zoning_analysis.json`

- **`verification/`** - Verification results
  - `hyland_verification.json`
  - `kettler_verification.json`
  - `skidmore_firms_validation.json`
  - `business_license_verification.json`
  - `property_management_license_verification.json`
  - `bar_association_verification_all.json`
  - `dpor_license_verification_all.json`
  - `management_chain_license_audit.json`

- **`timelines/`** - Timeline analyses
  - `timeline_analysis.json`
  - `lease_evidence_cross_reference.json`
  - `lease_abnormalities_detailed.json`
  - `lease_agreement_analysis.json`

- **`summaries/`** - Summary reports
  - `filing_recommendations.json`
  - `FINAL_NEXUS_FINDINGS.md`
  - `NEXUS_ANALYSIS_REPORT.md`
  - `validation_report.md`
  - `DATABASE_SEARCH_FRAMEWORK.md`

- **`search_results/`** - Search result files
  - All `*_search*.json` files
  - All `*_results.json` files

### 3. Moved Configuration Files

- `state_dpor_registry.csv` → `config/state_dpor_registry.csv`
- `config/gcp-env-template.txt` → `config/templates/gcp-env-template.txt`

### 4. Moved Documentation

- `MICROSERVICES_ARCHITECTURE.md` → `docs/architecture/`
- `GCP_SETUP.md` → `docs/`
- `GOOGLE_DRIVE_SETUP.md` → `docs/`

### 5. Created Path Utilities

- **`scripts/utils/paths.R`** - Centralized path management
- **`scripts/utils/research_paths.R`** - Research file path helpers
- **`bin/load_paths.R`** - Path loading utility for bin scripts

### 6. Updated Script References

- Updated 23+ scripts to use new file paths
- Updated `source()` calls to use new script locations
- Updated file path references throughout codebase

## New Directory Structure

```
.
├── bin/                    # Entry point scripts
├── scripts/                # Library scripts
│   ├── search/
│   ├── analysis/
│   ├── extraction/
│   ├── validation/
│   ├── reporting/
│   ├── etl/
│   ├── microservices/
│   └── utils/
├── data/                   # Data directories
│   ├── source/
│   ├── raw/
│   ├── cleaned/
│   ├── analysis/
│   ├── scraped/
│   └── vectors/
├── research/               # Research outputs (organized)
│   ├── connections/
│   ├── violations/
│   ├── anomalies/
│   ├── evidence/
│   ├── verification/
│   ├── timelines/
│   ├── summaries/
│   └── search_results/
├── evidence/               # Source evidence
├── filings/                # Filing materials
├── docs/                   # Documentation
│   ├── guides/
│   ├── reference/
│   └── architecture/
├── config/                 # Configuration
│   └── templates/
└── outputs/                # Generated outputs
```

## Usage Changes

### Before
```r
source("search_multi_state_dpor.R")
source("analyze_skidmore_connections.R")
```

### After
```r
source("bin/search_states.R")
source("bin/analyze_connections.R")
```

Or use the path utilities:
```r
source("scripts/utils/paths.R")
source_bin("search_states.R")
```

## Benefits

1. **Clear Entry Points**: All main scripts in `bin/` directory
2. **Organized Research**: Easy to find files by category
3. **Centralized Paths**: Single source of truth for paths
4. **Better Discoverability**: Logical organization
5. **Easier Maintenance**: Clear structure reduces confusion

## Migration Guide

### For Scripts

1. **Load paths utility:**
   ```r
   source("scripts/utils/paths.R")
   ```

2. **Use predefined paths:**
   ```r
   file.path(RESEARCH_EVIDENCE_DIR, "all_entities_extracted.json")
   ```

3. **Use research path helpers:**
   ```r
   source("scripts/utils/research_paths.R")
   get_entities_file()
   ```

### For Documentation

- Update references to moved files
- Use new paths in examples
- Update cross-references

## Files Updated

- 23+ R scripts updated with new paths
- All bin scripts updated
- README.md updated
- Documentation reorganized
- Path utilities created

## Next Steps

1. Test all scripts with new paths
2. Update any remaining hardcoded paths
3. Update documentation references
4. Verify all file references work correctly

## Notes

- Empty directories (`address_clusters`, `license_violations`, `regulatory_agencies`) remain for future use
- Some scripts may still need path updates - check with `scripts/utils/update_paths.R`
- All changes are backward compatible where possible (fallback paths included)
