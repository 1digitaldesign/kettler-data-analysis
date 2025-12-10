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

- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - System architecture
- [DATA_FLOW.md](DATA_FLOW.md) - Data pipeline
- [COMPONENTS.md](COMPONENTS.md) - Component reference
- [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) - Repository structure
- [SYSTEM_ANALYST_GUIDE.md](SYSTEM_ANALYST_GUIDE.md) - System analyst guide
- [ORGANIZATION.md](ORGANIZATION.md) - Repository organization
- [DIAGRAMS.md](DIAGRAMS.md) - Visual diagrams

## Data documentation

Documentation about data structure and meaning:

- [data/schema.json](../data/schema.json) - Complete schema with FK/PK
- [data/DATA_DICTIONARY.md](../data/DATA_DICTIONARY.md) - Field definitions
- [data/ONTOLOGY.md](../data/ONTOLOGY.md) - Conceptual relationships
- [data/ANCESTRY.md](../data/ANCESTRY.md) - Data lineage
- [data/metadata.json](../data/metadata.json) - Global metadata
- [data/README.md](../data/README.md) - Data directory guide

## Research documentation

Documentation about research outputs:

- [research/README.md](../research/README.md) - Research directory guide
- [research/RESEARCH_INDEX.json](../research/RESEARCH_INDEX.json) - Master file index

## API & deployment

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide

## Documentation graph

- [DOCUMENTATION_GRAPH.md](DOCUMENTATION_GRAPH.md) - Complete documentation network graph (graph theory visualization)
