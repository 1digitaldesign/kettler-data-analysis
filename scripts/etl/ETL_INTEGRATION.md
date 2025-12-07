# ETL Integration Guide

## Overview

The vector embedding ETL system has been integrated into the project to automatically process all data types (CSV, JSON, PDF, Excel) and create vector embeddings for semantic search and similarity matching.

## Automatic Integration

The ETL pipeline is automatically triggered in the following scenarios:

1. **Full Pipeline Run**: When running `run_full_pipeline.R`, ETL runs as Step 5
2. **Data Loading**: When using enhanced load functions (see below)
3. **Chat Sessions**: When sourcing `chat_data_hook.R` at the start of analysis scripts

## Usage in Existing Code

### Option 1: Use Enhanced Load Functions

Replace existing data loading with ETL-enhanced versions:

```r
# Instead of:
source("analyze_skidmore_connections.R")
data <- load_skidmore_data()

# Use:
source("scripts/etl/integrate_with_loaders.R")
data <- load_skidmore_data_with_etl()
```

### Option 2: Add Chat Hook

At the beginning of any analysis script:

```r
source("scripts/etl/chat_data_hook.R")
# Now all read.csv() and fromJSON() calls automatically trigger ETL
```

### Option 3: Manual ETL Trigger

```r
source("scripts/etl/auto_etl_hook.R")
auto_run_etl(force = FALSE)  # Check and run if needed
```

## Data Sources Processed

The ETL pipeline processes data from:

1. **Ingress** (`data/raw/`): Raw data files
2. **Egress** (`data/cleaned/`): Cleaned/processed data files
3. **Source** (`data/source/`): Source data files
4. **Research** (`research/`): Research JSON files
5. **Evidence** (`evidence/`): PDF evidence files
6. **Scraped** (`data/scraped/`): Scraped data files

## Vector Store Location

- **Vector Index**: `data/vectors/vector_index.faiss`
- **Metadata**: `data/vectors/metadata.json`
- **Processed Files**: `data/vectors/processed_files.json`
- **ETL Results**: `data/vectors/etl_results.json`

## Querying Vector Embeddings

```r
source("scripts/etl/vector_query.R")

# Search for similar content
results <- query_similar("Caitlin Skidmore license", top_k = 10)
print(results)

# Get statistics
stats <- get_vector_stats()
print(stats)
```

## Initial Setup

Run the initialization script to set up the vector store:

```bash
Rscript scripts/etl/init_vector_store.R
```

Or manually:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run ETL pipeline
python3 scripts/etl/etl_pipeline.py
```

## Performance Considerations

- **Incremental Processing**: Only new/changed files are processed
- **Caching**: Processed files are tracked to avoid reprocessing
- **Fast Search**: FAISS index enables fast similarity search
- **Model**: Uses `all-MiniLM-L6-v2` (384 dimensions, optimized for speed)

## Troubleshooting

### Python Not Found
```bash
# Check Python installation
which python3

# Install dependencies
pip install sentence-transformers faiss-cpu pandas numpy
```

### ETL Not Running Automatically
1. Check that `chat_data_hook.R` is sourced at the start of your script
2. Verify Python dependencies are installed
3. Check `data/vectors/` directory exists and is writable

### Vector Store Not Found
Run initialization:
```bash
Rscript scripts/etl/init_vector_store.R
```

## Integration Points

The ETL system integrates with:

- `run_full_pipeline.R` - Step 5: Vector embeddings
- `analyze_skidmore_connections.R` - Via `load_skidmore_data_with_etl()`
- `scripts/analysis/analyze_all_evidence.R` - Via `load_all_evidence_with_etl()`
- `organize_evidence.R` - Via `load_all_data_with_etl()`

## Future Enhancements

- Real-time ETL on file changes (file watcher)
- Integration with database systems
- Support for additional data formats
- Custom embedding models for domain-specific tasks
