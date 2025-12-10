# Kettler Data Analysis

> Property management licensing investigation platform. Python-first architecture.

![Status](https://img.shields.io/badge/status-100%25%20complete-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Research](https://img.shields.io/badge/research-350%20files-orange)

**Last Updated:** December 10, 2025

---

## 🚀 Quick Start

<details>
<summary><b>📋 For Filing Administrative Complaints</b></summary>

- 📄 [Executive Summary](research/va_dpor_complaint/EXECUTIVE_SUMMARY.json)
- ✅ [Complaint Readiness](research/RESEARCH_READY_FOR_COMPLAINT.json)
- 📑 [Master Research Index](research/MASTER_RESEARCH_INDEX.json)

</details>

<details>
<summary><b>🔍 For Understanding Findings</b></summary>

- ✅ [100% Verification](research/FINAL_100_PERCENT_VERIFIED.json)
- 📊 [Research Index](research/RESEARCH_INDEX.json)
- 📁 [VA DPOR Complaint Files](research/va_dpor_complaint/)

</details>

<details>
<summary><b>📊 For Data Analysis</b></summary>

- 🏢 [Firm Data](data/source/skidmore_all_firms_complete.json) - 38 firms
- 🔗 [Connections](research/connections/) - Connection analyses
- ⚠️ [Violations](research/violations/) - Violation findings
- 🔍 [Anomalies](research/anomalies/) - Anomaly reports

</details>

---

## 📖 System Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Multi-state license search, connection analysis, and regulatory compliance investigation |
| **Architecture** | Python-first with unified core modules, ETL pipeline, and optional API/web frontend |
| **Data Flow** | Source → Extract → Clean → Analyze → Research Outputs |

## 🛠️ Installation

```bash
git clone https://github.com/1digitaldesign/kettler-data-analysis.git
cd kettler-data-analysis
pip install -r requirements.txt
python bin/run_pipeline.py
```

> 📘 See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## 💻 Usage

<details>
<summary><b>Full Pipeline</b></summary>

```bash
python bin/run_pipeline.py
```

Runs the complete data processing pipeline:
1. ✅ Data extraction
2. ✅ Data cleaning
3. ✅ Connection analysis
4. ✅ Data validation
5. ✅ Report generation

</details>

<details>
<summary><b>Individual Scripts</b></summary>

```bash
python bin/analyze_connections.py  # Connection analysis
python bin/validate_data.py        # Data validation
python bin/clean_data.py           # Data cleaning
python bin/generate_reports.py     # Report generation
```

</details>

## 📚 Documentation

<details>
<summary><b>Getting Started</b></summary>

- 📘 [INSTALLATION.md](INSTALLATION.md) - Setup guide
- ⚡ [QUICK_START.md](QUICK_START.md) - Quick start
- 📊 [STATUS.md](STATUS.md) - Current status

</details>

<details>
<summary><b>System Documentation</b></summary>

- 🏗️ [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
- 🔄 [Data Flow](docs/DATA_FLOW.md)
- 🧩 [Components](docs/COMPONENTS.md)
- 📁 [Repository Structure](docs/REPOSITORY_STRUCTURE.md)
- 📈 [Diagrams](docs/DIAGRAMS.md)

</details>

<details>
<summary><b>Data Documentation</b></summary>

- 📋 [Schema](data/schema.json) - FK/PK relationships
- 📖 [Data Dictionary](data/DATA_DICTIONARY.md) - Field definitions
- 🧠 [Ontology](data/ONTOLOGY.md) - Conceptual relationships
- 🔗 [Ancestry](data/ANCESTRY.md) - Data lineage
- 📊 [Metadata](data/metadata.json) - Global metadata

</details>

<details>
<summary><b>Complete Index</b></summary>

- 📑 [Documentation Index](docs/INDEX.md) - All documentation

</details>

## 📊 Research Status

![Research](https://img.shields.io/badge/research-100%25%20complete-brightgreen)
![Files](https://img.shields.io/badge/files-350%20JSON%20%2B%2030%20MD-blue)
![States](https://img.shields.io/badge/states-15%20searched-orange)

**100% Complete:** All critical areas documented, evidence compiled, ready for complaint filing.

### Key Statistics

| Metric | Value |
|--------|-------|
| **Total Files** | 350 JSON + 30 MD |
| **Research Categories** | 10 categories |
| **License Searches** | 285 files across 15 states |
| **Firms** | 38 firms |
| **Individual Licenses** | 40+ licenses |
| **Connections** | 100+ connections |

### Key Findings

- ✅ **8 regulatory violations** across 11 states
- ⏱️ **Principal broker gap:** 10.5 years
- 📍 **Geographic violation:** 1,300 miles
- 👥 **16 unlicensed personnel** (7 property managers)
- 💰 **$4.75B property value** under management

## 🏗️ System Structure

```
bin/              # Entry points
scripts/core/     # Unified modules
scripts/analysis/ # Analysis scripts
scripts/etl/      # ETL pipeline
data/             # Data (source, cleaned, vectors)
research/         # Research outputs
docs/             # Documentation
```

## ✨ Features

- 🔍 Multi-state license search
- 🔗 Connection mapping
- 🔍 Anomaly detection
- 📄 Evidence extraction (PDF/Excel)
- 🧮 Vector embeddings
- 📅 Timeline analysis
- ✅ Schema validation

---

**Research Status:** ✅ 100% Complete - Ready for Complaint Filing
