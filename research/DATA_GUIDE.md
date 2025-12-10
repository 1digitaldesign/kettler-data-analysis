# Research Data Guide

Complete guide to understanding and using research data in this directory.

## About this guide

This guide explains what research data exists, how it's organized, and how to use it. Use this guide when you need to:

- Find specific research data
- Understand data structure
- Navigate the research directory
- Use data for complaints or analysis

---

## Data categories

Research data is organized into five main categories:

### 1. License searches

**What it is:** License search results from 15 state databases
**Where:** `license_searches/` directory
**Format:** JSON files
**Count:** 285 files

**Purpose:** Contains search results for individuals and firms across multiple states. Each file contains license information, status, and related data.

**How to use:**
- Browse by state subdirectory
- Search for specific person names
- Use for license verification

### 2. VA DPOR complaint

**What it is:** Complete research package for Virginia DPOR complaint
**Where:** `va_dpor_complaint/` directory
**Format:** JSON files
**Count:** 20 files

**Purpose:** All research compiled specifically for filing a complaint with Virginia DPOR. Includes violations, evidence, and verification data.

**How to use:**
- Start with `EXECUTIVE_SUMMARY.json`
- Review verification reports
- Check violation files

### 3. Reports

**What it is:** Summary reports and findings
**Where:** `reports/` directory
**Format:** Markdown files
**Count:** 11 files

**Purpose:** Human-readable summaries of findings, violations, and anomalies.

**How to use:**
- Read summaries for overview
- Check violation reports
- Review anomaly findings

### 4. Connections

**What it is:** Connection analyses between firms and individuals
**Where:** `connections/` directory
**Format:** JSON files
**Count:** 1 file

**Purpose:** Maps relationships between firms and licensed individuals.

**How to use:**
- Analyze firm-individual relationships
- Understand management chains
- Identify connection patterns

### 5. Analysis

**What it is:** Processed analysis outputs
**Where:** `analysis/` directory
**Format:** JSON files
**Count:** 15 files

**Purpose:** Processed data from various analyses including nexus, evidence, and email domains.

**How to use:**
- Review processed findings
- Check evidence summaries
- Analyze connection matrices

---

## File types explained

### JSON files

**Purpose:** Structured data following `data/schema.json`
**Use:** Programmatic access, data analysis
**Examples:** License searches, violation data, evidence

### Markdown files

**Purpose:** Human-readable summaries and reports
**Use:** Reading summaries, understanding findings
**Examples:** Violation reports, status summaries

### Status files

**Purpose:** Historical status updates (can be ignored)
**Use:** Historical reference only
**Examples:** Files with names like `STATUS`, `COMPLETE`, `PROGRESS`

---

## Finding specific data

### By state

License searches are organized by state:
- `license_searches/virginia/` - Virginia searches
- `license_searches/maryland/` - Maryland searches
- `license_searches/connecticut/` - Connecticut searches
- And 12 more states

### By person name

License search files use naming pattern:
- `{state}_{person_name}_search.json`
- Example: `virginia_caitlin_skidmore_search.json`

### By category

Use `research_index.json` to find files by category:
- Connections
- Violations
- Anomalies
- Evidence
- Verification

---

## Data schema

All JSON files follow the schema in `data/schema.json`:

- **Primary Keys:** Unique identifiers
- **Foreign Keys:** References to firms and licenses
- **Categories:** Predefined categories for organization

See [Data Dictionary](../data/DATA_DICTIONARY.md) for complete field definitions.

---

## Common tasks

### Task: File a complaint

1. Start with `va_dpor_complaint/EXECUTIVE_SUMMARY.json`
2. Review `va_dpor_complaint/COMPREHENSIVE_PERSONNEL_VERIFICATION_REPORT.json`
3. Check `reports/COMPREHENSIVE_VIOLATIONS_REPORT.md`

### Task: Find license information

1. Go to `license_searches/{state}/`
2. Search for person name
3. Open corresponding JSON file

### Task: Understand violations

1. Read `reports/FINAL_VIOLATION_SUMMARY.md`
2. Check `reports/COMPREHENSIVE_VIOLATIONS_REPORT.md`
3. Review violation JSON files in `va_dpor_complaint/`

### Task: Analyze connections

1. Open `connections/caitlin_skidmore_connections.json`
2. Review `analysis/connection_matrix.json`
3. Check related license searches

---

## Key statistics

| Metric | Value |
|--------|-------|
| **Total Files** | 350 JSON + 30 MD |
| **License Searches** | 285 files |
| **States Covered** | 15 states |
| **Firms Investigated** | 38 firms |
| **Individual Licenses** | 40+ licenses |
| **Connections Mapped** | 100+ connections |

---

## Related documentation

- [Research README](README.md) - Research directory overview
- [Research Index](RESEARCH_INDEX.json) - Master file index
- [Data Dictionary](../data/DATA_DICTIONARY.md) - Field definitions
- [Data Schema](../data/schema.json) - Complete schema
