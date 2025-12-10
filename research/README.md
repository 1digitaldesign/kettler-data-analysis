# Research Directory

Complete research outputs from multi-state license investigation and regulatory compliance analysis.

![Research](https://img.shields.io/badge/research-100%25%20complete-brightgreen)
![Files](https://img.shields.io/badge/files-350%20JSON-blue)
![States](https://img.shields.io/badge/states-15%20searched-orange)

## About this directory

This directory contains all research outputs from investigating property management licensing compliance across 15 states. The data includes license searches, connection analyses, violation findings, and evidence compilation for regulatory complaints.

**What you'll find:**
- License search results from 15 states
- Connection analyses between firms and individuals
- Violation findings and anomaly reports
- Evidence compilation for regulatory complaints
- Analysis outputs and summary reports

---

## Quick navigation

**Start here based on your goal:**

| Goal | Start Here |
|------|------------|
| **File a complaint** | [VA DPOR Complaint Files](va_dpor_complaint/) |
| **Find specific data** | [Research Index](RESEARCH_INDEX.json) |
| **View summaries** | [Reports Directory](reports/) |
| **Search licenses** | [License Searches](license_searches/) |

---

## Data organization

Research files are organized by category and purpose:

### License searches

**Location:** `license_searches/`  
**Count:** 285 files across 15 states  
**Purpose:** Multi-state license search results for individuals and firms

**Structure:**
- One subdirectory per state (e.g., `virginia/`, `maryland/`, `connecticut/`)
- JSON files containing search results
- Each file follows the schema in `data/schema.json`

**Key states:**
- Virginia: 19 files
- Maryland: 37 files
- Connecticut: 22 files
- New Jersey: 22 files
- New York: 21 files
- DC: 21 files
- Plus 9 more states

### VA DPOR complaint

**Location:** `va_dpor_complaint/`  
**Count:** 20 files  
**Purpose:** Complete research package for Virginia DPOR complaint filing

**Key files:**
- `EXECUTIVE_SUMMARY.json` - Executive summary
- `COMPREHENSIVE_PERSONNEL_VERIFICATION_REPORT.json` - Personnel verification
- `50_mile_rule_violations.json` - Geographic violations
- `corporate_structure_analysis.json` - Corporate structure

### Reports

**Location:** `reports/`  
**Count:** 11 markdown files  
**Purpose:** Summary reports and findings

**Key reports:**
- `COMPREHENSIVE_VIOLATIONS_REPORT.md` - All violations found
- `FINAL_VIOLATION_SUMMARY.md` - Violation summary
- `ALL_ANOMALIES_SUMMARY.md` - Anomaly findings
- `NEXUS_ANALYSIS_REPORT.md` - Nexus analysis

### Connections

**Location:** `connections/`  
**Count:** 1 file  
**Purpose:** Connection analyses between firms and individuals

**File:** `caitlin_skidmore_connections.json`

### Analysis

**Location:** `analysis/`  
**Count:** 15 files  
**Purpose:** General analysis outputs

**Key files:**
- `all_evidence_summary.json` - Evidence summary
- `real_nexus_analysis.json` - Nexus analysis
- `hyland_upl_investigation.json` - UPL investigation
- `connection_matrix.json` - Connection matrix

---

## Understanding the data

### Data format

All JSON files follow the schema defined in `data/schema.json`:

- **Primary Keys:** Auto-generated unique IDs
- **Foreign Keys:** References to `firms.firm_license` and `individual_licenses.license_number`
- **Categories:** connections, violations, anomalies, evidence, verification, timelines, summaries, search_results, analysis, va_dpor_complaint

### File naming conventions

- **License searches:** `{state}_{person_name}_search.json`
- **Violations:** `{type}_violations.json`
- **Reports:** `{category}_{summary_type}.md`
- **Status files:** Historical status updates (can be ignored)

### Status and progress files

Many markdown files with names like `STATUS`, `COMPLETE`, `PROGRESS`, `UPDATE` are historical status updates from during the investigation. These can be ignored for current research. Focus on:

- JSON files in subdirectories (actual data)
- Files in `reports/` directory (summaries)
- Files in `va_dpor_complaint/` directory (complaint package)

---

## Key findings

### Violations

- 8 regulatory violations across 11 states
- Principal broker gap: 10.5 years
- Geographic violation: 1,300 miles
- 16 unlicensed personnel (7 property managers)

### Scope

- 38 firms investigated
- 40+ individual licenses searched
- 100+ connections mapped
- $4.75B property value under management

---

## Using the research data

### For complaint filing

1. Start with `va_dpor_complaint/EXECUTIVE_SUMMARY.json`
2. Review `va_dpor_complaint/COMPREHENSIVE_PERSONNEL_VERIFICATION_REPORT.json`
3. Check `reports/COMPREHENSIVE_VIOLATIONS_REPORT.md`

### For data analysis

1. Use `RESEARCH_INDEX.json` to find specific files
2. Browse `license_searches/` by state
3. Review `analysis/` for processed data

### For understanding findings

1. Read `reports/FINAL_VIOLATION_SUMMARY.md`
2. Check `reports/ALL_ANOMALIES_SUMMARY.md`
3. Review `reports/NEXUS_ANALYSIS_REPORT.md`

---

## Directory structure

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
└── [root status files] # Historical status (can ignore)
```

---

## Related documentation

- [Data Dictionary](../data/DATA_DICTIONARY.md) - Field definitions
- [Data Schema](../data/schema.json) - Complete schema
- [Research Index](RESEARCH_INDEX.json) - Master file index
- [Main README](../README.md) - Project overview

---

**Status:** 100% Complete - Ready for Complaint Filing
