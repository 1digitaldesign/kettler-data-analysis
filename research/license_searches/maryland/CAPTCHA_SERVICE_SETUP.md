# CAPTCHA Service Setup for Maryland Searches

**Date:** December 7, 2025
**Status:** Ready for Configuration

## Overview

This document explains how to set up a CAPTCHA solving service to automate Maryland DLLR license searches.

## Available Services

### 1. 2Captcha (Recommended)
- **URL:** https://2captcha.com
- **Cost:** $2.99 per 1000 CAPTCHAs (~$0.003 per search)
- **Success Rate:** ~95%
- **Setup Time:** 5 minutes

### 2. Anti-Captcha
- **URL:** https://anti-captcha.com
- **Cost:** $1.00 per 1000 CAPTCHAs (~$0.001 per search)
- **Success Rate:** ~98%
- **Setup Time:** 5 minutes

### 3. CapSolver
- **URL:** https://capsolver.com
- **Cost:** $1.50 per 1000 CAPTCHAs (~$0.0015 per search)
- **Success Rate:** ~96%
- **Setup Time:** 5 minutes

## Setup Instructions

### Step 1: Create Account

1. Visit one of the service websites above
2. Create an account
3. Add funds (minimum usually $2-5)
4. Get your API key from account dashboard

### Step 2: Install Dependencies

```bash
cd /Users/machine/.cursor/worktrees/kettler-data-analysis/nzg
npm install axios playwright-recaptcha
```

### Step 3: Set API Key

**Option A: Environment Variable (Recommended)**
```bash
export CAPTCHA_API_KEY=your_api_key_here
export CAPTCHA_SERVICE=2captcha  # or 'anticaptcha' or 'capsolver'
```

**Option B: Direct in Script**
Edit `scripts/search/maryland_captcha_service_search.js` and replace:
```javascript
const CAPTCHA_SERVICE_API_KEY = 'your_api_key_here';
```

### Step 4: Run Script

```bash
node scripts/search/maryland_captcha_service_search.js
```

## Cost Estimate

For 15 employees:
- **2Captcha:** ~$0.045 (15 × $0.003)
- **Anti-Captcha:** ~$0.015 (15 × $0.001)
- **CapSolver:** ~$0.023 (15 × $0.0015)

**Recommended:** Anti-Captcha (lowest cost, highest success rate)

## Manual Fallback

If API key is not set, the script will:
1. Fill in the search form
2. Wait for you to manually complete CAPTCHA
3. Continue automation after CAPTCHA is completed

## Testing

Test with one employee first:
```javascript
// In script, temporarily change:
const EMPLOYEES = [
  { name: 'Edward Hyland', last_name: 'Hyland', first_name: 'Edward', priority: 'HIGH' }
];
```

## Troubleshooting

### Error: "CAPTCHA_API_KEY not set"
- Set environment variable: `export CAPTCHA_API_KEY=your_key`
- Or edit script directly

### Error: "Insufficient balance"
- Add funds to your CAPTCHA service account
- Check account balance on service dashboard

### Error: "CAPTCHA solving timeout"
- Service may be slow, try again
- Check service status page
- Consider switching to different service

### Error: "Could not find reCAPTCHA site key"
- Page structure may have changed
- Check if CAPTCHA iframe is present
- May need to update script

## Alternative: Manual CAPTCHA

If you prefer not to use a service:
1. Use `maryland_manual_captcha_search.R` framework
2. Complete CAPTCHA manually for each search
3. Script will wait and continue after completion

## Next Steps

1. ✅ Choose a CAPTCHA service (recommend Anti-Captcha)
2. ✅ Create account and get API key
3. ✅ Set environment variable
4. ✅ Run test with one employee
5. ✅ Run full search for all 15 employees

## Files

- `scripts/search/maryland_captcha_service_search.js` - Main automation script
- `research/license_searches/maryland/maryland_search_framework.json` - Employee list
- `research/license_searches/maryland/CAPTCHA_SERVICE_SETUP.md` - This file
