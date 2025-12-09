# Lease Agreement Abnormality Report

**Date:** December 7, 2025
**Property:** 800 John Carlyle Street, Unit 533, Alexandria, VA 22314
**Lease File:** LeaseRenewalAgreement_6102025.txt

## Key Information Extracted

- **Owner:** Azure Carlyle LP
- **Manager:** Kettler Management
- **Residents:** Joran Bailey, Betty Tai
- **Lease Term:** April 17, 2025 to May 16, 2026 (13 months)
- **Monthly Rent:** $2,325.00
- **Security Deposit:** $300.00
- **Lease Signed:** February 26, 2025

## Abnormalities Identified

### 1. Unusually Low Security Deposit (MEDIUM SEVERITY)

**Finding:** Security deposit of $300 is only 12.9% of monthly rent ($2,325)

**Standard Practice:** Security deposits typically range from 50% to 200% of monthly rent (0.5-2 months)

**Implications:**
- Significantly below industry standard
- May indicate financial risk acceptance
- Could suggest unusual lease terms or relationship

**Ratio:** 0.129 (standard: 0.5-2.0)

### 2. Owner-Manager Entity Separation (HIGH SEVERITY)

**Finding:** Owner entity "Azure Carlyle LP" is separate from management company "Kettler Management"

**Investigation Needed:**
- Verify relationship between Azure Carlyle LP and Kettler Management
- Check if Azure Carlyle LP is a Kettler entity or separate
- Search Virginia State Corporation Commission for Azure Carlyle LP registration
- Verify Kettler Management's authority to manage Azure Carlyle LP properties

**Relevance:** This separation may be part of the shell company structure identified in other analyses

### 3. Missing Explicit STR Prohibition (MEDIUM SEVERITY)

**Finding:** Lease does not appear to explicitly prohibit short-term rentals (Airbnb, VRBO, subletting)

**Context:** Investigation has identified 90+ unregistered STRs at 800 John Carlyle

**Implications:**
- Lack of explicit prohibition may facilitate STR operations
- Could be intentional omission
- Standard leases typically include subletting/STR prohibitions

### 4. Accommodation Language Present (HIGH SEVERITY)

**Finding:** Lease contains reasonable accommodation and disability-related language

**Relevance:**
- Given UPL investigation regarding Edward Hyland's denial of reasonable accommodation
- Language in lease may conflict with actual practices
- Evidence suggests RA was denied despite lease language

### 5. Multiple Additional Fees

**Fees Identified:**
- Amenity Fee: $500 (one-time)
- Animal Rent: $60/month
- Animal Fee: $500 (one-time)
- Parking (2nd vehicle): $125/month
- Trash: $10/month
- Pest Control: $2.75/month

**Note:** Amenity fee of $500 is significant additional cost

### 6. Kettler Management Contact Information

**Address:** 800 John Carlyle Street, Alexandria, VA 22314
**Phone:** (703) 299-7599

**Note:** Management office is at the same address as the leased property

## Connections to Investigation

1. **Kettler Management** - Listed as manager, consistent with investigation findings
2. **800 John Carlyle** - Property address matches investigation focus
3. **Azure Carlyle LP** - New entity identified, requires verification
4. **Low Security Deposit** - May indicate unusual business practices
5. **STR Context** - Lease terms may facilitate STR operations

## Recommended Actions

1. **Search Virginia SCC** for Azure Carlyle LP registration
2. **Verify relationship** between Azure Carlyle LP and Kettler entities
3. **Check property records** for 800 John Carlyle ownership
4. **Compare lease terms** with other Kettler-managed properties
5. **Investigate Azure Carlyle LP** in all state databases

## Data Sources

- Lease Agreement Analysis: `research/lease_agreement_analysis.json`
- Detailed Abnormality Analysis: `research/lease_abnormalities_detailed.json`
- Azure Carlyle Search Framework: `research/azure_carlyle_search.json`

---

*This report analyzes the 2025 lease renewal agreement for abnormalities and connections to the broader investigation.*
