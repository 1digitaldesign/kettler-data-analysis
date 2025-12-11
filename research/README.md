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
| **View summaries** | [Reports](REPORTS.md) |
| **Search licenses** | [License Searches](license_searches/) |
| **Check search completion** | [Research Outline](RESEARCH_OUTLINE.md) |
| **View consolidation** | [Consolidation View](CONSOLIDATION_VIEW.json) |

---

## Research Outline System

All searches are organized using a standardized outline system:

- **[RESEARCH_OUTLINE.json](RESEARCH_OUTLINE.json)** - Master definition of all 10 search categories
- **[CONSOLIDATION_VIEW.json](CONSOLIDATION_VIEW.json)** - Consolidated view with statistics and completion status
- **[RESEARCH_OUTLINE.md](RESEARCH_OUTLINE.md)** - Complete documentation

**Check completion status:**
```bash
python3.14 scripts/research/check_search_completion.py
```

**Generate consolidation view:**
```bash
python3.14 scripts/research/generate_consolidation_view.py
```

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

**See [REPORTS.md](REPORTS.md) for consolidated report index.**

### Investigations

**Location:** `investigations/`
**Count:** 12 investigation-specific files
**Purpose:** Detailed investigation findings and analyses

**Key investigations:**
- Lariat Realty Advisors investigations
- Virginia license findings
- Method comparisons
- Specific violation analyses

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

---

## Understanding the data

### Data format

All JSON files follow the schema in `data/schema.json`:
- **Primary Keys (PK)**: Unique identifiers
- **Foreign Keys (FK)**: Relationships between entities
- **Metadata**: Creation date, source, lineage

### File naming conventions

- `*_results.json` - Search results
- `*_connections.json` - Connection analyses
- `*_violations.json` - Violation findings
- `*_analysis.json` - Analysis outputs
- `*_summary.json` - Summary reports

### Status and progress files

Many markdown files in this directory are historical status updates from during the investigation. See [ARCHIVE.md](ARCHIVE.md) for consolidated archive of all status files.

**Focus on:**
- JSON files (actual data)
- Files in `reports/` (summaries)
- Files in `va_dpor_complaint/` (complaint package)
- Main guides: `README.md`, `DATA_GUIDE.md`, `REPORTS.md`

---

## Key findings

### Violations identified

- **8 regulatory violations** across 11 states
- **Principal broker gap:** 10.5 years
- **Geographic violation:** 1,300 miles
- **16 unlicensed personnel** (7 property managers)
- **$4.75B property value** under management

### Critical violations

1. **Edward Hyland** - Unlicensed practice of real estate (Virginia)
2. **Principal Broker Gap** - Firm licensed 10.5 years before broker
3. **Geographic Violations** - Operations beyond licensed jurisdiction
4. **Supervision Impossibility** - Too many properties for one broker

---

## Using the research data

### For complaint filing

1. Start with [VA DPOR Complaint Files](va_dpor_complaint/)
2. Review [Reports](REPORTS.md) for key findings
3. Use [Research Index](research_index.json) to find specific evidence

### For data analysis

1. Check [Data Guide](DATA_GUIDE.md) for data structure
2. Review [Data Catalog](../data/DATA_CATALOG.md) for asset discovery
3. Use JSON files in subdirectories for analysis

### For understanding findings

1. Read [Reports](REPORTS.md) for summaries
2. Review violation files in `reports/`
3. Check connection analyses in `connections/`

---

## Related documentation

### Data documentation
- [Data Catalog](../data/DATA_CATALOG.md) - Data asset catalog
- [Data Dictionary](../data/DATA_DICTIONARY.md) - Field definitions
- [Data Guide](DATA_GUIDE.md) - Complete data guide
- [Schema](../data/schema.json) - JSON Schema definitions

### System documentation
- [Documentation Index](../docs/INDEX.md) - Complete documentation index
- [System Architecture](../docs/SYSTEM_ARCHITECTURE.md) - System architecture

---

**Last Updated:** 2025-12-10
**Research Status:** 100% Complete
