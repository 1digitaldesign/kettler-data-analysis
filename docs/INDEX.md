# Documentation Index

![Index](https://img.shields.io/badge/index-complete-brightgreen)
![Docs](https://img.shields.io/badge/docs-25%2B-blue)

Complete index of all documentation in the repository.

## About this index

This index helps you find documentation quickly. Use it to:

- Discover available documentation
- Navigate to specific topics
- Understand documentation structure
- Find related documents

## Documentation graph

See how all documentation connects:

```mermaid
graph LR
    README[README.md] --> INDEX[INDEX.md]
    INDEX --> ARCH[SYSTEM_ARCHITECTURE.md]
    INDEX --> DATA[DATA_DICTIONARY.md]
    INDEX --> RESEARCH[research/README.md]

    style README fill:#C8E6C9,stroke:#4CAF50,stroke-width:3px
    style INDEX fill:#B3E5FC,stroke:#2196F3,stroke-width:2px
```

> See [DOCUMENTATION_GRAPH.md](DOCUMENTATION_GRAPH.md) for complete interactive graph with 174 nodes and 124 edges.

## Getting started

Essential documentation for new users:

- [README.md](../README.md) - Main overview
- [INSTALLATION.md](../INSTALLATION.md) - Installation and setup
- [QUICK_START.md](../QUICK_START.md) - Quick start guide
- [STATUS.md](../STATUS.md) - Current repository status

## System documentation

Technical documentation about the system:

- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - Complete system architecture (components, data flow, structure, diagrams)
- [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) - Detailed repository structure
- [SYSTEM_ANALYST_GUIDE.md](SYSTEM_ANALYST_GUIDE.md) - System analyst guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [ARCHIVE.md](ARCHIVE.md) - Historical archive (consolidated status files)
- [DOCUMENTATION_ARCHITECTURE_VERIFICATION.md](DOCUMENTATION_ARCHITECTURE_VERIFICATION.md) - Comprehensive verification of documentation-to-code/data alignment

## Data documentation

Documentation about data structure, governance, and management:

### Data structure
- [data/schema.json](../data/schema.json) - Complete schema with FK/PK
- [data/DATA_DICTIONARY.md](../data/DATA_DICTIONARY.md) - Field definitions
- [data/ONTOLOGY.md](../data/ONTOLOGY.md) - Conceptual relationships
- [data/ANCESTRY.md](../data/ANCESTRY.md) - Data lineage
- [data/metadata.json](../data/metadata.json) - Global metadata

### Data governance and cataloging
- [data/DATA_CATALOG.md](../data/DATA_CATALOG.md) - Comprehensive data catalog (discoverability, metadata, quality)
- [data/GOVERNANCE.md](../data/GOVERNANCE.md) - Data governance framework (policies, compliance, security)

### Data directory
- [data/README.md](../data/README.md) - Data directory guide

## Research documentation

Documentation about research outputs:

- [research/README.md](../research/README.md) - Research directory guide
- [research/RESEARCH_INDEX.json](../research/RESEARCH_INDEX.json) - Master file index

## API & deployment

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide

## Documentation graph

- [DOCUMENTATION_GRAPH.md](DOCUMENTATION_GRAPH.md) - Complete documentation network graph (graph theory visualization)
