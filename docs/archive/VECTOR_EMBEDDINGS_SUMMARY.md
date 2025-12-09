# Vector Embeddings and ETL Pipeline - Implementation Summary

## Overview

A comprehensive vector embedding system and ETL/ELT pipeline has been added to automatically process all data types (CSV, JSON, PDF, Excel) and create vector embeddings for semantic search and similarity matching.

## What Was Created

### Python Components (`scripts/etl/`)

1. **`vector_embeddings.py`** - Core vector embedding system
   - Creates embeddings using sentence-transformers (`all-MiniLM-L6-v2`)
   - Stores embeddings in FAISS vector index
   - Provides similarity search functionality
   - Handles CSV, JSON, PDF, and Excel data

2. **`etl_pipeline.py`** - ETL pipeline orchestrator
   - Processes all data sources (ingress, egress, source, research, evidence, scraped)
   - Tracks processed files to avoid reprocessing
   - Supports incremental processing
   - Command-line interface for flexible usage

### R Components (`scripts/etl/`)

3. **`vector_query.R`** - R interface for querying embeddings
   - Query similar content
   - Get vector store statistics
   - Run ETL pipeline from R

4. **`auto_etl_hook.R`** - Automatic ETL trigger
   - Checks if ETL needs to run
   - Processes files when data is accessed
   - Tracks last run time

5. **`chat_data_hook.R`** - Chat session integration
   - Overrides `read.csv()` and `fromJSON()` to auto-trigger ETL
   - Runs automatically when data is loaded in chat sessions

6. **`integrate_with_loaders.R`** - Integration with existing loaders
   - Enhanced versions of existing data loading functions
   - Automatic ETL triggering

7. **`init_vector_store.R`** - Initialization script
   - Checks dependencies
   - Sets up vector store
   - Runs initial ETL

8. **`test_etl.R`** - Test script
   - Verifies system setup
   - Checks dependencies
   - Tests Python imports

### Documentation

9. **`README.md`** - Comprehensive usage guide
10. **`ETL_INTEGRATION.md`** - Integration guide for existing code

## Integration Points

### Main Pipeline
- **`run_full_pipeline.R`** - Added Step 5: Vector Embeddings
  - Automatically runs ETL pipeline after data cleaning
  - Creates embeddings for all processed data

### Data Loading
- Enhanced load functions available via `integrate_with_loaders.R`
- Automatic hooks via `chat_data_hook.R`
- Manual triggers via `auto_etl_hook.R`

## Data Flow

```
Ingress (data/raw/)          → Vector Embeddings
Egress (data/cleaned/)       → Vector Embeddings
Source (data/source/)        → Vector Embeddings
Research (research/)         → Vector Embeddings
Evidence (evidence/)         → Vector Embeddings
Scraped (data/scraped/)     → Vector Embeddings
                                    ↓
                            FAISS Vector Store
                                    ↓
                            Similarity Search
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `sentence-transformers` - For embeddings
- `faiss-cpu` - For vector search
- `pandas`, `numpy` - For data processing

### 2. Initialize Vector Store

```bash
Rscript scripts/etl/init_vector_store.R
```

Or manually:
```bash
python3 scripts/etl/etl_pipeline.py
```

### 3. Use in Your Code

**Option A: Chat Hook (Recommended)**
```r
source("scripts/etl/chat_data_hook.R")
# Now all data loading automatically triggers ETL
data <- read.csv("data/source/file.csv")
```

**Option B: Enhanced Loaders**
```r
source("scripts/etl/integrate_with_loaders.R")
data <- load_skidmore_data_with_etl()
```

**Option C: Manual Trigger**
```r
source("scripts/etl/auto_etl_hook.R")
auto_run_etl(force = FALSE)
```

### 4. Query Similar Content

```r
source("scripts/etl/vector_query.R")
results <- query_similar("Caitlin Skidmore", top_k = 10)
print(results)
```

## File Structure

```
scripts/etl/
├── vector_embeddings.py      # Core embedding system
├── etl_pipeline.py           # ETL orchestrator
├── vector_query.R            # R query interface
├── auto_etl_hook.R           # Auto ETL trigger
├── chat_data_hook.R          # Chat session hook
├── integrate_with_loaders.R  # Loader integration
├── init_vector_store.R       # Initialization script
├── test_etl.R               # Test script
├── README.md                 # Usage guide
└── ETL_INTEGRATION.md        # Integration guide

data/vectors/
├── vector_index.faiss        # FAISS vector index
├── metadata.json             # Embedding metadata
├── processed_files.json      # Processed files list
├── etl_results.json          # ETL results
└── last_etl_run.json         # Last run timestamp
```

## Key Features

1. **Automatic Processing**: ETL runs automatically when data is accessed
2. **Incremental Updates**: Only processes new/changed files
3. **Multiple Data Types**: Supports CSV, JSON, PDF, Excel
4. **Fast Search**: FAISS index enables fast similarity search
5. **R Integration**: Full R interface for querying and management
6. **Chat Integration**: Automatic ETL in chat sessions

## Usage Examples

### Process Specific File
```bash
python3 scripts/etl/etl_pipeline.py --file data/raw/sample.csv
```

### Process Directory
```bash
python3 scripts/etl/etl_pipeline.py --dir data/research
```

### Force Reprocessing
```bash
python3 scripts/etl/etl_pipeline.py --force
```

### Query from R
```r
source("scripts/etl/vector_query.R")
results <- query_similar("license violation", top_k = 5)
```

### Get Statistics
```r
stats <- get_vector_stats()
print(stats)
```

## Technical Details

- **Embedding Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Vector Store**: FAISS IndexFlatL2 (L2 distance)
- **Storage**: Persistent to disk (`data/vectors/`)
- **Performance**: Fast similarity search, incremental processing

## Next Steps

1. Run initialization: `Rscript scripts/etl/init_vector_store.R`
2. Test the system: `Rscript scripts/etl/test_etl.R`
3. Integrate into your workflows using the chat hook or enhanced loaders
4. Query embeddings for semantic search and similarity matching

## Troubleshooting

See `scripts/etl/README.md` and `scripts/etl/ETL_INTEGRATION.md` for detailed troubleshooting guides.

## Notes

- The system is conservative and only processes files that haven't been processed
- Vector store is persisted to disk for reuse across sessions
- ETL runs automatically but can be manually triggered if needed
- All data types are supported: CSV, JSON, PDF, Excel
