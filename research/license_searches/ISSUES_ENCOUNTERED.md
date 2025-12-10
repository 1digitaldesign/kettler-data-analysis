# License Search - Issues Encountered

**Date:** December 7, 2025

## Security/Malware Issues

### New Jersey Site
- **Issue:** Malicious alert dialog appearing: "MacOS Security Center" scam
- **URL:** https://newjersey.mylicense.com/verification/
- **Action Taken:** Dismissed dialog, continuing with search
- **Note:** This appears to be a malicious redirect/scam. Site may be compromised or have ad injection.

### eAccessNY Redirect
- **Issue:** URL https://www.eaccessny.com/ redirects to suspicious domain (pressurisationtech.com)
- **Action:** Will use alternative New York DOS URL instead

## Technical Issues

### Connecticut Form Interaction
- **Issue:** Custom dropdown component not responding to standard Playwright selectOption
- **Component Type:** Custom listbox (not standard HTML select)
- **Attempted Solutions:**
  - Standard selectOption - Failed
  - Direct JavaScript manipulation - Needs testing
  - Keyboard navigation - Not yet attempted
- **Status:** In progress - 2/15 employees searched

### Maryland CAPTCHA
- **Issue:** reCAPTCHA blocking all automated searches
- **Status:** Documented - requires manual intervention
- **Options:** Manual searches or CAPTCHA bypass service

## URL Verification Status

### ✅ Verified Working
- Virginia DPOR: https://www.dpor.virginia.gov/LicenseLookup
- DC OCPLA: https://govservices.dcra.dc.gov/oplaportal/Home/GetLicenseSearchDetails
- Connecticut: https://www.elicense.ct.gov/lookup/licenselookup.aspx

### ⚠️ Issues Found
- New Jersey: https://newjersey.mylicense.com/verification/ (malicious popup, but functional)
- eAccessNY: https://www.eaccessny.com/ (redirects to suspicious site)

### ✅ Alternative URLs Found
- New York: https://appext20.dos.ny.gov/nydos/searchByName.do (testing)
- New Jersey Alternative: https://www-dobi.nj.gov/DOBI_LicSearch/recSearch.jsp

## Recommendations

1. **New Jersey:** Try alternative DOBI URL or proceed with caution, dismissing popups
2. **New York:** Use DOS URL directly, avoid eAccessNY redirect
3. **Connecticut:** Continue with JavaScript-based form interaction
4. **Maryland:** Document limitation, proceed with other states
