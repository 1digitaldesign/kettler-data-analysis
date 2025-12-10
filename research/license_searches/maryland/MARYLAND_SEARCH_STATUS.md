# Maryland DLLR License Search - Current Status

**Date:** December 7, 2025
**Last Updated:** After completing NJ/NY searches
**Progress:** 1/15 complete (6.7%)

---

## Completed Searches

### ✅ Edward Hyland
- **Status:** Complete
- **Result:** ❌ NO LICENSE FOUND
- **Date Completed:** December 7, 2025
- **Findings:** Found 2 other "Hyland" licenses (Kristina L Hyland, William H Hyland, Jr) but not Edward
- **Pattern:** Consistent with VA, DC, NJ findings - unlicensed in all states searched

---

## In Progress / Waiting

### 🔄 Robert Kettler
- **Status:** Form filled, waiting for CAPTCHA completion
- **Last Name:** Kettler
- **First Name:** Robert
- **Priority:** HIGH
- **Action Required:** Manual CAPTCHA completion needed
- **Browser State:** Form ready, CAPTCHA waiting

---

## Pending Searches

### High Priority (1)

#### Caitlin Skidmore
- **Status:** Pending
- **Priority:** HIGH
- **Reason:** Only licensed employee (DC), critical to verify MD status
- **Expected Result:** Likely unlicensed (pattern suggests DC-only licensing)

### Medium Priority (12)

1. **Cindy Fisher** (President)
2. **Luke Davis** (CIO)
3. **Pat Cassada** (CFO)
4. **Sean Curtin** (General Counsel)
5. **Amy Groff** (VP Operations)
6. **Robert Grealy** (SVP Operations)
7. **Djene Moyer** (Community Manager)
8. **Henry Ramos** (Property Manager)
9. **Kristina Thoummarath** (Chief of Staff)
10. **Christina Chang** (Head of Asset Management)
11. **Todd Bowen** (SVP Strategic Services)
12. **Jeffrey Williams** (VP Human Resources)

---

## CAPTCHA Handling Strategy

### Current Approach: Manual CAPTCHA
- **Status:** Active
- **Method:** User manually completes CAPTCHA for each search
- **Time per search:** ~2-3 minutes
- **Success Rate:** 100% (Edward Hyland completed successfully)

### Alternative Approaches Available

#### Option 1: Continue Manual CAPTCHA
- **Pros:** No cost, reliable
- **Cons:** Time-consuming (13 searches × 3 min = ~39 minutes)
- **Best For:** High-priority searches (Robert Kettler, Caitlin Skidmore)

#### Option 2: CAPTCHA Solving Service
- **Status:** Framework ready
- **Services Available:** 2Captcha, Anti-Captcha, CapSolver
- **Cost:** ~$0.01-0.04 per search (~$0.13-0.52 for 13 searches)
- **Best For:** Medium-priority bulk searches

#### Option 3: Direct Commission Request
- **Status:** Contact info documented
- **Method:** Request bulk data directly from Maryland DLLR
- **Best For:** Long-term comprehensive data needs

---

## Search Process

### Step-by-Step Process

1. Navigate to: `https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name`
2. Fill form:
   - Last Name: [Employee Last Name]
   - First Name: [Employee First Name]
3. Complete CAPTCHA (manual or service)
4. Click "Search" button
5. Evaluate results:
   - Check for exact name match
   - Verify license type (Real Estate)
   - Document findings

### Expected Results Pattern

Based on findings from other states:
- **Caitlin Skidmore:** Likely unlicensed (licensed only in DC)
- **All other employees:** Likely unlicensed (consistent pattern across VA, DC, NJ, NY)

---

## Key Findings So Far

### Pattern Confirmed
- **Edward Hyland:** Unlicensed in VA, DC, NJ, MD (4/4 states)
- **Consistent Pattern:** All employees unlicensed except Caitlin Skidmore (DC only)

### Other Findings
- Found 2 unrelated "Hyland" licenses in MD database
- Maryland DLLR database appears comprehensive and searchable

---

## Next Actions

### Immediate (High Priority)
1. ✅ Complete CAPTCHA for Robert Kettler search (waiting)
2. ⏳ Search Caitlin Skidmore (high priority)

### Short-term (Medium Priority)
3. ⏳ Complete remaining 12 employee searches
4. ⏳ Document all findings in JSON format
5. ⏳ Update comprehensive violation reports

### Long-term
6. ⏳ Consider CAPTCHA service for bulk searches
7. ⏳ File administrative complaints with Maryland DLLR

---

## Files Created

- `maryland_hyland_search_results.json` - Edward Hyland findings
- `maryland_search_framework.json` - Search framework and employee list
- `MARYLAND_PROGRESS.md` - Progress tracking
- `MARYLAND_SEARCH_STATUS.md` - This file

---

## Notes

- Browser automation working but requires manual CAPTCHA intervention
- Form interaction is reliable once CAPTCHA is completed
- Search results are clear and easy to evaluate
- Pattern consistent with other states (unlicensed operations)
