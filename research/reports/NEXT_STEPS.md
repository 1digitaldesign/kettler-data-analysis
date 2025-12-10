# Next Steps for Data Collection

![Priority](https://img.shields.io/badge/priority-high-red)
![Status](https://img.shields.io/badge/status-ready-blue)

Immediate actionable steps to continue data collection.

---

## Immediate Actions (This Week)

### 1. Complete License Searches ⚠️ HIGH PRIORITY

**Status:** 88% complete (13/15 states)

**Remaining Work:**

#### Maryland (1/15 employees - 7%)
- [ ] Complete 14 remaining employee searches
- [ ] CAPTCHA issues resolved, ready to proceed
- [ ] Use browser automation or manual search
- **Estimated:** 1 day

#### Connecticut (0/15 employees - 0%)
- [ ] Complete all 15 employee searches
- [ ] Use browser automation framework
- **Estimated:** 1 day

**Tools Available:**
- `scripts/data_collection/complete_license_searches.py` - Generates search list and templates
- Browser automation framework in `research/browser_automation/`

**Files Created:** Search templates will be created automatically

---

### 2. Start Company Registration Searches ⚠️ HIGH PRIORITY

**Status:** Not started

**Tasks:**
- [ ] Search Kettler Management Inc. in all operational states
- [ ] Verify business registration status
- [ ] Document registered agents and addresses
- [ ] Cross-reference with license addresses

**States to Search:**
1. District of Columbia - https://corponline.dccorporations.gov/
2. Maryland - https://egov.maryland.gov/BusinessExpress/EntitySearch
3. Virginia - https://cis.scc.virginia.gov/EntitySearch/Index
4. New Jersey - https://www.njportal.com/DOR/BusinessNameSearch/
5. New York - https://apps.dos.ny.gov/publicInquiry/
6. Connecticut - https://www.concord-sots.ct.gov/CONCORD/PublicInquiry

**Tools Available:**
- `scripts/data_collection/start_company_registrations.py` - Creates search templates
- Templates created in `research/company_registrations/{state}/`

**Estimated:** 1-2 days

---

### 3. Document Employee Roles ⚠️ HIGH PRIORITY

**Status:** 30% complete (employees identified, roles need documentation)

**Tasks:**
- [ ] Create job description templates for all 15 employees
- [ ] Document organizational structure
- [ ] Verify who performs licensed activities
- [ ] Document supervision structure

**Data Needed:**
- Job descriptions (if publicly available)
- LinkedIn profiles for role verification
- Company website organizational information

**Files:** `research/employees/employee_roles.json`, `research/employees/organizational_chart.json`

**Estimated:** 1-2 days

---

## Short-term Actions (Next 2 Weeks)

### 4. Collect Property Management Contracts

**Tasks:**
- [ ] Identify properties under management
- [ ] Request sample contracts (if publicly available)
- [ ] Document service scope and geographic distribution
- [ ] Verify licensing requirements in contracts

**Sources:**
- Property listings
- Company website
- Public property records

**Estimated:** 3-5 days

---

### 5. Search Regulatory Complaints

**Tasks:**
- [ ] Search state regulatory agency databases
- [ ] Check Better Business Bureau
- [ ] Search for enforcement actions
- [ ] Document any settlements or penalties

**States:** DC, MD, VA, NJ, NY, CT

**Estimated:** 2-3 days

---

## Tools and Scripts

### Available Scripts

1. **`scripts/data_collection/complete_license_searches.py`**
   - Lists remaining license searches
   - Creates search templates
   - Generates search checklist

2. **`scripts/data_collection/collect_company_registrations.py`**
   - Creates company registration templates
   - Provides state-specific SOS URLs
   - Generates search checklist

3. **`scripts/data_collection/collect_employee_roles.py`**
   - Creates employee roles documentation
   - Generates organizational chart
   - Documents licensed activity assignments

4. **`scripts/data_collection/collect_property_contracts.py`**
   - Creates property management contract template
   - Provides search instructions
   - Documents service scope structure

5. **`scripts/data_collection/collect_regulatory_complaints.py`**
   - Creates regulatory complaint template
   - Provides state agency URLs
   - Generates search instructions

6. **`scripts/data_collection/collect_fair_housing.py`**
   - Creates HUD and EEOC templates
   - Provides state discrimination agency info
   - Generates search instructions

7. **`scripts/data_collection/collect_news_coverage.py`**
   - Creates news coverage templates
   - Lists 8 news sources with URLs
   - Provides search terms

8. **`scripts/data_collection/update_progress.py`**
   - Automatically updates progress bars
   - Counts completed files
   - Updates status indicators

### Usage

```bash
# Check remaining license searches
python3.14 scripts/data_collection/complete_license_searches.py

# Start company registration searches
python3.14 scripts/data_collection/start_company_registrations.py

# Update progress tracking
python3.14 scripts/data_collection/update_progress.py
```

---

## Progress Tracking

**Track your progress:**
- [DATA_COLLECTION_PROGRESS.md](DATA_COLLECTION_PROGRESS.md) - Real-time progress with bars
- [DATA_COLLECTION_TODOS.md](DATA_COLLECTION_TODOS.md) - Detailed task descriptions

**Update progress:**
- Run `scripts/data_collection/update_progress.py` after completing tasks
- Manually update checkboxes in `DATA_COLLECTION_PROGRESS.md`
- Commit progress updates regularly

---

## Related Documentation

- [Data Collection Progress](DATA_COLLECTION_PROGRESS.md) - Progress tracker
- [Data Collection Todos](DATA_COLLECTION_TODOS.md) - Complete task list
- [Investigation Summary](../license_searches/reports/INVESTIGATION_SUMMARY.md) - Investigation overview

---

**Last Updated:** 2025-12-10
**Next Review:** After completing Maryland and Connecticut searches
