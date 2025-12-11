# CAPTCHA-Protected Search Guide

**Date:** December 11, 2025
**Purpose:** Guide for completing manual searches that require CAPTCHA interaction

## Company Registrations (HIGH PRIORITY)

### Virginia - Kettler Management Inc
- **URL:** https://cis.scc.virginia.gov/EntitySearch/Index
- **Status:** ✅ Form filled - "Kettler Management" entered, Search clicked
- **Action Needed:** Complete CAPTCHA, then review results
- **Search Terms to Try:**
  - "Kettler Management" (Contain)
  - "Kettler Management Inc" (Exact Match)
  - "Lariat" (Contain)
- **File to Update:** `research/company_registrations/data/virginia/virginia_kettler_management_inc_registration.json`

### Maryland - Kettler Management Inc
- **URL:** https://egov.maryland.gov/BusinessExpress/EntitySearch
- **Search Terms:**
  - "Kettler Management"
  - "Kettler Management Inc"
  - "Lariat"
- **File to Update:** `research/company_registrations/data/maryland/maryland_kettler_management_inc_registration.json`

### District of Columbia - Kettler Management Inc
- **URL:** https://corponline.dccorp.dc.gov/
- **Search Terms:**
  - "Kettler Management"
  - "Kettler Management Inc"
  - "Lariat"
- **File to Update:** `research/company_registrations/data/dc/kettler_management_inc_registration.json`

### New Jersey - Kettler Management Inc
- **URL:** https://www.njportal.com/DOR/BusinessNameSearch/
- **Search Terms:**
  - "Kettler Management"
  - "Kettler Management Inc"
  - "Lariat"
- **File to Update:** `research/company_registrations/data/new_jersey/new_jersey_kettler_management_inc_registration.json`

### New York - Kettler Management Inc
- **URL:** https://appext20.dos.ny.gov/corp_public/corpsearch.entity_search_entry
- **Search Terms:**
  - "Kettler Management"
  - "Kettler Management Inc"
  - "Lariat"
- **File to Update:** `research/company_registrations/data/new_york/new_york_kettler_management_inc_registration.json`

### Connecticut - Kettler Management Inc
- **URL:** https://www.concord-sots.ct.gov/CONCORD/PublicInquiry
- **Search Terms:**
  - "Kettler Management"
  - "Kettler Management Inc"
  - "Lariat"
- **File to Update:** `research/company_registrations/data/connecticut/connecticut_kettler_management_inc_registration.json`

## Regulatory Complaint History (HIGH PRIORITY)

### Better Business Bureau (BBB)
- **URL:** https://www.bbb.org
- **Action Needed:** Accept cookies, then search for:
  - "Kettler Management"
  - "Kettler Management Inc"
  - "Kettler Companies"
- **File to Update:** `research/complaints/data/bbb_complaints.json`

### Virginia Regulatory Complaints
- **URL:** https://www.dpor.virginia.gov/Boards/RealEstateBoard/
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/complaints/data/va/regulatory_complaints.json`

### Maryland Regulatory Complaints
- **URL:** https://www.dllr.state.md.us/license/rec/recsearch.shtml
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/complaints/data/md/regulatory_complaints.json`

### District of Columbia Regulatory Complaints
- **URL:** https://dcra.dc.gov/
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/complaints/data/dc/regulatory_complaints.json`

### New Jersey Regulatory Complaints
- **URL:** https://www.nj.gov/dobi/division_cons/realestate.shtml
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/complaints/data/nj/regulatory_complaints.json`

### New York Regulatory Complaints
- **URL:** https://www.dos.ny.gov/licensing/
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/complaints/data/ny/regulatory_complaints.json`

### Connecticut Regulatory Complaints
- **URL:** https://www.ct.gov/dcp/cwp/view.asp?a=1621&q=274200
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/complaints/data/ct/regulatory_complaints.json`

## Fair Housing Records (MEDIUM PRIORITY)

### HUD Complaints
- **URL:** https://www.hud.gov/program_offices/fair_housing_equal_opp/online-complaint
- **Note:** May require account creation or direct database access
- **File to Update:** `research/discrimination/data/hud_complaints.json`

### EEOC Records
- **URL:** https://www.eeoc.gov/
- **Search Terms:**
  - "Kettler Management"
  - "Kettler"
- **File to Update:** `research/discrimination/data/eeoc_records.json`

### State Discrimination Complaints
- **DC:** https://ohr.dc.gov/
- **MD:** https://mccr.maryland.gov/
- **VA:** https://www.dpor.virginia.gov/
- **NJ:** https://www.nj.gov/oag/dcr/
- **NY:** https://dhr.ny.gov/
- **CT:** https://portal.ct.gov/DAS/Equal-Opportunity-Diversity-Management
- **Files to Update:** `research/discrimination/data/{state}_discrimination_complaints.json`

## Data Format for Results

When updating JSON files, use this structure:

```json
{
  "metadata": {
    "date": "2025-12-11",
    "state": "Virginia",
    "company": "Kettler Management Inc",
    "search_url": "https://...",
    "search_method": "Manual browser search with CAPTCHA"
  },
  "findings": {
    "registered": true/false,
    "entity_type": "Corporation/LLC/etc",
    "formation_date": "YYYY-MM-DD",
    "registered_agent": "Name",
    "business_address": "Address",
    "status": "Active/Inactive",
    "entity_id": "ID Number"
  },
  "conclusion": "Summary of findings"
}
```

## Progress Tracking

- [ ] Virginia Company Registration
- [ ] Maryland Company Registration
- [ ] DC Company Registration
- [ ] New Jersey Company Registration
- [ ] New York Company Registration
- [ ] Connecticut Company Registration
- [ ] BBB Complaints
- [ ] Virginia Regulatory Complaints
- [ ] Maryland Regulatory Complaints
- [ ] DC Regulatory Complaints
- [ ] New Jersey Regulatory Complaints
- [ ] New York Regulatory Complaints
- [ ] Connecticut Regulatory Complaints
- [ ] HUD Complaints
- [ ] EEOC Records
- [ ] State Discrimination Complaints (6 states)

## Notes

- Many state databases use reCAPTCHA v2 or v3
- Some sites require cookie acceptance first
- Results may take a few seconds to load after CAPTCHA completion
- If no results found, document "No registrations/complaints found" in the findings
- Take screenshots if helpful for documentation
