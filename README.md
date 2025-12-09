# Kettler Data Analysis

A comprehensive data analysis platform for investigating property management firm licensing, connections, and regulatory compliance across all 50 US states.

## 🎯 Overview

This project provides automated tools to:
- **Search** state licensing databases (DPOR) across all 50 states
- **Analyze** connections between firms, individuals, and license patterns
- **Extract** evidence from PDFs, Excel files, and web sources
- **Validate** data quality and flag anomalies
- **Generate** comprehensive reports and visualizations
- **Vectorize** documents for semantic search and analysis

## 🏗️ Architecture

The project uses a **Python-first** architecture with:
- **Unified Core Modules** - Consolidated analysis, search, validation, and reporting
- **Microservices** - API gateway, analysis service, and Google Drive integration
- **ETL Pipeline** - Vector embeddings and data processing
- **Web Application** - React/TypeScript frontend for interactive analysis
- **Docker & Kubernetes** - Containerized deployment

## 📁 Project Structure

```
.
├── bin/                    # Entry point scripts
│   ├── run_pipeline.py     # Main pipeline runner
│   ├── run_all.py          # Run all analyses
│   ├── analyze_connections.py
│   ├── validate_data.py
│   ├── generate_reports.py
│   ├── organize_evidence.py
│   └── clean_data.py
│
├── scripts/                # Core library modules
│   ├── core/               # Unified analysis modules
│   │   ├── unified_analysis.py
│   │   ├── unified_search.py
│   │   ├── unified_validation.py
│   │   ├── unified_reporting.py
│   │   └── unified_investigation.py
│   ├── analysis/           # Analysis scripts
│   ├── extraction/        # Evidence extraction
│   ├── etl/                # ETL and vectorization
│   ├── microservices/      # Microservice implementations
│   └── utils/              # Utility functions
│
├── data/                   # Data directories
│   ├── source/             # Source data files
│   ├── raw/                # Raw search results
│   ├── cleaned/            # Cleaned data
│   ├── analysis/           # Analysis outputs
│   ├── scraped/            # Scraped web data
│   └── vectors/            # Vector embeddings
│
├── research/               # Research outputs (organized by category)
│   ├── connections/        # Connection analyses
│   ├── violations/         # Violation findings
│   ├── anomalies/          # Anomaly reports
│   ├── evidence/           # Evidence summaries
│   ├── verification/       # Verification results
│   ├── timelines/          # Timeline analyses
│   ├── summaries/          # Summary reports
│   └── search_results/     # Search result files
│
├── api/                    # FastAPI server
├── web/                    # React/TypeScript frontend
├── microservices/          # Microservice implementations
├── evidence/               # Source evidence documents
├── filings/                # Filing materials
├── docs/                   # Documentation
└── config/                 # Configuration files
```

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8+ (primary language)
- **Node.js** 18+ (for web application)
- **Docker** (optional, for containerized deployment)

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
   # Edit .env with your configuration
   ```

4. **Install web dependencies** (optional)
   ```bash
   cd web
   npm install
   ```

### Running the Pipeline

**Option 1: Run complete pipeline**
```bash
python bin/run_pipeline.py
```

**Option 2: Run individual components**
```bash
# Run all analyses
python bin/run_all.py

# Analyze connections
python bin/analyze_connections.py

# Validate data
python bin/validate_data.py

# Generate reports
python bin/generate_reports.py

# Organize evidence
python bin/organize_evidence.py
```

**Option 3: Use unified modules**
```python
from scripts.core.unified_analysis import UnifiedAnalyzer

analyzer = UnifiedAnalyzer()
analyzer.load_all_data()
results = analyzer.analyze_all()
```

### Running the Web Application

```bash
cd web
npm run dev
# Open http://localhost:3000
```

### Running the API Server

```bash
cd api
python server.py
# API docs at http://localhost:8000/docs
```

## 🔧 Key Features

### Unified Analysis
- **Connection Analysis** - Identify relationships between firms and individuals
- **Anomaly Detection** - Flag suspicious patterns and gaps
- **Timeline Analysis** - Track events and identify patterns over time
- **Evidence Extraction** - Extract structured data from PDFs and Excel files

### Data Processing
- **Vector Embeddings** - Semantic search using Hugging Face models
- **Data Validation** - Quality checks and duplicate detection
- **ETL Pipeline** - Automated data transformation and loading

### Microservices
- **API Gateway** - Centralized API routing
- **Analysis Service** - Distributed analysis processing
- **Google Drive Integration** - Access and process Drive files

## 📊 Data Sources

### Source Data
- `data/source/skidmore_all_firms_complete.json` - Complete firm data (38 firms)
- `data/source/skidmore_individual_licenses.json` - Individual license records

### Research Outputs
- `research/connections/` - Connection analyses and matrices
- `research/violations/` - Violation findings and UPL evidence
- `research/anomalies/` - Anomaly reports and fraud indicators
- `research/evidence/` - Extracted evidence summaries

## 🛠️ Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python tests/test_unified_modules.py
```

### Code Quality
```bash
# Format code
black scripts/ bin/

# Lint code
flake8 scripts/ bin/
```

### Docker Deployment
```bash
# Build images
make build

# Start services
make up

# View logs
make logs
```

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started quickly
- **[Architecture Guide](ARCHITECTURE_GUIDE.md)** - System architecture
- **[Organization Guide](docs/ORGANIZATION.md)** - Repository structure
- **[Microservices Architecture](MICROSERVICES_ARCHITECTURE.md)** - Microservices design
- **[API Documentation](api/README.md)** - API endpoints
- **[Web Application Guide](web/README.md)** - Frontend documentation

## 🔍 Key Analysis Capabilities

1. **Multi-State License Search** - Automated searches across all 50 states
2. **Connection Mapping** - Identify relationships through addresses, brokers, and licenses
3. **Anomaly Detection** - Flag suspicious patterns and gaps
4. **Evidence Extraction** - Extract structured data from documents
5. **Timeline Analysis** - Track events and identify patterns
6. **Vector Search** - Semantic search across documents

## 📈 Output Files

### Analysis Outputs
- `data/analysis/dpor_skidmore_connections.csv` - All identified connections
- `data/analysis/dpor_validated.csv` - Validated data with quality flags
- `data/analysis/analysis_summary.json` - Summary statistics
- `data/analysis/data_quality_report.json` - Quality metrics

### Research Outputs
- `research/connections/connection_matrix.json` - Connection matrix
- `research/violations/all_violations_compiled.json` - Compiled violations
- `research/anomalies/all_anomalies_consolidated.json` - Consolidated anomalies
- `research/timelines/timeline_analysis.json` - Timeline analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is for research and analysis purposes.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- FastAPI for the API framework
- React/TypeScript for the web interface

## 📞 Support

For questions or issues, please open an issue on GitHub.
