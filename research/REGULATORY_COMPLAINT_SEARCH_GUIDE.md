# Regulatory Complaint Search Guide

**Date:** December 11, 2025
**Purpose:** Manual searches for regulatory complaints in BBB and 6 states (DC, MD, VA, NJ, NY, CT)

## Entities to Search

Search for complaints against:
1. **Kettler Management Inc**
2. **Kettler Management**
3. **Kettler Companies**
4. **Lariat Companies**
5. Related Kettler entities

## Search Instructions

### Better Business Bureau (BBB)
**URL:** https://www.bbb.org

**Steps:**
1. Navigate to https://www.bbb.org
2. Accept cookies if prompted
3. Use search bar: **"Kettler Management"**
4. Select location filters if needed (DC, MD, VA, etc.)
5. Review company profiles and complaint history
6. Record all complaints found

**Data to Record:**
- Company name
- BBB rating
- Number of complaints
- Complaint details (dates, types, resolutions)
- Customer reviews
- BBB profile URL

**Save to:** `research/complaints/data/bbb_complaints.json`

---

### State Regulatory Databases

#### 1. Virginia
**URL:** Search Virginia DPOR complaint database
**Search Terms:** "Kettler Management", "Kettler"

**Steps:**
1. Navigate to Virginia DPOR website
2. Access complaint/disciplinary action database
3. Search for "Kettler Management"
4. Complete CAPTCHA if required
5. Record all complaints/violations found

**Save to:** `research/complaints/data/va/regulatory_complaints.json`

---

#### 2. Maryland
**URL:** Maryland DLLR complaint database
**Search Terms:** "Kettler Management", "Kettler"

**Steps:**
1. Navigate to Maryland DLLR website
2. Access complaint database
3. Search for "Kettler Management"
4. Complete CAPTCHA if required
5. Record all complaints/violations found

**Save to:** `research/complaints/data/md/regulatory_complaints.json`

---

#### 3. District of Columbia (DC)
**URL:** DCRA complaint database
**Search Terms:** "Kettler Management", "Kettler"

**Steps:**
1. Navigate to DCRA website
2. Access complaint database
3. Search for "Kettler Management"
4. Complete CAPTCHA if required
5. Record all complaints/violations found

**Save to:** `research/complaints/data/dc/regulatory_complaints.json`

---

#### 4. New Jersey
**URL:** New Jersey Division of Consumer Affairs
**Search Terms:** "Kettler Management", "Kettler"

**Steps:**
1. Navigate to NJ consumer affairs website
2. Access complaint database
3. Search for "Kettler Management"
4. Complete CAPTCHA if required
5. Record all complaints/violations found

**Save to:** `research/complaints/data/nj/regulatory_complaints.json`

---

#### 5. New York
**URL:** New York Department of State or AG complaint database
**Search Terms:** "Kettler Management", "Kettler"

**Steps:**
1. Navigate to NY regulatory website
2. Access complaint database
3. Search for "Kettler Management"
4. Complete CAPTCHA if required
5. Record all complaints/violations found

**Save to:** `research/complaints/data/ny/regulatory_complaints.json`

---

#### 6. Connecticut
**URL:** Connecticut DCP complaint database
**Search Terms:** "Kettler Management", "Kettler"

**Steps:**
1. Navigate to Connecticut DCP website
2. Access complaint database
3. Search for "Kettler Management"
4. Complete CAPTCHA if required
5. Record all complaints/violations found

**Save to:** `research/complaints/data/ct/regulatory_complaints.json`

---

## JSON Format Template

### BBB Complaints Format:
```json
{
  "metadata": {
    "date": "2025-12-11T00:00:00",
    "source": "Better Business Bureau",
    "search_method": "Manual search"
  },
  "companies_found": [
    {
      "name": "Kettler Management Inc",
      "bbb_rating": "A+",
      "bbb_profile_url": "https://...",
      "location": "McLean, VA",
      "complaints": [
        {
          "date": "2024-01-15",
          "type": "Service Issue",
          "status": "Resolved",
          "description": "Brief description"
        }
      ],
      "reviews": {
        "total": 10,
        "average_rating": 4.5
      }
    }
  ],
  "complaints": []
}
```

### State Regulatory Complaints Format:
```json
{
  "metadata": {
    "date": "2025-12-11T00:00:00",
    "state": "Virginia",
    "source": "Virginia DPOR",
    "search_method": "Manual search with CAPTCHA"
  },
  "complaints": [
    {
      "case_number": "CASE-12345",
      "date_filed": "2023-05-10",
      "complainant": "Name (if public)",
      "respondent": "Kettler Management Inc",
      "violation_type": "License violation",
      "status": "Resolved/Pending",
      "resolution": "Description of resolution",
      "penalty": "Fine amount or action taken"
    }
  ],
  "disciplinary_actions": [],
  "summary": "Found X complaints against Kettler entities in [State]"
}
```

## Notes

- If no complaints found, set `"complaints": []` and add note: `"No complaints found"`
- Record case numbers, dates, and status for all complaints
- Some states may have separate databases for different types of complaints (real estate, consumer, etc.)
- Take screenshots of important findings
- Note if complaint databases require registration or have access restrictions
