# Naming Conventions

![Conventions](https://img.shields.io/badge/conventions-standardized-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

Comprehensive naming convention guide for all files in the repository.

---

## Overview

This document defines consistent naming conventions for all file types in the repository to ensure:
- **Discoverability** - Easy to find files by purpose
- **Consistency** - Predictable naming patterns
- **Clarity** - Clear file purpose from name
- **Maintainability** - Easy to organize and refactor

---

## General Principles

1. **Use descriptive names** - File names should clearly indicate content
2. **Be consistent** - Follow the same pattern within each file type
3. **Avoid abbreviations** - Use full words unless universally understood
4. **Use separators** - Separate words with underscores or hyphens (no spaces)
5. **Lowercase preferred** - Use lowercase for data files and code

---

## File Type Conventions

### Documentation Files (`.md`)

**Pattern:** `SCREAMING_SNAKE_CASE` for important documents, `kebab-case` for guides

**Categories:**

| Category | Pattern | Examples |
|----------|---------|----------|
| **Core Documentation** | `SCREAMING_SNAKE_CASE` | `README.md`, `DATA_DICTIONARY.md`, `SYSTEM_ARCHITECTURE.md` |
| **Guides** | `kebab-case` | `quick-start.md`, `installation.md`, `complaint-amendment-guide.md` |
| **Reports** | `SCREAMING_SNAKE_CASE` | `REPORTS.md`, `EXECUTIVE_SUMMARY.md` |
| **Archives** | `SCREAMING_SNAKE_CASE` | `ARCHIVE.md` |

**Rules:**
- Core documentation: `SCREAMING_SNAKE_CASE` (e.g., `DATA_DICTIONARY.md`)
- User guides: `kebab-case` (e.g., `quick-start.md`)
- Status/archive files: `SCREAMING_SNAKE_CASE` (e.g., `ARCHIVE.md`)
- Investigation files: `kebab-case` (e.g., `lariat-companies-search.md`)

### Data Files (`.json`)

**Pattern:** `snake_case`

**Categories:**

| Category | Pattern | Examples |
|----------|---------|----------|
| **Source Data** | `snake_case` | `skidmore_all_firms_complete.json` |
| **Analysis Outputs** | `{entity}_{type}_{category}.json` | `hyland_upl_investigation.json` |
| **Search Results** | `{state}_{person}_search.json` | `virginia_caitlin_skidmore_search.json` |
| **Compilations** | `{purpose}_compilation.json` | `complaint_evidence_compilation.json` |

**Rules:**
- Use `snake_case` (lowercase with underscores)
- Include entity name, type, and category when applicable
- Use descriptive suffixes: `_analysis`, `_summary`, `_results`, `_compilation`
- License searches: `{state}_{person_name}_search.json`

### Python Files (`.py`)

**Pattern:** `snake_case`

**Rules:**
- Use `snake_case` for all Python files
- Module files: descriptive name (e.g., `unified_analysis.py`)
- Utility files: `{purpose}.py` (e.g., `validate_schema.py`)
- Entry points: `{action}.py` (e.g., `run_pipeline.py`)

### Configuration Files

| File Type | Pattern | Examples |
|-----------|---------|----------|
| `requirements.txt` | `lowercase` | `requirements.txt` |
| `schema.json` | `lowercase` | `schema.json`, `metadata.json` |
| `.gitignore` | `lowercase` | `.gitignore` |

---

## Directory Naming

**Pattern:** `lowercase` with hyphens for multi-word directories

**Examples:**
- `license_searches/` - License search results
- `va_dpor_complaint/` - VA DPOR complaint files
- `browser_automation/` - Browser automation scripts

**Rules:**
- Use `snake_case` for directories
- Be descriptive and specific
- Avoid abbreviations

---

## Naming Patterns by Purpose

### Research Files

| Purpose | Pattern | Example |
|---------|---------|---------|
| **Core Guides** | `SCREAMING_SNAKE_CASE.md` | `README.md`, `DATA_GUIDE.md` |
| **Reports** | `SCREAMING_SNAKE_CASE.md` | `REPORTS.md`, `EXECUTIVE_SUMMARY.md` |
| **Investigations** | `kebab-case.md` | `lariat-companies-search.md` |
| **Evidence** | `snake_case.json` | `complaint_evidence_compilation.json` |
| **Analysis** | `{entity}_{type}.json` | `hyland_upl_investigation.json` |

### Documentation Files

| Purpose | Pattern | Example |
|---------|---------|---------|
| **Index/README** | `SCREAMING_SNAKE_CASE.md` | `INDEX.md`, `README.md` |
| **Guides** | `kebab-case.md` | `quick-start.md`, `installation.md` |
| **Architecture** | `SCREAMING_SNAKE_CASE.md` | `SYSTEM_ARCHITECTURE.md` |
| **Reference** | `SCREAMING_SNAKE_CASE.md` | `DATA_DICTIONARY.md` |

---

## Special Cases

### Status/Progress Files

**Pattern:** Archive in `archive/` directory, use descriptive names

**Examples:**
- `archive/execution_summary.md`
- `archive/final_deliverables_summary.md`

### Investigation Files

**Pattern:** `kebab-case.md` in `investigations/` directory

**Examples:**
- `investigations/lariat-companies-search.md`
- `investigations/virginia-40-licenses-finding.md`

### License Search Files

**Pattern:** `{state}_{person_name}_search.json`

**Examples:**
- `virginia_caitlin_skidmore_search.json`
- `maryland_edward_hyland_search.json`

---

## Migration Strategy

### Phase 1: Core Documentation
- Rename essential documentation files
- Update all references

### Phase 2: Research Files
- Rename research documentation
- Rename data files
- Update references

### Phase 3: Investigation Files
- Move to `investigations/` with kebab-case names
- Update references

### Phase 4: Archive Files
- Standardize archive file names
- Update references

---

## Examples

### Before → After

| Before | After | Reason |
|--------|-------|--------|
| `ALL_STATES_LARIAT_COMPANIES_SEARCH.md` | `investigations/lariat-companies-search.md` | Investigation file → kebab-case |
| `HYLAND_UPL_EVIDENCE.md` | `investigations/hyland-upl-evidence.md` | Investigation file → kebab-case |
| `VIRGINIA_40_LICENSES_CRITICAL_FINDING.md` | `investigations/virginia-40-licenses-finding.md` | Investigation file → kebab-case |
| `COMPLAINT_EVIDENCE_COMPILATION.json` | `complaint_evidence_compilation.json` | Data file → snake_case |
| `RESEARCH_EXECUTION_PROGRESS.json` | `archive/json/research_execution_progress.json` | Status file → archive, snake_case |

---

## Validation

Files should be validated against these conventions:
- ✅ Documentation files follow SCREAMING_SNAKE_CASE or kebab-case
- ✅ Data files follow snake_case
- ✅ Python files follow snake_case
- ✅ Directory names follow snake_case
- ✅ No spaces in file names
- ✅ No special characters except `-` and `_`

---

## Related Documentation

- [Repository Structure](REPOSITORY_STRUCTURE.md) - File organization
- [Data Dictionary](../data/DATA_DICTIONARY.md) - Data file structure
- [System Architecture](SYSTEM_ARCHITECTURE.md) - Code organization

---

**Last Updated:** 2025-12-10
**Convention Version:** 1.0.0
