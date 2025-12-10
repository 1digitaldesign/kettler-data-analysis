# Data Collection Todos

![Status](https://img.shields.io/badge/status-active-blue)
![Priority](https://img.shields.io/badge/priority-high-red)

Comprehensive list of data collection tasks required for the Kettler Management investigation.

---

## Overview

This document outlines all data collection tasks needed to complete the investigation and support regulatory filings. Tasks are organized by priority and category.

**Investigation Status:** License searches complete (288 files), additional data collection needed for comprehensive investigation package.

> 📊 **Track Progress:** See [DATA_COLLECTION_PROGRESS.md](DATA_COLLECTION_PROGRESS.md) for real-time progress tracking with progress bars.

---

## High Priority Data Collection

### 1. Additional License Searches

**Status:** ⚠️ Partial - 15 states complete, additional states may be needed

**Tasks:**
- [ ] **Complete Maryland searches** - 14 employees remaining (CAPTCHA issues resolved)
- [ ] **Complete Connecticut searches** - 13 employees remaining
- [ ] **Verify all 15 employees** across all operational states
- [ ] **Cross-reference license numbers** with company affiliations
- [ ] **Document license expiration dates** for all active licenses
- [ ] **Verify license status changes** (active/inactive/suspended)

**Data Needed:**
- Individual license search results (JSON format)
- License expiration dates
- License type classifications
- Company affiliation records
- License status history

**Files:** `research/license_searches/data/{state}/{state}_{person}_finding.json`

---

### 2. Company Registration Data

**Status:** ❌ Not Started

**Tasks:**
- [ ] **Kettler Management Inc.** - Verify registration in all operational states
- [ ] **Skidmore-affiliated companies** - Verify all 24+ companies registered
- [ ] **Shell company identification** - Identify any shell companies used
- [ ] **Business entity searches** - Secretary of State records
- [ ] **Registered agent information** - Verify registered agents
- [ ] **Business address verification** - Cross-reference with license addresses

**Data Needed:**
- Business registration records
- Entity formation documents
- Registered agent information
- Business addresses
- Operating authority records

**Files:** `research/company_registrations/{state}/{company}_registration.json`

---

### 3. Property Management Contracts

**Status:** ❌ Not Started

**Tasks:**
- [ ] **Property management agreements** - Collect sample contracts
- [ ] **Service scope documentation** - What services are provided
- [ ] **Geographic scope** - Properties managed by state
- [ ] **Contract terms** - Licensing requirements in contracts
- [ ] **Client lists** - Properties under management
- [ ] **Property addresses** - Verify geographic distribution

**Data Needed:**
- Property management contracts (redacted)
- Service agreements
- Property lists by state
- Client information (if publicly available)
- Geographic distribution data

**Files:** `research/contracts/property_management_contracts.json`

---

### 4. Employee Role Documentation

**Status:** ⚠️ Partial - 15 employees identified, roles need verification

**Tasks:**
- [ ] **Job descriptions** - Verify roles and responsibilities
- [ ] **Organizational charts** - Management structure
- [ ] **Employee directories** - Complete employee lists
- [ ] **Role verification** - Confirm who performs licensed activities
- [ ] **Supervision documentation** - Who supervises whom
- [ ] **Training records** - Licensing education requirements

**Data Needed:**
- Job descriptions
- Organizational charts
- Employee directories
- Role assignments
- Supervision structure
- Training documentation

**Files:** `research/employees/employee_roles.json`, `research/employees/organizational_chart.json`

---

## Medium Priority Data Collection

### 5. Regulatory Complaint History

**Status:** ❌ Not Started

**Tasks:**
- [ ] **State regulatory complaints** - Search all states for complaints
- [ ] **Consumer complaints** - Better Business Bureau, state consumer affairs
- [ ] **Enforcement actions** - Any disciplinary actions taken
- [ ] **Settlement records** - Regulatory settlements
- [ ] **License violations** - Historical violations
- [ ] **Penalty records** - Fines or penalties assessed

**Data Needed:**
- Complaint records (publicly available)
- Enforcement action documents
- Settlement agreements
- Violation history
- Penalty records

**Files:** `research/complaints/regulatory_complaints.json`, `research/complaints/enforcement_actions.json`

---

### 6. Financial Records (Public)

**Status:** ❌ Not Started

**Tasks:**
- [ ] **SEC filings** - If publicly traded or REIT
- [ ] **State business filings** - Annual reports, financial statements
- [ ] **Property value assessments** - Total property value under management
- [ ] **Revenue estimates** - Based on property values
- [ ] **Tax records** - Public tax filings if available

**Data Needed:**
- SEC filings (if applicable)
- State business filings
- Property assessment records
- Revenue estimates
- Public tax records

**Files:** `research/financial/public_filings.json`

---

### 7. News and Media Coverage

**Status:** ⚠️ Partial - Some searches completed

**Tasks:**
- [ ] **Violation coverage** - News articles about violations
- [ ] **Company announcements** - Press releases, announcements
- [ ] **Legal proceedings** - Court cases, lawsuits
- [ ] **Regulatory actions** - Media coverage of enforcement
- [ ] **Industry publications** - Trade publication coverage

**Data Needed:**
- News articles
- Press releases
- Court records (public)
- Media coverage
- Trade publication articles

**Files:** `research/news/violations_coverage.json`, `research/news/legal_proceedings.json`

---

### 8. Fair Housing and Discrimination Records

**Status:** ❌ Not Started

**Tasks:**
- [ ] **HUD complaints** - Fair Housing Act complaints
- [ ] **EEOC records** - Employment discrimination complaints
- [ ] **State discrimination complaints** - State-level complaints
- [ ] **Settlement records** - Discrimination settlements
- [ ] **Court cases** - Discrimination lawsuits

**Data Needed:**
- HUD complaint records
- EEOC records
- State complaint records
- Settlement agreements
- Court case records

**Files:** `research/discrimination/hud_complaints.json`, `research/discrimination/eeoc_records.json`

---

## Low Priority Data Collection

### 9. Professional Association Memberships

**Status:** ❌ Not Started

**Tasks:**
- [ ] **Real estate associations** - NAR, state associations
- [ ] **Property management associations** - IREM, NAA
- [ ] **Professional certifications** - CPM, ARM certifications
- [ ] **Continuing education** - CE records

**Data Needed:**
- Association memberships
- Certification records
- Continuing education records

**Files:** `research/professional/memberships.json`

---

### 10. Social Media and Online Presence

**Status:** ❌ Not Started

**Tasks:**
- [ ] **Company websites** - Service descriptions, geographic scope
- [ ] **LinkedIn profiles** - Employee profiles, company page
- [ ] **Social media** - Company social media accounts
- [ ] **Online reviews** - Google, Yelp reviews
- [ ] **Property listings** - Properties advertised for management

**Data Needed:**
- Website content
- Social media posts
- Online reviews
- Property listings

**Files:** `research/online/social_media.json`, `research/online/reviews.json`

---

## Data Collection Methods

### Official Sources

1. **State Regulatory Agencies**
   - DPOR databases
   - Real Estate Commissions
   - Secretary of State records
   - Consumer Affairs departments

2. **Federal Agencies**
   - HUD (Fair Housing)
   - EEOC (Employment)
   - SEC (if applicable)

3. **Public Records**
   - Court records
   - Business filings
   - Property records

### Research Methods

1. **Database Searches**
   - Automated browser searches
   - Manual verification
   - Cross-referencing

2. **FOIA Requests**
   - Regulatory agency records
   - Enforcement actions
   - Complaint records

3. **Public Records Requests**
   - Business filings
   - Court records
   - Property records

---

## Data Organization

### File Structure

```
research/
├── license_searches/          # ✅ Complete (288 files)
├── company_registrations/     # ❌ Not started
├── contracts/                 # ❌ Not started
├── employees/                 # ⚠️ Partial
├── complaints/                # ❌ Not started
├── financial/                 # ❌ Not started
├── news/                      # ⚠️ Partial
├── discrimination/            # ❌ Not started
├── professional/              # ❌ Not started
└── online/                    # ❌ Not started
```

### Data Format

**JSON Schema:** All data follows `data/schema.json`
- Standardized structure
- Primary/Foreign key relationships
- Metadata included
- Timestamps and sources

---

## Priority Matrix

| Task | Priority | Status | Estimated Effort |
|------|----------|--------|------------------|
| Complete license searches | HIGH | ⚠️ Partial | 2-3 days |
| Company registrations | HIGH | ❌ Not started | 1-2 days |
| Property management contracts | HIGH | ❌ Not started | 3-5 days |
| Employee role documentation | HIGH | ⚠️ Partial | 1-2 days |
| Regulatory complaints | MEDIUM | ❌ Not started | 2-3 days |
| Financial records | MEDIUM | ❌ Not started | 1-2 days |
| News coverage | MEDIUM | ⚠️ Partial | 1 day |
| Fair Housing records | MEDIUM | ❌ Not started | 2-3 days |
| Professional memberships | LOW | ❌ Not started | 1 day |
| Social media | LOW | ❌ Not started | 1 day |

---

## Next Steps

### Immediate (This Week)

1. **Complete Maryland license searches** - Resolve CAPTCHA, finish 14 remaining searches
2. **Complete Connecticut license searches** - Finish 13 remaining searches
3. **Company registration searches** - Start with primary operational states

### Short-term (Next 2 Weeks)

4. **Property management contracts** - Collect sample contracts
5. **Employee role verification** - Document all employee roles
6. **Regulatory complaint searches** - Search all state databases

### Medium-term (Next Month)

7. **Financial records** - Collect public financial data
8. **Fair Housing records** - HUD and EEOC searches
9. **News coverage** - Complete media searches

---

## Related Documentation

- [Investigation Summary](../license_searches/reports/INVESTIGATION_SUMMARY.md) - Complete investigation overview
- [Executive Summary](../license_searches/reports/EXECUTIVE_SUMMARY_FOR_FILINGS.md) - Filing-ready summary
- [Data Guide](../DATA_GUIDE.md) - Data structure guide
- [Research README](../README.md) - Research directory guide

---

**Last Updated:** 2025-12-10
**Status:** Active - Data collection in progress
**Next Review:** Weekly
