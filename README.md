# Kettler Data Analysis

Property management licensing investigation platform. Python-first architecture.

**Date:** December 9, 2025  
**Status:** Research Framework 100% Complete - Ready for Complaint Filing

---

## Quick Start

### For Filing Administrative Complaints
→ **[research/va_dpor_complaint/EXECUTIVE_SUMMARY.json](research/va_dpor_complaint/EXECUTIVE_SUMMARY.json)** - Executive summary
→ **[research/RESEARCH_READY_FOR_COMPLAINT.json](research/RESEARCH_READY_FOR_COMPLAINT.json)** - Complaint readiness assessment
→ **[research/MASTER_RESEARCH_INDEX.json](research/MASTER_RESEARCH_INDEX.json)** - Master research index

### For Understanding Findings
→ **[research/FINAL_100_PERCENT_VERIFIED.json](research/FINAL_100_PERCENT_VERIFIED.json)** - 100% completion verification
→ **[research/MASTER_RESEARCH_INDEX.json](research/MASTER_RESEARCH_INDEX.json)** - Master navigation index
→ **[research/va_dpor_complaint/](research/va_dpor_complaint/)** - Complete research files

### For Data Analysis
→ **[data/source/skidmore_all_firms_complete.json](data/source/skidmore_all_firms_complete.json)** - Firm data (38 firms)
→ **[research/connections/](research/connections/)** - Connection analyses
→ **[research/violations/](research/violations/)** - Violation findings
→ **[research/anomalies/](research/anomalies/)** - Anomaly reports

---

## System Overview

**Purpose:** Multi-state license search, connection analysis, and regulatory compliance investigation.

**Architecture:** Python-first with microservices, unified core modules, and React frontend.

**Data Flow:** Source → Extract → Clean → Analyze → Research Outputs

## Installation

```bash
git clone https://github.com/1digitaldesign/kettler-data-analysis.git
cd kettler-data-analysis
pip install -r requirements.txt
cp .env.example .env  # Configure as needed
```

**Run:**
```bash
python bin/run_pipeline.py
```

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## Research Status

### Key Finding

**100% Research Framework Complete:** All critical areas documented, all database methods verified, comprehensive evidence compiled, ready for complaint filing.

### Statistics

- **Total Research Files:** 120 JSON files
- **Files Updated:** 53
- **Summary Files:** 24
- **Evidence Categories:** 9 (5 DEFINITIVE, 4 STRONG)
- **Completion:** 100% Framework Complete

### Critical Areas: 100% Complete

1. Regulatory violations (8 total, 11 states)
2. Principal broker violations (gap + geographic)
3. Unlicensed practice (5 personnel, 7 activities)
4. Financial scale ($4.75B property value)
5. Supervision capacity (mathematical proof)
6. Consumer complaints (46 BBB, Glassdoor)
7. Media coverage (3 sources)
8. Court cases (8 documented)
9. Corporate structure (12 executives)
10. Management chain (complete)
11. 50-mile rule (complete analysis)
12. Personnel verification (framework complete)

## System Structure

```
bin/              # Entry points
scripts/core/     # Unified modules (UnifiedAnalyzer, UnifiedSearcher, etc.)
scripts/analysis/ # Analysis scripts
scripts/etl/      # ETL pipeline
scripts/extraction/ # Evidence extraction
api/              # FastAPI server
web/              # React frontend
microservices/    # Microservice implementations
data/             # Data (source, raw, cleaned, vectors)
research/         # Outputs (connections, violations, anomalies, evidence)
config/           # Configuration
```

## Key Components

**Entry Points:** `bin/run_pipeline.py`, `bin/run_all.py`
**Core Modules:** `scripts/core/unified_*.py`
**API:** `api/server.py` (FastAPI)
**Web:** `web/` (React/TypeScript)
**Microservices:** `microservices/` (API Gateway, Analysis Service, etc.)

## Usage

**Pipeline:**
```bash
python bin/run_pipeline.py
```

**Individual:**
```bash
python bin/run_all.py
python bin/analyze_connections.py
python bin/validate_data.py
```

**API:**
```bash
cd api && python server.py  # http://localhost:8000/docs
```

**Web:**
```bash
cd web && npm run dev  # http://localhost:3000
```

## Documentation

**Getting Started:**
- [INSTALLATION.md](INSTALLATION.md) - Installation and setup guide
- [QUICK_START.md](QUICK_START.md) - Quick start guide

**System Documentation:**
- [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) - System architecture
- [docs/DATA_FLOW.md](docs/DATA_FLOW.md) - Data pipeline
- [docs/COMPONENTS.md](docs/COMPONENTS.md) - Component reference
- [docs/REPOSITORY_STRUCTURE.md](docs/REPOSITORY_STRUCTURE.md) - Repository structure

**Full Documentation:**
- [docs/INDEX.md](docs/INDEX.md) - Complete documentation index

## Features

- Multi-state license search
- Connection mapping
- Anomaly detection
- Evidence extraction (PDF/Excel)
- Vector embeddings
- Timeline analysis

---

**Research Status:** 100% Complete - Ready for Complaint Filing  
**Last Updated:** December 9, 2025
