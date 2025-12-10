# License Searches Directory

Multi-state license search results and investigation files.

![Searches](https://img.shields.io/badge/searches-285%20files-blue)
![States](https://img.shields.io/badge/states-15-orange)

## About this directory

This directory contains license search results from 15 states, organized by state and search type. Each search result follows the schema in `data/schema.json`.

---

## Directory structure

```
license_searches/
├── virginia/          # 19 files
├── maryland/          # 37 files
├── connecticut/       # 22 files
├── new_jersey/        # 22 files
├── new_york/          # 21 files
├── dc/                # 21 files
├── florida/           # 15 files
├── [9 more states]/   # Additional state directories
└── consolidated/      # Consolidated results
```

---

## Search results

### By state

Each state directory contains:
- Individual license search results (JSON)
- Batch search results (JSON)
- State-specific findings and summaries

### Key files

- `*_results.json` - Search results
- `*_finding.json` - Specific findings
- `*_batch*.json` - Batch search results

---

## Historical status files

Many markdown files in this directory are historical status updates from during the investigation. These have been archived in `archive/` and are not needed for current research.

**Focus on:**
- JSON files (actual search results)
- Consolidated results in `consolidated/`
- Complaint letters in `complaint_letters/`
- Essential guides: `README.md`, `EXECUTIVE_SUMMARY_FOR_FILINGS.md`, `COMPLETE_INVESTIGATION_PACKAGE.md`

---

## Related documentation

- [Research README](../README.md) - Research directory guide
- [Reports](../REPORTS.md) - Consolidated reports
- [Data Guide](../DATA_GUIDE.md) - Data structure guide

---

**Last Updated:** 2025-12-10
