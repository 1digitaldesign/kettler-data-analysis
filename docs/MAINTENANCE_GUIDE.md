# Maintenance

## Maintenance Structure

```mermaid
graph TB
    subgraph "Data Directories"
        RAW[data/raw/<br/>Raw Results<br/>gitignored]
        CLEANED[data/cleaned/<br/>Cleaned Data<br/>gitignored]
    end

    subgraph "Research Outputs"
        RESEARCH[research/<br/>Research Outputs<br/>tracked]
    end

    subgraph "Source Documents"
        EVIDENCE[evidence/<br/>Source Documents]
    end

    RAW --> CLEANED
    CLEANED --> RESEARCH

    style RAW fill:#FFE0B2
    style CLEANED fill:#FFF9C4
    style RESEARCH fill:#E1BEE7
    style EVIDENCE fill:#B3E5FC
```

**Text Structure:**

```
data/raw/         # Raw results (gitignored)
data/cleaned/     # Cleaned data (gitignored)
research/         # Research outputs (tracked)
evidence/         # Source documents
```

## Scripts

- `bin/` - Entry points
- `scripts/core/` - Unified modules
- `scripts/analysis/` - Analysis scripts
- `scripts/extraction/` - Evidence extraction

## Paths

Use `scripts/utils/paths.py` for all file paths.

## Data Flow

```mermaid
flowchart LR
    A[Source Data] --> B[Raw Results]
    B --> C[Cleaned Data]
    C --> D[Research Outputs]

    A --> A1[data/source/]
    B --> B1[data/raw/]
    C --> C1[data/cleaned/]
    D --> D1[research/]

    style A fill:#C8E6C9
    style B fill:#FFE0B2
    style C fill:#FFF9C4
    style D fill:#E1BEE7
```

**Text Flow:**

1. Source data → `data/source/`
2. Raw results → `data/raw/`
3. Cleaned data → `data/cleaned/`
4. Research outputs → `research/{category}/`
