# Kettler Data Analysis

Property management licensing investigation platform. Python-first architecture.

**Status:** Research Framework 100% Complete - Ready for Complaint Filing  
**Last Updated:** December 10, 2025

---

## Quick Start

### Filing Administrative Complaints
- [Executive Summary](research/va_dpor_complaint/EXECUTIVE_SUMMARY.json)
- [Complaint Readiness](research/RESEARCH_READY_FOR_COMPLAINT.json)
- [Master Research Index](research/MASTER_RESEARCH_INDEX.json)

### Understanding Findings
- [100% Verification](research/FINAL_100_PERCENT_VERIFIED.json)
- [Research Index](research/RESEARCH_INDEX.json)
- [VA DPOR Complaint Files](research/va_dpor_complaint/)

### Data Analysis
- [Firm Data](data/source/skidmore_all_firms_complete.json) - 38 firms
- [Connections](research/connections/) - Connection analyses
- [Violations](research/violations/) - Violation findings
- [Anomalies](research/anomalies/) - Anomaly reports

---

## System Overview

**Purpose:** Multi-state license search, connection analysis, and regulatory compliance investigation.

**Architecture:** Python-first with unified core modules, ETL pipeline, and optional API/web frontend.

**Data Flow:** Source → Extract → Clean → Analyze → Research Outputs

## Installation

```bash
git clone https://github.com/1digitaldesign/kettler-data-analysis.git
cd kettler-data-analysis
pip install -r requirements.txt
python bin/run_pipeline.py
```

See [INSTALLATION.md](INSTALLATION.md) for detailed setup.

## Usage

**Full Pipeline:**
```bash
python bin/run_pipeline.py
```

**Individual Scripts:**
```bash
python bin/analyze_connections.py  # Connection analysis
python bin/validate_data.py        # Data validation
python bin/clean_data.py           # Data cleaning
python bin/generate_reports.py     # Report generation
```

## Documentation

**Getting Started:**
- [INSTALLATION.md](INSTALLATION.md) - Setup guide
- [QUICK_START.md](QUICK_START.md) - Quick start
- [STATUS.md](STATUS.md) - Current status

**System Documentation:**
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
- [Data Flow](docs/DATA_FLOW.md)
- [Components](docs/COMPONENTS.md)
- [Repository Structure](docs/REPOSITORY_STRUCTURE.md)
- [Diagrams](docs/DIAGRAMS.md)

**Data Documentation:**
- [Schema](data/schema.json) - FK/PK relationships
- [Data Dictionary](data/DATA_DICTIONARY.md) - Field definitions
- [Ontology](data/ONTOLOGY.md) - Conceptual relationships
- [Ancestry](data/ANCESTRY.md) - Data lineage
- [Metadata](data/metadata.json) - Global metadata

**Complete Index:**
- [Documentation Index](docs/INDEX.md) - All documentation

## Research Status

**100% Complete:** All critical areas documented, evidence compiled, ready for complaint filing.

**Statistics:**
- 350 JSON files + 30 markdown files
- 10 research categories
- 285 license searches across 15 states
- 38 firms, 40+ individual licenses
- 100+ connections identified

**Key Findings:**
- 8 regulatory violations across 11 states
- Principal broker gap: 10.5 years
- Geographic violation: 1,300 miles
- 16 unlicensed personnel (7 property managers)
- $4.75B property value under management

## System Structure

```
bin/              # Entry points
scripts/core/     # Unified modules
scripts/analysis/ # Analysis scripts
scripts/etl/      # ETL pipeline
data/             # Data (source, cleaned, vectors)
research/         # Research outputs
docs/             # Documentation
```

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
