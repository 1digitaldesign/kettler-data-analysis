# Company Registration Search Guide

**Date:** December 11, 2025
**Purpose:** Manual searches for company registrations in 6 states (DC, MD, VA, NJ, NY, CT)

## Companies to Search

For each state, search for:
1. **Kettler Management Inc** (or variations)
2. **Kettler Management** (without "Inc")
3. **Lariat Companies** (or Lariat-related entities)
4. Any other Kettler-related entities found

## Search Instructions by State

### 1. Virginia
**URL:** https://cis.scc.virginia.gov/EntitySearch/Index

**Steps:**
1. Navigate to the URL
2. Select search type: **"Contain"** from dropdown
3. Enter in "Entity Name" field: **"Kettler Management"**
4. Complete CAPTCHA if required
5. Click **"Search"** button
6. Record all results found
7. Repeat for "Kettler Management Inc" (exact match)
8. Repeat for "Lariat"

**Data to Record:**
- Entity Name
- Entity Type (Corporation, LLC, etc.)
- Entity ID/Number
- Formation Date
- Status (Active, Inactive, etc.)
- Registered Agent
- Business Address
- Filing Number

**Save to:** `research/company_registrations/data/virginia/virginia_kettler_management_inc_registration.json`

---

### 2. Maryland
**URL:** https://egov.maryland.gov/BusinessExpress/EntitySearch

**Steps:**
1. Navigate to the URL
2. Search for: **"Kettler Management"**
3. Complete CAPTCHA if required
4. Review results
5. Repeat for "Kettler Management Inc" and "Lariat"

**Data to Record:** Same as Virginia

**Save to:** `research/company_registrations/data/maryland/maryland_kettler_management_inc_registration.json`

---

### 3. District of Columbia (DC)
**URL:** https://corponline.dccorp.dc.gov/

**Steps:**
1. Navigate to the URL
2. Use entity search function
3. Search for: **"Kettler Management"**
4. Complete CAPTCHA if required
5. Review results
6. Repeat for variations

**Data to Record:** Same as Virginia

**Save to:** `research/company_registrations/data/dc/kettler_management_inc_registration.json`

---

### 4. New Jersey
**URL:** https://www.njportal.com/DOR/BusinessNameSearch/

**Steps:**
1. Navigate to the URL
2. Search for: **"Kettler Management"**
3. Complete CAPTCHA if required
4. Review results
5. Repeat for variations

**Data to Record:** Same as Virginia

**Save to:** `research/company_registrations/data/new_jersey/new_jersey_kettler_management_inc_registration.json`

---

### 5. New York
**URL:** https://appext20.dos.ny.gov/corp_public/corpsearch.entity_search_entry

**Steps:**
1. Navigate to the URL
2. Search for: **"Kettler Management"**
3. Complete CAPTCHA if required
4. Review results
5. Repeat for variations

**Data to Record:** Same as Virginia

**Save to:** `research/company_registrations/data/new_york/new_york_kettler_management_inc_registration.json`

---

### 6. Connecticut
**URL:** https://www.concord-sots.ct.gov/CONCORD/PublicInquiry

**Steps:**
1. Navigate to the URL
2. Search for: **"Kettler Management"**
3. Complete CAPTCHA if required
4. Review results
5. Repeat for variations

**Data to Record:** Same as Virginia

**Save to:** `research/company_registrations/data/connecticut/connecticut_kettler_management_inc_registration.json`

---

## JSON Format Template

Use this format when saving results:

```json
{
  "metadata": {
    "date": "2025-12-11T00:00:00",
    "state": "Virginia",
    "company": "Kettler Management Inc.",
    "search_url": "https://cis.scc.virginia.gov/EntitySearch/Index",
    "search_method": "Manual search with CAPTCHA"
  },
  "findings": {
    "registered": true,
    "entity_type": "Stock Corporation",
    "entity_id": "S12345678",
    "formation_date": "2000-01-15",
    "registered_agent": "Name and Address",
    "business_address": "Full Address",
    "status": "Active",
    "filing_number": "F123456"
  },
  "additional_entities_found": [
    {
      "name": "Other Kettler Entity",
      "entity_type": "LLC",
      "status": "Active"
    }
  ],
  "conclusion": "Kettler Management Inc is registered in [State] as a [Entity Type], status: [Status]"
}
```

## Notes

- If no results found, set `"registered": false` and `"conclusion": "No registration found for Kettler Management Inc in [State]"`
- Record ALL entities found, not just exact matches
- Take screenshots if helpful for documentation
- Some states may have multiple entities - record all of them
