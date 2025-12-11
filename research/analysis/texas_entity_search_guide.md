# Texas Entity Search Guide

**Date:** December 11, 2025
**Purpose:** Search Texas business entity database for Kettler and Lariat-related entities

## Entities to Search in Texas

Based on research findings, search for the following entities:

### 1. **Lariat Companies** (HIGH PRIORITY)
- **Also known as:** Lariat Realty Advisors
- **Known Address:** 2591 Dallas Parkway, Suite 300, Frisco, TX 75034
- **Reason:** Lariat is affiliated with Kettler operations and has Texas presence
- **Search Terms:**
  - "Lariat Companies"
  - "Lariat Realty Advisors"
  - "Lariat"
  - Entity ID if available

### 2. **Kettler Management Inc** (HIGH PRIORITY)
- **Legal Name:** KETTLER MANAGEMENT INC.
- **Fictitious Name:** Kettler Management Corp.
- **Reason:** Verify if Kettler is registered/qualified as foreign entity in Texas
- **Search Terms:**
  - "Kettler Management Inc"
  - "Kettler Management"
  - "KETTLER MANAGEMENT INC"

### 3. **Frisco Address Cluster Entities** (MEDIUM PRIORITY)
Search for entities registered at these Frisco, TX addresses:

**Address 1:** 5729 Lebanon Rd Suite 144553, Frisco, TX 75034
- **Known Entities at this address:**
  - Multiple Virginia-licensed firms use this address
  - Caitlin Skidmore's license addresses
  - Shell company pattern identified

**Address 2:** 2591 Dallas Parkway, Suite 300, Frisco, TX 75034
- **Known Entity:** Lariat Realty Advisors

**Search Method:** Search by registered agent address or business address

### 4. **Related Entities** (MEDIUM PRIORITY)
Based on Lariat-affiliated companies investigation:
- **BAINBRIDGE MID-ATLANTIC MANAGEMENT LLC**
- **CAPREIT Residential Management, LLC**
- **BOZZUTO MANAGEMENT COMPANY**
- **GABLES RESIDENTIAL SERVICES, INC.**

## Texas Secretary of State Search

**URL:** https://www.sos.texas.gov/corp/sosda/index.shtml

**Alternative URLs:**
- https://mycpa.cpa.state.tx.us/coa/
- https://www.sos.texas.gov/corp/forms_boc.shtml

## Search Instructions

### Step 1: Search for Lariat Companies
1. Navigate to Texas SOS business entity search
2. Search for: **"Lariat"**
3. Review all results
4. Record:
   - Entity name
   - Entity type
   - Entity ID/File Number
   - Formation date
   - Status
   - Registered agent
   - Business address
   - Officers/Directors (if available)

### Step 2: Search for Kettler Management
1. Search for: **"Kettler Management"**
2. Try variations:
   - "Kettler Management Inc"
   - "KETTLER MANAGEMENT INC"
   - "Kettler Management Corp"
3. Record all findings

### Step 3: Search by Address
1. Search for entities at: **"5729 Lebanon Rd"** or **"Frisco"**
2. Search for entities at: **"2591 Dallas Parkway"** or **"Dallas Parkway Frisco"**
3. Record all entities found at these addresses

### Step 4: Search Related Entities
1. Search for each related entity:
   - "Bainbridge Mid-Atlantic"
   - "CAPREIT"
   - "Bozzuto"
   - "Gables Residential"
2. Record findings

## Data to Record

For each entity found, record:

```json
{
  "entity_name": "",
  "entity_type": "",
  "entity_id": "",
  "file_number": "",
  "formation_date": "",
  "status": "",
  "registered_agent": {
    "name": "",
    "address": ""
  },
  "business_address": "",
  "officers": [],
  "directors": [],
  "filing_history": [],
  "notes": ""
}
```

## Save Results To

Create file: `research/company_registrations/data/texas/texas_entity_search_results.json`

Format:
```json
{
  "metadata": {
    "date": "2025-12-11",
    "state": "Texas",
    "search_url": "https://www.sos.texas.gov/corp/sosda/index.shtml",
    "search_method": "Manual search"
  },
  "lariat_entities": [],
  "kettler_entities": [],
  "frisco_address_entities": [],
  "related_entities": [],
  "summary": {
    "total_entities_found": 0,
    "lariat_found": false,
    "kettler_found": false,
    "frisco_address_cluster_found": false
  }
}
```

## Key Questions to Answer

1. **Is Lariat Companies registered in Texas?**
   - If yes, what is the entity structure?
   - What is the relationship to Kettler?

2. **Is Kettler Management Inc registered/qualified in Texas?**
   - If yes, is it as foreign entity or domestic?
   - What is the registration status?

3. **What entities are registered at the Frisco addresses?**
   - Who owns/controls these addresses?
   - Are they shell companies?

4. **Are the Lariat-affiliated companies registered in Texas?**
   - What is their relationship to Lariat?
   - What is their relationship to Kettler?

## Expected Findings

Based on research:
- **Lariat Realty Advisors** likely registered in Texas (has Frisco address)
- **Frisco address cluster** may reveal shell company structure
- **Kettler Management** may or may not be registered (check foreign qualification)

## Notes

- Texas SOS database may require CAPTCHA
- Some searches may return many results - review all
- Address searches may reveal unexpected connections
- Cross-reference findings with Virginia and other state registrations
