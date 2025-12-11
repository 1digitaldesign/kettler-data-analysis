# Bar License Check Summary

**Date:** December 11, 2025
**Status:** Browser automation attempted - some sites require manual access

## Employees to Check for Bar Licenses

### High Priority (Likely Attorneys):

1. **Sean Curtin** - General Counsel
   - **Title:** General Counsel
   - **Reason:** General Counsel typically requires bar admission
   - **States to Check:** DC, VA, MD, NY, CT, NJ

2. **Todd Bowen** - SVP Strategic Services
   - **Title:** SVP Strategic Services
   - **Reason:** May have legal background
   - **States to Check:** Multiple states (bar license files exist)

3. **Edward Hyland** - Senior Regional Manager
   - **Title:** Senior Regional Manager
   - **Reason:** Bar license files exist for multiple states
   - **States to Check:** Various states

### Medium Priority:

4. **Pat Cassada** - CFO
   - May have legal/compliance background

5. **Robert Kettler** - CEO/Founder
   - May have legal background

6. **Cindy Fisher** - President
   - May have legal background

## Bar Association Search URLs

### District of Columbia
- **DC Bar:** https://www.dcbar.org/member-directory/ (404 error - site may be broken)
- **DC Courts Attorney Search:** https://www.dccourts.gov/services/attorney-services/attorney-search (404 error)
- **Alternative:** Search DC Bar website directly or use Google search

### Virginia
- **Virginia State Bar:** https://www.vsb.org/site/members/lookup
- **Status:** Accessible

### Maryland
- **Maryland State Bar Association:** https://www.msba.org/member-directory/
- **Maryland Attorney Search:** https://www.courts.state.md.us/attygrievance/attysearch

### New York
- **New York State Bar Association:** https://www.nysba.org/member-directory/
- **New York Attorney Search:** https://iapps.courts.state.ny.us/attorney/AttorneySearch

### Connecticut
- **Connecticut Bar Association:** https://www.ctbar.org/member-directory/
- **Connecticut Attorney Search:** https://www.jud.ct.gov/attorney/

### New Jersey
- **New Jersey State Bar Association:** https://www.njsba.com/member-directory/
- **New Jersey Attorney Search:** https://www.njcourts.gov/attorneys/attorney-search

## Browser Automation Challenges

1. **DC Bar Directory:** Returns 404 error - site may be broken or restructured
2. **DC Courts:** Attorney search page returns 404
3. **Some sites require:** Login, CAPTCHA, or have complex search forms

## Recommended Manual Search Process

### For Each Employee:

1. **Sean Curtin (General Counsel)**
   - Search: "Sean Curtin" + "attorney" + "DC"
   - Search: "Sean Curtin" + "bar" + state name
   - Check LinkedIn for bar admission information
   - Check state bar association directories manually

2. **Todd Bowen**
   - Search existing bar license files for states searched
   - Verify findings with state bar associations
   - Check multiple states

3. **Edward Hyland**
   - Review existing bar license findings
   - Verify with state bar associations
   - Check for any bar licenses found

## Existing Bar License Files

**Total Files:** 133+ bar license finding files exist

**States Covered:**
- Alabama (AL)
- Arizona (AR)
- California (CA)
- Colorado (CO)
- Connecticut (CT)
- Delaware (DE)
- District of Columbia (DC)
- Florida (FL)
- Georgia (GE)
- Massachusetts (MA)
- Nebraska (NE)
- Pennsylvania (PE)
- Virgin Islands (VI)

**Key Findings from Existing Files:**
- Most searches show "bar_license: false"
- Files indicate "requires manual verification"
- Status: "Not found" for most employees

## Next Steps

1. **Manual Verification Required:**
   - DC Bar directory appears broken (404 error)
   - State bar association websites may require manual navigation
   - Some sites have CAPTCHA protection

2. **Alternative Search Methods:**
   - Google search: "[Name] attorney [State] bar"
   - LinkedIn profiles for bar admission information
   - State bar association member directories
   - Court records for attorney admissions

3. **Priority Employees:**
   - **Sean Curtin** (General Counsel) - highest priority
   - **Todd Bowen** - multiple state files exist
   - **Edward Hyland** - multiple state files exist

## Files to Update

After manual searches, update:
- `research/license_searches/data/bar_licenses/DC_sean_curtin_bar_finding.json`
- `research/license_searches/data/bar_licenses/*_todd_bowen_bar_finding.json`
- `research/license_searches/data/bar_licenses/*_edward_hyland_bar_finding.json`
- Other relevant bar license files

## Notes

- Browser automation blocked by 404 errors on DC Bar site
- State bar association websites may require different search approaches
- Manual verification recommended for critical employees (especially General Counsel)
