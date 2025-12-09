# Quick Start Guide

**Last Updated:** December 9, 2025

## Getting Started

### Prerequisites

1. **Python** (version 3.8+)
2. **Node.js** (version 18+, optional for web app)
3. **Docker** (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kettler-data-analysis.git
   cd kettler-data-analysis
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   # - GCP credentials (for Google Drive API)
   # - Hugging Face tokens (for data cleaning)
   ```

4. **Install web dependencies** (optional)
   ```bash
   cd web
   npm install
   ```

## Running the Pipeline

### Option 1: Run Complete Pipeline

```bash
python bin/run_pipeline.py
```

This runs the complete analysis pipeline:
- Data loading and validation
- Connection analysis
- Anomaly detection
- Report generation

### Option 2: Run Individual Components

1. **Run all analyses:**
   ```bash
   python bin/run_all.py
   ```

2. **Analyze connections:**
   ```bash
   python bin/analyze_connections.py
   ```

3. **Validate data:**
   ```bash
   python bin/validate_data.py
   ```

4. **Generate reports:**
   ```bash
   python bin/generate_reports.py
   ```

5. **Organize evidence:**
   ```bash
   python bin/organize_evidence.py
   ```

### Option 3: Use Unified Modules

```python
from scripts.core.unified_analysis import UnifiedAnalyzer

# Initialize analyzer
analyzer = UnifiedAnalyzer()

# Load all data
analyzer.load_all_data()

# Run all analyses
results = analyzer.analyze_all()

# Save results
analyzer.save_results()
```

## Running the Web Application

```bash
cd web
npm run dev
```

Open http://localhost:3000 in your browser.

## Running the API Server

```bash
cd api
python server.py
```

API documentation available at http://localhost:8000/docs

## Directory Structure Quick Reference

- **`bin/`** - Entry point scripts (run these)
- **`scripts/core/`** - Unified analysis modules
- **`scripts/analysis/`** - Analysis scripts
- **`scripts/extraction/`** - Evidence extraction
- **`scripts/etl/`** - ETL and vectorization
- **`data/`** - Data files
  - `source/` - Original source data
  - `raw/` - Raw search results
  - `cleaned/` - Cleaned data
  - `analysis/` - Analysis outputs
- **`research/`** - Research outputs
  - `connections/` - Connection analyses
  - `violations/` - Violation findings
  - `anomalies/` - Anomaly reports
  - `evidence/` - Evidence summaries
  - `verification/` - Verification results
- **`config/`** - Configuration files
- **`docs/`** - Documentation

## Common Tasks

### Find Connection Analyses
```bash
ls research/connections/
```

### Find Violation Evidence
```bash
ls research/violations/
```

### View Evidence Summaries
```bash
ls research/evidence/
```

### Check Verification Results
```bash
ls research/verification/
```

## Configuration

### State Registry
Located at: `config/state_dpor_registry.csv`

### Environment Variables
Copy `.env.example` to `.env` and configure:
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to GCP credentials
- `HUGGINGFACE_TOKEN` - Hugging Face API token
- `GCP_PROJECT_ID` - Google Cloud Project ID

## Documentation

- **[README.md](README.md)** - Main project documentation
- **[Architecture Guide](ARCHITECTURE_GUIDE.md)** - System architecture
- **[Organization Guide](docs/ORGANIZATION.md)** - Repository structure
- **[Microservices Architecture](MICROSERVICES_ARCHITECTURE.md)** - Microservices design

## Troubleshooting

### Import Errors
If you get import errors:
1. Ensure you're running from the project root directory
2. Check that `scripts/` directory exists
3. Verify Python path includes project root

### Missing Dependencies
If dependencies are missing:
```bash
pip install -r requirements.txt
```

### Path Errors
If you get path-related errors:
1. Check that you're running from project root
2. Verify directory structure matches expected layout
3. Check `scripts/utils/paths.py` for path configuration

### Missing Data Files
If data files aren't found:
1. Check `data/source/` for source files
2. Run extraction scripts to generate data
3. Check `data/analysis/` for analysis outputs

## Next Steps

1. Review the [README.md](README.md) for detailed information
2. Explore the [Architecture Guide](ARCHITECTURE_GUIDE.md)
3. Check out the [web application](web/README.md)
4. Review [API documentation](api/README.md)
