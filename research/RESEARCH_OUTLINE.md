# Research Outline System

Complete guide to the research outline system for organizing and tracking all search activities.

## Overview

The Research Outline System provides a standardized structure for organizing all research searches, tracking completion status, and generating consolidated views of research data.

## Key Components

### 1. RESEARCH_OUTLINE.json

Master definition file that specifies:
- All 10 search categories
- Data folder structure for each search
- Completion criteria
- File patterns and requirements

**Location:** `research/RESEARCH_OUTLINE.json`

### 2. CONSOLIDATION_VIEW.json

Auto-generated consolidated view containing:
- Summary statistics for all searches
- Completion status (1=complete, 0=incomplete)
- File counts and data sizes
- Cross-references by priority, completion, and data folder

**Location:** `research/CONSOLIDATION_VIEW.json`

**Regeneration:** Run `python3.14 scripts/research/generate_consolidation_view.py`

### 3. Completion Checker

Python script that checks completion status for searches.

**Location:** `scripts/research/check_search_completion.py`

**Usage:**
```bash
# Check all searches
python3.14 scripts/research/check_search_completion.py

# Check specific search
python3.14 scripts/research/check_search_completion.py license_searches
# Returns: 1 (complete) or 0 (incomplete)
```

## Search Categories

### 1. License Searches
- **ID:** `license_searches`
- **Data Folder:** `research/license_searches/data`
- **Description:** Multi-state license searches for real estate brokers, salespersons, and bar licenses
- **Priority:** High
- **Structure:** Organized by state subdirectories

### 2. Company Registrations
- **ID:** `company_registrations`
- **Data Folder:** `research/company_registrations/data`
- **Description:** Business entity registration searches across operational states
- **Priority:** High
- **Structure:** Organized by state subdirectories

### 3. Property Management Contracts
- **ID:** `property_contracts`
- **Data Folder:** `research/contracts/data`
- **Description:** Property management contracts, service agreements, and property lists
- **Priority:** High
- **Structure:** Flat structure with key files

### 4. Employee Role Documentation
- **ID:** `employee_roles`
- **Data Folder:** `research/employees/data`
- **Description:** Employee job descriptions, organizational charts, and role verification
- **Priority:** High
- **Structure:** Flat structure with key files

### 5. Regulatory Complaint History
- **ID:** `regulatory_complaints`
- **Data Folder:** `research/complaints/data`
- **Description:** State regulatory complaints, consumer complaints, and enforcement actions
- **Priority:** High
- **Structure:** Organized by state subdirectories

### 6. Financial Records
- **ID:** `financial_records`
- **Data Folder:** `research/financial/data`
- **Description:** SEC filings, state business filings, and property value assessments
- **Priority:** Medium
- **Structure:** Flat structure with key files

### 7. News and Media Coverage
- **ID:** `news_coverage`
- **Data Folder:** `research/news/data`
- **Description:** News articles about violations, legal proceedings, and media coverage
- **Priority:** Medium
- **Structure:** Flat structure with key files

### 8. Fair Housing Records
- **ID:** `fair_housing`
- **Data Folder:** `research/discrimination/data`
- **Description:** HUD complaints, EEOC records, and state discrimination complaints
- **Priority:** Medium
- **Structure:** Flat structure with state-specific files

### 9. Professional Memberships
- **ID:** `professional_memberships`
- **Data Folder:** `research/memberships/data`
- **Description:** Real estate and property management association memberships
- **Priority:** Low
- **Structure:** Flat structure with key files

### 10. Social Media and Online Presence
- **ID:** `social_media`
- **Data Folder:** `research/social_media/data`
- **Description:** Company websites, LinkedIn profiles, and online reviews
- **Priority:** Low
- **Structure:** Flat structure with key files

## Data Folder Structure

All searches follow a standardized structure:

```
research/
├── {search_id}/
│   ├── data/              # All search data files
│   │   ├── {subdirectories}/  # State/type subdirectories (if applicable)
│   │   └── *.json         # Data files
│   └── README.md          # Search-specific documentation (optional)
```

### Examples

**License Searches (with state subdirectories):**
```
research/license_searches/data/
├── virginia/
│   └── *.json
├── maryland/
│   └── *.json
└── bar_licenses/
    └── *.json
```

**Property Contracts (flat structure):**
```
research/contracts/data/
├── property_management_contracts.json
├── service_scope.json
└── property_lists_by_state.json
```

## Completion Criteria

Each search is considered complete (returns 1) when:

1. **Required folders exist** - All specified data folders are present
2. **Required files exist** - All specified required files are present
3. **File patterns match** - File patterns match expected files
4. **Minimum file count** - Meets minimum file count threshold (if specified)
5. **Required states** - All required state subdirectories exist (if applicable)

## Usage Examples

### Check Completion Status

```python
from scripts.research.check_search_completion import check_search_completion

# Check if license searches are complete
status = check_search_completion('license_searches')
# Returns: 1 (complete) or 0 (incomplete)

# Get all completion statuses
from scripts.research.check_search_completion import get_all_completion_status
all_statuses = get_all_completion_status()
# Returns: {'license_searches': 1, 'company_registrations': 0, ...}
```

### Generate Consolidation View

```bash
# Generate/update consolidation view
python3.14 scripts/research/generate_consolidation_view.py
```

### Validate Data Folders

```python
from scripts.research.check_search_completion import validate_data_folders

validation = validate_data_folders()
# Returns: {'valid': True/False, 'folders': {...}, 'errors': [...]}
```

## Integration with Progress Tracking

The research outline system integrates with the existing progress tracking:

- `outputs/reports/progress_data.json` - Overall progress tracking
- `research/RESEARCH_OUTLINE.json` - Search definitions
- `research/CONSOLIDATION_VIEW.json` - Consolidated view

## Related Documentation

- [Research README](README.md) - Research directory guide
- [Research Index](RESEARCH_INDEX.json) - File index
- [Reports](REPORTS.md) - Research reports

---

**Last Updated:** 2025-12-10
**Version:** 1.0.0
