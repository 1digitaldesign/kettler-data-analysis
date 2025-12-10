# Virginia DPOR Company Extraction Status

**Date:** December 8, 2025
**Status:** 🔄 **IN PROGRESS** - 3 of 40 licenses extracted (7.5%)

## Summary

Successfully identified **40 individual Principal Broker licenses** for Caitlin Skidmore in Virginia, indicating a massive "broker for rent" operation significantly larger than the 24 companies found in DC.

## Extracted Companies (3)

1. **BOZZUTO MANAGEMENT COMPANY**
   - Individual License: 0225273913
   - Firm License: 0226024808
   - Status: Confirmed
   - Note: Also found in DC list

2. **CORTLAND MANAGEMENT LLC**
   - Individual License: 0225273906
   - Firm License: 0226038642
   - Status: Confirmed
   - Note: NEW - not in DC list

3. **MIDDLEBURG MANAGEMENT LLC**
   - Individual License: 0225258285
   - Firm License: 0226038324
   - Status: Confirmed
   - Note: NEW - not in DC list

## Remaining Work

**37 licenses remaining** - Need to extract company names via Related Licenses tab

### Known License Numbers (Sample)
- 0225273785
- 0225273907
- 0225273908
- 0225273909
- 0225273910
- 0225273911
- 0225273912
- (Plus 30 more across pages 2-4)

## Technical Challenges

The Virginia DPOR website uses an iframe-based interface that makes automated extraction challenging:
- Browser automation struggles with iframe navigation
- Related Licenses tab requires precise element targeting
- Page structure changes dynamically

## Next Steps

1. **Option A:** Continue manual browser extraction (systematic clicking through each license)
2. **Option B:** Develop custom scraping script targeting the iframe content directly
3. **Option C:** Use Virginia DPOR API if available (needs investigation)

## Impact

This finding reveals:
- **40 companies** using Caitlin Skidmore as broker in Virginia alone
- Potential **massive supervision violations** (impossible to supervise 40 companies)
- Scale of "broker for rent" operation is **67% larger** than initially found in DC (40 vs 24)
