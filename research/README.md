# Research Directory

This directory contains all research outputs organized by category and methodology.

## Directory Structure

```
research/
├── browser_automation/     # Browser automation results (Playwright MCP)
│   ├── azure_carlyle_*.json
│   ├── browser_automation_*.json
│   ├── captcha_handled_*.json
│   └── DATABASE_SEARCH_FRAMEWORK.md
│
├── license_searches/       # License search results by state
│   ├── virginia/          # Virginia DPOR search results
│   ├── maryland/          # Maryland DLLR search results
│   ├── dc/                # DC OCPLA search results
│   ├── new_york/          # New York DOS search results
│   ├── new_jersey/        # New Jersey Consumer Affairs results
│   ├── connecticut/       # Connecticut DCP search results
│   ├── CORRECT_URLS_FOUND.json
│   └── *LICENSE*.md       # License search reports
│
├── analysis/              # Analysis and investigation results
│   ├── *analysis*.json
│   ├── *anomalies*.json
│   ├── *violations*.json
│   ├── *nexus*.json
│   ├── *connection*.json
│   ├── *evidence*.json
│   └── *.csv
│
└── reports/              # Comprehensive reports and summaries
    ├── *REPORT*.md
    ├── *SUMMARY*.md
    ├── *AUDIT*.md
    └── *FINDINGS*.md
```

## MCP Tools Used

### Playwright Browser Automation
- **Purpose:** Automated license searches, web scraping, database queries
- **Results Location:** `browser_automation/` and `license_searches/`
- **Key Features:**
  - State licensing database searches
  - CAPTCHA handling
  - Multi-state license verification
  - Real estate license lookups

## Research Workflow

1. **Browser Automation** → `browser_automation/`
   - Automated searches using Playwright MCP
   - Database queries and web scraping
   - CAPTCHA handling results

2. **License Searches** → `license_searches/`
   - Organized by state
   - JSON results and markdown reports
   - URL documentation

3. **Analysis** → `analysis/`
   - Pattern analysis
   - Connection mapping
   - Violation identification
   - Evidence extraction results

4. **Reporting** → `reports/`
   - Comprehensive summaries
   - Audit reports
   - Findings documentation

## Quick Access

- **License Search Status:** `license_searches/LICENSE_SEARCH_SUMMARY_AND_NEXT_STEPS.md`
- **Browser Automation:** `browser_automation/DATABASE_SEARCH_FRAMEWORK.md`
- **Latest Report:** `reports/COMPREHENSIVE_KETTLER_EMPLOYEES_LICENSE_SEARCH.md`
