# Project Organization Guide

## Folder Structure

```
kettler-data-analysis/
├── evidence/                    # Source evidence documents
│   ├── pdfs/                   # PDF documents (lease terminations, etc.)
│   ├── emails/                 # Email correspondence
│   └── documents/               # Other supporting documents
│
├── filings/                     # Administrative filing materials
│   ├── federal/                # Federal agency filing information
│   │   └── federal_agencies.csv
│   ├── state/                  # State agency filing information
│   │   └── state_agencies.csv
│   ├── local/                  # Local agency filing information
│   │   └── local_agencies.csv
│   ├── filing_checklist.csv     # Complete filing checklist
│   ├── filing_evidence_package.json  # Complete evidence package
│   └── executive_summary.md     # Executive summary for filings
│
├── research/                    # Research and analysis outputs
│   ├── regulatory_agencies_registry.json  # All regulatory agencies
│   ├── pdf_evidence_extracted.json       # Extracted PDF data
│   ├── pdf_evidence_summary.csv          # PDF evidence summary
│   ├── fraud_indicators.json              # Identified fraud patterns
│   └── filing_recommendations.json       # Filing recommendations
│
├── data/                        # Processed data
│   ├── raw/                    # Raw search results
│   ├── cleaned/                # Cleaned and standardized data
│   └── analysis/               # Analysis outputs
│       ├── dpor_skidmore_connections.csv
│       ├── dpor_validated.csv
│       ├── analysis_summary.json
│       └── data_quality_report.json
│
├── scripts/                     # Analysis scripts
│   ├── extraction/             # Evidence extraction scripts
│   │   └── extract_pdf_evidence.R
│   ├── search/                 # Search and discovery scripts
│   │   └── search_regulatory_agencies.R
│   └── analysis/               # Analysis scripts
│       └── analyze_fraud_patterns.R
│
├── skidmore_*.csv              # Original Skidmore data files
├── state_dpor_registry.csv     # State DPOR registry
├── organize_evidence.R          # Master organization script
└── FILING_GUIDE.md             # Complete filing guide
```

## Key Evidence Files

### PDF Evidence
- **Location:** `evidence/pdfs/Gmail - RE_ Formal Notice of Lease Termination - Unit 533 - Addendum with Additional Documentation.pdf`
- **Key Information Extracted:**
  - Address: 8255 Greensboro Drive #200, McLean, VA 22102
  - Emails: 8 addresses (including @kettler.com addresses)
  - Violations mentioned: violation (1), misrepresentation (4), breach (2)
  - Agencies mentioned: HUD, SEC, IRS
  - Units: 533, 433, 147

### License Data
- **Files:**
  - `skidmore_all_firms_complete.csv` - Complete firm data
  - `skidmore_firms_database.csv` - Firm database
  - `skidmore_individual_licenses.csv` - Individual licenses
  - `data/analysis/dpor_skidmore_connections.csv` - Connection analysis

### Cross-Reference Findings
- **KETTLER MANAGEMENT INC** matches PDF address (8255 Greensboro Drive, McLean, VA)
- **6 firms** share same Texas address (5729 LEBANON RD STE 144553, FRISCO, TX 75034)
- **11 firms** list Caitlin Skidmore as Principal Broker
- **8 firms** have license gaps of 6.5-14 years

## Quick Reference

### To Extract PDF Evidence
```bash
cd scripts/extraction
Rscript extract_pdf_evidence.R
```

### To Search Regulatory Agencies
```bash
cd scripts/search
Rscript search_regulatory_agencies.R
```

### To Analyze Fraud Patterns
```bash
cd scripts/analysis
Rscript analyze_fraud_patterns.R
```

### To Organize All Evidence
```bash
Rscript organize_evidence.R
```

### To View Filing Checklist
```bash
cat filings/filing_checklist.csv
```

## Evidence Summary

### Address Connections
1. **8255 Greensboro Drive, McLean, VA** - Found in PDF and matches KETTLER MANAGEMENT INC license
2. **5729 LEBANON RD STE 144553, FRISCO, TX 75034** - 6 firms + Skidmore individual licenses

### Email Connections
- **@kettler.com addresses found in PDF:**
  - ehyland@kettler.com
  - Carlyle.PM@kettler.com
  - Carlyle@kettler.com
  - Carlyle.APM@kettler.com

### Violation Patterns
- License gaps: 8 firms with 6.5-14 year gaps
- Address clustering: 6 firms at same Texas address
- Principal broker pattern: 11 firms listing same broker
- Timeline issues: Firms licensed after Skidmore (potential backdating)

## Filing Priorities

### HIGH PRIORITY
1. **Virginia DPOR** - 11 firms, clear license violations
2. **FTC** - Consumer fraud, multiple firms pattern
3. **CFPB** - Address clustering suggests shell companies

### MEDIUM PRIORITY
4. **HUD** - If housing violations apply
5. **State Real Estate Commissions** (NC, TX, MD, MO, NE)

## Next Steps

1. Review `filings/filing_evidence_package.json` for complete evidence
2. Review `FILING_GUIDE.md` for detailed filing instructions
3. Use `filings/filing_checklist.csv` to track filing progress
4. Contact agencies using `research/regulatory_agencies_registry.json`
