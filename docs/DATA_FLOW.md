# Data Flow

![Pipeline](https://img.shields.io/badge/pipeline-ETL-blue)
![Status](https://img.shields.io/badge/status-operational-brightgreen)

## Pipeline Overview

```mermaid
flowchart LR
    A[Source Data<br/>data/source/] --> B[Extraction<br/>scripts/extraction/]
    B --> C[Raw Data<br/>data/raw/]
    C --> D[Cleaning<br/>bin/clean_data.py]
    D --> E[Cleaned Data<br/>data/cleaned/]
    E --> F[Analysis<br/>scripts/core/]
    F --> G[Research Outputs<br/>research/]

    G --> H[connections/]
    G --> I[summaries/]
    G --> J[verification/]
    G --> K[violations/]
    G --> L[anomalies/]
    G --> M[timelines/]

    style A fill:#C8E6C9
    style E fill:#FFF9C4
    style G fill:#E1BEE7
    style H fill:#D1C4E9
    style I fill:#D1C4E9
    style J fill:#D1C4E9
    style K fill:#D1C4E9
    style L fill:#D1C4E9
    style M fill:#D1C4E9
```

## Processing Steps

<details>
<summary><b>1. Source Data</b> (`data/source/`)</summary>

**Files:**
- `skidmore_all_firms_complete.json` - 38 firms
- `skidmore_individual_licenses.json` - Individual licenses

**Format:** JSON
**Status:** ✅ Complete

</details>

<details>
<summary><b>2. Extraction</b> (`scripts/extraction/`)</summary>

**Purpose:** Extract data from PDFs, Excel files, web sources

**Scripts:**
- `extract_pdf_evidence.py` - PDF extraction
- `extract_excel_evidence.py` - Excel extraction

**Output:** `data/raw/`

</details>

<details>
<summary><b>3. Raw Data</b> (`data/raw/`)</summary>

**Content:** Unprocessed search results

**Status:** Gitignored (not tracked)

</details>

<details>
<summary><b>4. Cleaning</b> (`bin/clean_data.py`)</summary>

**Purpose:** Standardize and normalize data

**Operations:**
- ✅ Normalize firm names
- ✅ Standardize addresses
- ✅ Parse dates
- ✅ Extract entities
- ✅ Remove duplicates

**Output:** `data/cleaned/`

</details>

<details>
<summary><b>5. Cleaned Data</b> (`data/cleaned/`)</summary>

**Files:**
- `firms.json` - Cleaned firm data
- `individual_licenses.json` - Cleaned license data

**Status:** Gitignored (not tracked)

</details>

<details>
<summary><b>6. Analysis</b> (`scripts/core/`, `scripts/analysis/`)</summary>

**Purpose:** Run analyses and generate insights

**Modules:**
- UnifiedAnalyzer - Analysis operations
- UnifiedInvestigator - Investigation
- Analysis scripts - Pattern detection

**Output:** `research/{category}/`

</details>

<details>
<summary><b>7. Research Outputs</b> (`research/`)</summary>

**Categories:**
- `connections/` - Connection analyses
- `violations/` - Violation findings
- `anomalies/` - Anomaly reports
- `evidence/` - Evidence summaries
- `verification/` - Verification results
- `summaries/` - Summary reports
- `timelines/` - Timeline analyses

**Status:** ✅ 350+ files

</details>

## Data Types

| Type | Location | Description |
|------|----------|-------------|
| **Source** | `data/source/` | Authoritative datasets |
| **Raw** | `data/raw/` | Unprocessed results |
| **Cleaned** | `data/cleaned/` | Standardized data |
| **Vectors** | `data/vectors/` | Vector embeddings |
| **Research** | `research/` | Analysis outputs |

## Quick Reference

```bash
# Run full pipeline
python bin/run_pipeline.py

# Run individual steps
python bin/clean_data.py           # Step 4: Cleaning
python bin/analyze_connections.py  # Step 6: Analysis
python bin/validate_data.py        # Validation
```

> 📘 See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for architecture details.
