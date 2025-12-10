# Connecticut DCP License Search - Current Status

**Date:** December 7, 2025
**Progress:** 2/15 attempted (13.3%)

---

## Search Information

**URL:** https://www.elicense.ct.gov/lookup/licenselookup.aspx
**Regulatory Agency:** Connecticut Department of Consumer Protection (DCP)
**Method:** Playwright browser automation

---

## Correct License Types Identified

- **REAL ESTATE BROKER**
- **REAL ESTATE SALESPERSON**
- **REAL ESTATE TEAM**

---

## Completed Searches

### ✅ Edward Hyland
- **Status:** Search executed
- **License Type:** Not specified in initial search
- **Result:** Pending evaluation
- **Note:** Initial search completed, results need verification

### ✅ Robert Kettler
- **Status:** Search executed
- **License Type:** REAL ESTATE BROKER
- **Result:** Pending evaluation
- **Note:** Search completed with correct license type

---

## Pending Searches (13 employees)

### High Priority
1. **Caitlin Skidmore** - Only licensed employee (DC), critical to verify CT status

### Medium Priority
2. **Cindy Fisher** (President)
3. **Luke Davis** (CIO)
4. **Pat Cassada** (CFO)
5. **Sean Curtin** (General Counsel)
6. **Amy Groff** (VP Operations)
7. **Robert Grealy** (SVP Operations)
8. **Djene Moyer** (Community Manager)
9. **Henry Ramos** (Property Manager)
10. **Kristina Thoummarath** (Chief of Staff)
11. **Christina Chang** (Head of Asset Management)
12. **Todd Bowen** (SVP Strategic Services)
13. **Jeffrey Williams** (VP Human Resources)

---

## Search Process

### Step-by-Step Process

1. Navigate to: `https://www.elicense.ct.gov/lookup/licenselookup.aspx`
2. Select license type:
   - For brokers/managers: **REAL ESTATE BROKER**
   - For salespersons/staff: **REAL ESTATE SALESPERSON**
3. Enter name:
   - Last Name: [Employee Last Name]
   - First Name: [Employee First Name]
4. Click "Search"
5. Evaluate results:
   - Check for exact name match
   - Verify license type
   - Document findings

### License Type Selection Guide

**REAL ESTATE BROKER:**
- Robert Kettler (CEO)
- Caitlin Skidmore (Principal Broker)
- Cindy Fisher (President)
- Pat Cassada (CFO)
- Luke Davis (CIO)
- Sean Curtin (General Counsel)
- Robert Grealy (SVP Operations)
- Todd Bowen (SVP Strategic Services)

**REAL ESTATE SALESPERSON:**
- Edward Hyland (Senior Regional Manager)
- Amy Groff (VP Operations)
- Djene Moyer (Community Manager)
- Henry Ramos (Property Manager)
- Kristina Thoummarath (Chief of Staff)
- Christina Chang (Head of Asset Management)
- Jeffrey Williams (VP Human Resources)

---

## Expected Results Pattern

Based on findings from other states:
- **Caitlin Skidmore:** Likely unlicensed (licensed only in DC)
- **All other employees:** Likely unlicensed (consistent pattern across VA, DC, NJ, NY)

---

## Issues Encountered

### Form Interaction Issues
- Initial searches encountered form interaction problems
- Correct license types identified: REAL ESTATE BROKER, REAL ESTATE SALESPERSON
- Robert Kettler search completed successfully with correct license type

### Next Steps
- Continue with remaining 13 employees
- Use appropriate license type for each employee
- Document all findings in JSON format

---

## Files Created

- `connecticut_batch1_results.json` - Edward Hyland search
- `connecticut_batch2_results.json` - Robert Kettler search
- `CONNECTICUT_SEARCH_STATUS.md` - This file

---

## Notes

- Form interaction issues resolved by identifying correct license types
- Search process working with proper license type selection
- Pattern consistent with other states (unlicensed operations expected)
