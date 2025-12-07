# Administrative Filing Documentation

## Quick Start

This repository contains all evidence and documentation needed to file administrative complaints with federal, state, and local agencies regarding real estate license violations and potential fraud.

## Key Documents

1. **FILING_GUIDE.md** - Complete guide for filing complaints
2. **EVIDENCE_SUMMARY.md** - Summary of all evidence
3. **PROJECT_ORGANIZATION.md** - Project structure guide
4. **filings/executive_summary.md** - Executive summary for agencies
5. **filings/filing_checklist.csv** - Filing checklist with priorities

## Evidence Package

**Location:** `filings/filing_evidence_package.json`

Contains:
- All extracted entities from PDF (emails, addresses, phone numbers)
- License violation data
- Connection analysis
- Fraud indicators
- Filing recommendations

## Key Findings

### Critical Evidence
1. **11 firms** list Caitlin Skidmore as Principal Broker
2. **KETTLER MANAGEMENT INC** matches PDF address (8255 Greensboro Drive, McLean, VA)
3. **6 firms** share same Texas address (potential shell companies)
4. **4 @kettler.com emails** found in PDF evidence
5. **PDF mentions violations:** violation (1), misrepresentation (4), breach (2)

### Recommended Filings (Priority Order)

1. **Virginia DPOR** - HIGH PRIORITY
   - 11 firms with license violations
   - Clear evidence of principal broker pattern

2. **Federal Trade Commission (FTC)** - HIGH PRIORITY
   - Consumer fraud complaint
   - Multiple firms, deceptive practices

3. **Consumer Financial Protection Bureau (CFPB)** - HIGH PRIORITY
   - Address clustering suggests shell company scheme

4. **State Real Estate Commissions** - MEDIUM PRIORITY
   - NC, TX, MD, MO, NE

## Running Analysis

```bash
# Extract PDF evidence
cd scripts/extraction && Rscript extract_pdf_evidence.R

# Search regulatory agencies
cd scripts/search && Rscript search_regulatory_agencies.R

# Analyze fraud patterns
cd scripts/analysis && Rscript analyze_fraud_patterns.R

# Organize all evidence
cd ../.. && Rscript organize_evidence.R
```

## File Locations

- **Evidence PDFs:** `evidence/pdfs/`
- **Filing Materials:** `filings/`
- **Research Outputs:** `research/`
- **Analysis Scripts:** `scripts/`
- **License Data:** Root directory (`skidmore_*.csv`)

## Contact Information

See `research/regulatory_agencies_registry.json` for complete agency contact information and filing URLs.
