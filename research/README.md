# Research Directory

**Total Files:** 350 JSON + 30 MD + 3 CSV + 5 TXT
**Status:** 100% Complete - Ready for Complaint Filing

## Quick Navigation

- **[RESEARCH_INDEX.json](./RESEARCH_INDEX.json)** - Master index of all files
- **[va_dpor_complaint/](./va_dpor_complaint/)** - VA DPOR complaint research files
- **[reports/](./reports/)** - Summary reports and findings

## Directory Structure

```
research/
├── connections/          # Connection analyses (1 file)
├── analysis/            # Analysis outputs (15 files)
├── license_searches/    # Multi-state searches (285 files)
│   ├── virginia/       # 19 files
│   ├── maryland/       # 37 files
│   ├── connecticut/    # 22 files
│   └── [12 more states]
├── va_dpor_complaint/   # Complaint research (20 files)
├── reports/             # Summary reports (11 files)
└── [root files]         # Root-level files (13 files)
```

## Categories

### Connections
- **Directory:** `connections/`
- **Key File:** `caitlin_skidmore_connections.json`
- **Description:** Connections between firms and individuals

### Analysis
- **Directory:** `analysis/`
- **Key Files:** `all_evidence_summary.json`, `real_nexus_analysis.json`
- **Description:** General analysis outputs

### License Searches
- **Directory:** `license_searches/`
- **Total:** 285 files across 15 states
- **Description:** Multi-state license search results

### VA DPOR Complaint
- **Directory:** `va_dpor_complaint/`
- **Key File:** `EXECUTIVE_SUMMARY.json`
- **Description:** Complaint research and evidence

### Reports
- **Directory:** `reports/`
- **Key Files:** `COMPREHENSIVE_VIOLATIONS_REPORT.md`, `FINAL_VIOLATION_SUMMARY.md`
- **Description:** Summary reports and findings

## Key Files

**For Complaint Filing:**
- `va_dpor_complaint/EXECUTIVE_SUMMARY.json`
- `COMPLAINT_EVIDENCE_COMPILATION.json`
- `COMPLAINT_AMENDMENT_GUIDE.md`

**For Understanding Findings:**
- `MASTER_RESEARCH_COMPLETION_REPORT.md`
- `FINAL_100_PERCENT_VERIFIED.json`
- `RESEARCH_INDEX.json`

## File Organization

All research files follow the schema defined in `data/schema.json`:
- **Primary Keys:** Auto-generated IDs
- **Foreign Keys:** References to `firms.firm_license` and `individual_licenses.license_number`
- **Categories:** connections, violations, anomalies, evidence, verification, timelines, summaries, search_results, analysis, va_dpor_complaint

## Related Documentation

- [Data Dictionary](../data/DATA_DICTIONARY.md) - Field definitions
- [Data Schema](../data/schema.json) - Complete schema
- [Research Index](./RESEARCH_INDEX.json) - Master file index
