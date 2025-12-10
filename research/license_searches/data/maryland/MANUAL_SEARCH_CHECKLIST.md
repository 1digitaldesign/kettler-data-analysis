# Maryland Manual Search Checklist

**Date:** December 8, 2025
**Site:** Maryland DLLR Real Estate Commission
**URL:** https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name

---

## Core 15 Employees: ✅ COMPLETE

All 15 core Kettler employees have been searched and documented.

---

## Additional Individuals to Search Manually

### Priority 1: Caitlin Skidmore's Direct Connections

#### ✅ 1. Liddy Bisanz (Liddy Bisanz saye)
- **Connection:** Co-broker with Caitlin Skidmore at Lariat Realty Advisors
- **Address:** 6700 Antioch Road
- **Already Searched:**
  - ✅ New Jersey: **UNLICENSED**
  - ✅ New York: **UNLICENSED**
- **Maryland Status:** ⏳ **NOT SEARCHED**
- **Search Instructions:**
  - Last Name: `Bisanz`
  - First Name: `Liddy` (or leave blank)
  - Complete CAPTCHA
  - Click Search
- **Expected Result:** Likely unlicensed (pattern from NJ/NY)
- **File to Create:** `md_liddy_bisanz_finding.json`

#### ⏳ 2. Leah Douthit
- **Connection:** Co-broker with Caitlin Skidmore at Lariat Realty Advisors
- **Address:** 6700 Antioch Road
- **Already Searched:** ⏳ **NONE** (not searched in any state)
- **Maryland Status:** ⏳ **NOT SEARCHED**
- **Search Instructions:**
  - Last Name: `Douthit`
  - First Name: `Leah` (or leave blank)
  - Complete CAPTCHA
  - Click Search
- **Expected Result:** Unknown - needs verification
- **File to Create:** `md_leah_douthit_finding.json`
- **Note:** This is a HIGH PRIORITY search - not yet verified anywhere

---

## Why These Searches Matter

### Legal Significance
1. **Network Evidence:** If Liddy Bisanz and Leah Douthit are also unlicensed, this strengthens the evidence of a coordinated unlicensed operation network
2. **Front Person Scheme:** Shows Caitlin Skidmore is not alone in this pattern
3. **Administrative Filings:** Additional violations can strengthen complaints

### Investigation Completeness
- Both individuals are direct business partners of Caitlin Skidmore
- Their licensing status is directly relevant to the investigation
- Maryland is a key state where Kettler operates properties

---

## Search Process

### Step-by-Step for Each Individual

1. **Navigate to:** https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name

2. **Fill Form:**
   - Last Name: [Individual's last name]
   - First Name: [Individual's first name] (optional but recommended)

3. **Complete CAPTCHA:**
   - Check "I'm not a robot" box
   - Complete any image challenges if required

4. **Click Search Button**

5. **Review Results:**
   - Check for exact name match
   - Verify license type (Real Estate Broker/Salesperson)
   - Note license number, status, expiration date if found

6. **Document Results:**
   - Create JSON finding file
   - Update consolidated CSV
   - Note any patterns or connections

---

## Expected Findings

### Based on Pattern from Other States

**Liddy Bisanz:**
- New Jersey: Unlicensed ✅
- New York: Unlicensed ✅
- **Maryland:** Likely unlicensed (to be verified)

**Leah Douthit:**
- **No searches completed yet** - Unknown status
- **Maryland:** Needs verification

---

## Documentation Template

### JSON Finding File Format

```json
{
  "metadata": {
    "date": "2025-12-08",
    "state": "Maryland",
    "search_url": "https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name",
    "employee": "[Name]",
    "search_method": "Manual search",
    "license_types_searched": ["Real Estate Broker", "Real Estate Salesperson"]
  },
  "findings": {
    "[name_key]": {
      "full_name": "[Full Name]",
      "search_executed": true,
      "results_found": 0,
      "real_estate_license": false,
      "note": "[Description of search and results]"
    }
  },
  "conclusion": "[Summary conclusion]"
}
```

---

## Priority Order

1. **HIGH:** Leah Douthit (not searched anywhere yet)
2. **MEDIUM:** Liddy Bisanz (verify Maryland status)
3. **LOW:** Other connections (if time permits)

---

## Summary

**Core Employees:** ✅ 15/15 complete
**Additional Searches Needed:** 2 individuals
- Liddy Bisanz (verify MD)
- Leah Douthit (not searched anywhere)

**Total Manual Searches:** 2

---

**Last Updated:** December 8, 2025
**Status:** Ready for Manual Searches
