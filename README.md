# Kettler Data Analysis

Property management licensing investigation platform. Python-first architecture.

![Status](https://img.shields.io/badge/status-100%25%20complete-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Research](https://img.shields.io/badge/research-350%20files-orange)

**Last Updated:** December 10, 2025

---

## About this project

This platform helps investigate property management licensing compliance across multiple states. It searches licenses, analyzes connections between firms and individuals, and generates research outputs for regulatory compliance investigations.

**What you can do:**
- Search licenses across 15 states
- Map connections between firms and individuals
- Detect anomalies and violations
- Extract evidence from PDFs and Excel files
- Generate comprehensive research reports

---

## Quick Start

Choose your path based on what you need to do:

<details>
<summary><b>Filing administrative complaints</b></summary>

Start here if you're preparing regulatory complaints:

- [VA DPOR Complaint Files](research/va_dpor_complaint/) - Complete complaint research
- [Research Index](research/RESEARCH_INDEX.json) - Master research index
- [Research README](research/README.md) - Research directory guide

</details>

<details>
<summary><b>Understanding findings</b></summary>

Start here to explore research results:

- [Research Index](research/RESEARCH_INDEX.json) - Master file index
- [VA DPOR Complaint Files](research/va_dpor_complaint/) - Complaint research
- [Research Reports](research/reports/) - Summary reports

</details>

<details>
<summary><b>Data analysis</b></summary>

Start here for data exploration:

- [Firm Data](data/source/skidmore_all_firms_complete.json) - 38 firms
- [Connections](research/connections/) - Connection analyses
- [Research Reports](research/reports/) - Analysis reports

</details>

---

## System overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Multi-state license search, connection analysis, and regulatory compliance investigation |
| **Architecture** | Python-first with unified core modules, ETL pipeline, and optional API/web frontend |
| **Data Flow** | Source → Extract → Clean → Analyze → Research Outputs |

---

## Installation

Install dependencies and run the pipeline:

```bash
git clone https://github.com/1digitaldesign/kettler-data-analysis.git
cd kettler-data-analysis
pip install -r requirements.txt
python bin/run_pipeline.py
```

> See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

**Requirements:** Python 3.10 or higher (Python 3.11+ recommended)

---

## Usage

### Run the full pipeline

```bash
python bin/run_pipeline.py
```

This runs the complete data processing pipeline:

1. Data extraction
2. Data cleaning
3. Connection analysis
4. Data validation
5. Report generation

### Run individual scripts

```bash
python bin/analyze_connections.py  # Connection analysis
python bin/validate_data.py        # Data validation
python bin/clean_data.py          # Data cleaning
python bin/generate_reports.py    # Report generation
```

---

## Documentation

### Getting started

- [INSTALLATION.md](INSTALLATION.md) - Setup guide
- [QUICK_START.md](QUICK_START.md) - Quick start
- [STATUS.md](STATUS.md) - Current status

### System documentation

- [System Architecture](docs/SYSTEM_ARCHITECTURE.md) - Architecture details
- [Data Flow](docs/DATA_FLOW.md) - Data pipeline
- [Components](docs/COMPONENTS.md) - Component reference
- [Repository Structure](docs/REPOSITORY_STRUCTURE.md) - File organization
- [Diagrams](docs/DIAGRAMS.md) - Visual diagrams

### Data documentation

- [Schema](data/schema.json) - FK/PK relationships
- [Data Dictionary](data/DATA_DICTIONARY.md) - Field definitions
- [Ontology](data/ONTOLOGY.md) - Conceptual relationships
- [Ancestry](data/ANCESTRY.md) - Data lineage
- [Metadata](data/metadata.json) - Global metadata

### Documentation index

- [Documentation Index](docs/INDEX.md) - All documentation
- [Documentation Graph](docs/DOCUMENTATION_GRAPH.md) - Interactive documentation network

**Documentation network:**

```mermaid
graph LR
    README[README.md] --> INDEX[docs/INDEX.md]
    INDEX --> ARCH[docs/SYSTEM_ARCHITECTURE.md]
    INDEX --> DATA[data/DATA_DICTIONARY.md]
    INDEX --> RESEARCH[research/README.md]

    style README fill:#C8E6C9,stroke:#4CAF50,stroke-width:3px
    style INDEX fill:#B3E5FC,stroke:#2196F3,stroke-width:2px
```

---

## Research status

![Research](https://img.shields.io/badge/research-100%25%20complete-brightgreen)
![Files](https://img.shields.io/badge/files-350%20JSON%20%2B%2030%20MD-blue)
![States](https://img.shields.io/badge/states-15%20searched-orange)

**Status:** 100% complete. All critical areas documented, evidence compiled, ready for complaint filing.

### Statistics

| Metric | Value |
|--------|-------|
| **Total Files** | 350 JSON + 30 MD |
| **Research Categories** | 10 categories |
| **License Searches** | 285 files across 15 states |
| **Firms** | 38 firms |
| **Individual Licenses** | 40+ licenses |
| **Connections** | 100+ connections |

### Key findings

- 8 regulatory violations across 11 states
- Principal broker gap: 10.5 years
- Geographic violation: 1,300 miles
- 16 unlicensed personnel (7 property managers)
- $4.75B property value under management

---

## System structure

```
bin/              # Entry points
scripts/core/     # Unified modules
scripts/analysis/ # Analysis scripts
scripts/etl/      # ETL pipeline
data/             # Data (source, cleaned, vectors)
research/         # Research outputs
docs/             # Documentation
```

---

## Features

- Multi-state license search
- Connection mapping
- Anomaly detection
- Evidence extraction (PDF/Excel)
- Vector embeddings
- Timeline analysis
- Schema validation

---

**Research Status:** 100% Complete - Ready for Complaint Filing
