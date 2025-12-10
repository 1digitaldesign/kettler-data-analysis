# Data Collection Scripts

![Status](https://img.shields.io/badge/status-active-green)
![Progress](https://img.shields.io/badge/progress-48%25-yellow)

Complete suite of data collection scripts with progress tracking.

---

## Progress Tracking Tools

### Quick Status

```bash
python3.14 scripts/data_collection/progress_guided_workflow.py --quick
```

Shows quick status with progress bars for high-priority categories.

### Comprehensive Report

```bash
python3.14 scripts/data_collection/final_progress_report.py
```

Complete progress report with all categories, statistics, and next actions.

### Live Dashboard

```bash
python3.14 scripts/data_collection/live_progress.py
```

Detailed live dashboard with file-by-file tracking.

### Full Dashboard

```bash
python3.14 scripts/data_collection/show_progress.py
```

Full dashboard showing all 10 categories with status indicators.

### Interactive Workflow

```bash
python3.14 scripts/data_collection/progress_guided_workflow.py --interactive
```

Interactive menu-driven workflow with progress tracking.

---

## Data Collection Scripts

### License Searches

```bash
python3.14 scripts/data_collection/complete_license_searches.py
```

Lists remaining license searches and creates templates.

### Company Registrations

```bash
python3.14 scripts/data_collection/start_company_searches.py
python3.14 scripts/data_collection/collect_company_registrations.py
```

View search queue and collect registration data.

### Employee Roles

```bash
python3.14 scripts/data_collection/collect_employee_roles.py
```

Create employee roles documentation.

### Other Categories

- `collect_property_contracts.py` - Property management contracts
- `collect_regulatory_complaints.py` - Regulatory complaints
- `collect_financial_records.py` - Financial records
- `collect_news_coverage.py` - News and media coverage
- `collect_fair_housing.py` - Fair housing records
- `collect_professional_memberships.py` - Professional memberships
- `collect_social_media.py` - Social media and online presence

---

## Progress Update

```bash
python3.14 scripts/data_collection/update_progress.py
```

Automatically updates the progress tracker markdown file.

---

## Current Status

**Overall Progress:** 48% (28/58 tasks)

- ✅ License Searches: 93% (14/15 states, 260 files)
- ✅ Employee Roles: 100% (2/2 files)
- ⚠️ Company Registrations: 0% (12 templates ready)
- ⚠️ Other Categories: Templates ready for data collection

---

## Usage Examples

### View Current Progress

```bash
# Quick status
python3.14 scripts/data_collection/progress_guided_workflow.py --quick

# Full report
python3.14 scripts/data_collection/final_progress_report.py
```

### Start Data Collection

```bash
# View company registration queue
python3.14 scripts/data_collection/start_company_searches.py

# Check license search status
python3.14 scripts/data_collection/complete_license_searches.py
```

### Update Progress

```bash
# Auto-update progress tracker
python3.14 scripts/data_collection/update_progress.py
```

---

**Last Updated:** 2025-12-10
