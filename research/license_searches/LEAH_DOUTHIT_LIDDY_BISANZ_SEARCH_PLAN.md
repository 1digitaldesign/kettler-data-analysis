# Leah Douthit & Liddy Bisanz - Comprehensive License Search Plan

**Date:** December 8, 2025
**Status:** Planning Phase
**Total Searches Required:** 22 searches (2 people × 11 states)

---

## Current Status

### Already Searched
- **Liddy Bisanz:** New Jersey ✅, New York ✅, Maryland ✅ (3 states)
- **Leah Douthit:** Maryland ✅ (1 state)

**Result:** Both unlicensed in all searched states

---

## Remaining States to Search

### Total: 11 States
1. **DC** (District of Columbia)
2. **Virginia**
3. **Connecticut**
4. **Pennsylvania**
5. **North Carolina**
6. **South Carolina**
7. **Georgia**
8. **Florida**
9. **Arizona** (2025 expansion)
10. **New Mexico** (2025 expansion)
11. **Utah** (2025 expansion)

---

## Search Plan - Broken into Smaller Tasks

### Phase 1: DMV Region (Priority 1) - 6 searches
**Rationale:** DMV is Kettler's primary operational area

#### Task 1.1: District of Columbia
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** https://govservices.dcra.dc.gov/oplaportal/Home/GetLicenseSearchDetails
- **Method:** Browser automation (Playwright)
- **Status:** ⏳ Pending
- **Expected:** Unlicensed (consistent with pattern)

#### Task 1.2: Virginia
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** https://www.dpor.virginia.gov/LicenseLookup
- **Method:** Browser automation (may require iframe handling)
- **Status:** ⏳ Pending
- **Expected:** Unlicensed (consistent with pattern)

#### Task 1.3: Connecticut
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** https://www.ct.gov/dcp/
- **Method:** Browser automation
- **Status:** ⏳ Pending
- **Expected:** Unlicensed (consistent with pattern)

---

### Phase 2: Northeast Region (Priority 2) - 2 searches
**Rationale:** Operational state, but lower priority than DMV

#### Task 2.1: Pennsylvania
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (Pennsylvania Real Estate Commission)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Expected:** Unlicensed (consistent with pattern)

---

### Phase 3: Southeast Region (Priority 3) - 8 searches
**Rationale:** Operational states with significant Kettler presence

#### Task 3.1: North Carolina
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (North Carolina Real Estate Commission)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Markets:** Raleigh, Charlotte, Wilmington, Durham, Cary, Chapel Hill, Greensboro

#### Task 3.2: South Carolina
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (South Carolina Real Estate Commission)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Market:** North Charleston

#### Task 3.3: Georgia
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (Georgia Real Estate Commission)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Markets:** Atlanta metro (Canton, Duluth, Lithonia, Stonecrest)

#### Task 3.4: Florida
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (Florida Real Estate Commission)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Markets:** Tampa, Celebration/Orlando, Maitland

---

### Phase 4: Southwest Region (Priority 4) - 6 searches
**Rationale:** 2025 expansion states, lower priority

#### Task 4.1: Arizona
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (Arizona Department of Real Estate)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Note:** Part of 2025 expansion

#### Task 4.2: New Mexico
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (New Mexico Real Estate Commission)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Note:** Part of 2025 expansion

#### Task 4.3: Utah
- **People:** Leah Douthit, Liddy Bisanz
- **Search URL:** TBD (Utah Division of Real Estate)
- **Method:** Browser automation or manual framework
- **Status:** ⏳ Pending
- **Note:** Part of 2025 expansion

---

## Search Execution Strategy

### Automated States (Browser Automation)
- **DC:** ✅ Framework exists (same as core employees)
- **Virginia:** ⚠️ May require iframe handling (known issue)
- **Connecticut:** ✅ Framework exists (same as core employees)
- **New Jersey:** ✅ Already searched
- **New York:** ✅ Already searched
- **Maryland:** ⚠️ CAPTCHA required (manual completion)

### Manual Framework States
- **Pennsylvania:** Need to identify search URL and framework
- **North Carolina:** Need to identify search URL and framework
- **South Carolina:** Need to identify search URL and framework
- **Georgia:** Need to identify search URL and framework
- **Florida:** Need to identify search URL and framework
- **Arizona:** Need to identify search URL and framework
- **New Mexico:** Need to identify search URL and framework
- **Utah:** Need to identify search URL and framework

---

## Expected Results

Based on pattern observed:
- **Liddy Bisanz:** Unlicensed in NJ, NY, MD
- **Leah Douthit:** Unlicensed in MD

**Expected:** Both will be unlicensed in all remaining states, consistent with the pattern that only Caitlin Skidmore (DC), Cindy Fisher (MD), and Christina Chang (MD) are licensed.

---

## Documentation Requirements

For each search, create:
1. **Finding File:** `{state_code}_{firstname}_{lastname}_finding.json`
   - Example: `dc_leah_douthit_finding.json`
   - Example: `va_liddy_bisanz_finding.json`

2. **Metadata:**
   - Search date
   - Search URL
   - Search method (automated/manual)
   - License types searched
   - Results found
   - License status

3. **Consolidation:**
   - Update `all_findings.csv`
   - Generate summary reports

---

## Task Breakdown Summary

| Phase | Region | States | Searches | Priority |
|-------|--------|--------|----------|----------|
| 1 | DMV | DC, VA, CT | 6 | High |
| 2 | Northeast | PA | 2 | Medium |
| 3 | Southeast | NC, SC, GA, FL | 8 | Medium |
| 4 | Southwest | AZ, NM, UT | 6 | Low |
| **Total** | | **11** | **22** | |

---

## Next Steps

1. ✅ **Create search plan** (this document)
2. ⏳ **Phase 1 - DMV:** Start with DC (framework exists)
3. ⏳ **Phase 1 - DMV:** Continue with Virginia (iframe handling)
4. ⏳ **Phase 1 - DMV:** Complete Connecticut
5. ⏳ **Phase 2-4:** Identify search URLs and create frameworks
6. ⏳ **Execute searches** in priority order
7. ⏳ **Consolidate findings** and generate reports

---

**Last Updated:** December 8, 2025
**Status:** Planning Complete - Ready for Execution
