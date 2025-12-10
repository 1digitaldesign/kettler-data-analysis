# Documentation Graph

![Graph](https://img.shields.io/badge/graph-complete-brightgreen)
![Nodes](https://img.shields.io/badge/nodes-173-blue)
![Edges](https://img.shields.io/badge/edges-110-orange)

Complete graph theory visualization of all documentation files and their relationships. This graph shows how all documentation connects when viewing files on GitHub.

## Interactive Documentation Network

```mermaid
graph TB
    subgraph "Root Documentation"
        README[README.md<br/>Main Overview]
        INSTALL[INSTALLATION.md<br/>Setup Guide]
        QUICK[QUICK_START.md<br/>Quick Start]
        STATUS[STATUS.md<br/>Repository Status]
    end

    subgraph "System Documentation"
        INDEX[docs/INDEX.md<br/>Documentation Index]
        ARCH[docs/SYSTEM_ARCHITECTURE.md<br/>Architecture]
        FLOW[docs/DATA_FLOW.md<br/>Data Pipeline]
        COMP[docs/COMPONENTS.md<br/>Components]
        STRUCT[docs/REPOSITORY_STRUCTURE.md<br/>Repository Structure]
        DIAGRAMS[docs/DIAGRAMS.md<br/>Visual Diagrams]
        ORG[docs/ORGANIZATION.md<br/>Organization]
        GUIDE[docs/SYSTEM_ANALYST_GUIDE.md<br/>System Analyst Guide]
    end

    subgraph "Data Documentation"
        DATA_README[data/README.md<br/>Data Guide]
        DATA_DICT[data/DATA_DICTIONARY.md<br/>Field Definitions]
        ONTOLOGY[data/ONTOLOGY.md<br/>Conceptual Model]
        ANCESTRY[data/ANCESTRY.md<br/>Data Lineage]
        SCHEMA[data/schema.json<br/>Schema Definition]
    end

    subgraph "Research Documentation"
        RESEARCH_README[research/README.md<br/>Research Guide]
        RESEARCH_INDEX[research/RESEARCH_INDEX.json<br/>Research Index]
    end

    README --> INSTALL
    README --> QUICK
    README --> STATUS
    README --> INDEX
    README --> ARCH
    README --> FLOW
    README --> COMP
    README --> DATA_DICT
    README --> ONTOLOGY
    README --> ANCESTRY

    INDEX --> README
    INDEX --> INSTALL
    INDEX --> QUICK
    INDEX --> STATUS
    INDEX --> ARCH
    INDEX --> FLOW
    INDEX --> COMP
    INDEX --> DATA_DICT
    INDEX --> ONTOLOGY
    INDEX --> ANCESTRY
    INDEX --> RESEARCH_README

    ARCH --> DATA_DICT
    ARCH --> SCHEMA
    FLOW --> ARCH
    COMP --> ARCH
    STRUCT --> ARCH
    DIAGRAMS --> ARCH
    DIAGRAMS --> FLOW
    DIAGRAMS --> COMP
    DIAGRAMS --> STRUCT

    DATA_README --> DATA_DICT
    DATA_README --> ONTOLOGY
    DATA_README --> ANCESTRY
    DATA_README --> SCHEMA
    DATA_DICT --> ONTOLOGY
    DATA_DICT --> ANCESTRY
    DATA_DICT --> SCHEMA
    ONTOLOGY --> DATA_DICT
    ONTOLOGY --> ANCESTRY
    ANCESTRY --> DATA_DICT
    ANCESTRY --> ONTOLOGY

    RESEARCH_README --> DATA_DICT
    RESEARCH_README --> RESEARCH_INDEX

    INSTALL --> QUICK
    INSTALL --> INDEX
    QUICK --> INSTALL
    QUICK --> INDEX
    STATUS --> README
    STATUS --> RESEARCH_README
    STATUS --> DATA_README
    STATUS --> INDEX

    style README fill:#C8E6C9,stroke:#4CAF50,stroke-width:3px
    style INDEX fill:#B3E5FC,stroke:#2196F3,stroke-width:2px
    style ARCH fill:#B3E5FC
    style FLOW fill:#B3E5FC
    style COMP fill:#B3E5FC
    style DATA_DICT fill:#FFF9C4
    style ONTOLOGY fill:#FFF9C4
    style ANCESTRY fill:#FFF9C4
    style RESEARCH_README fill:#E1BEE7
```

## Documentation Categories

<details>
<summary><b>Root Documentation</b> (4 files)</summary>

- `README.md` - Main project overview
- `INSTALLATION.md` - Installation and setup
- `QUICK_START.md` - Quick start guide
- `STATUS.md` - Current repository status

</details>

<details>
<summary><b>System Documentation</b> (8 files)</summary>

- `docs/INDEX.md` - Complete documentation index
- `docs/SYSTEM_ARCHITECTURE.md` - System architecture
- `docs/DATA_FLOW.md` - Data pipeline
- `docs/COMPONENTS.md` - Component reference
- `docs/REPOSITORY_STRUCTURE.md` - Repository structure
- `docs/DIAGRAMS.md` - Visual diagrams
- `docs/ORGANIZATION.md` - Organization guide
- `docs/SYSTEM_ANALYST_GUIDE.md` - System analyst guide

</details>

<details>
<summary><b>Data Documentation</b> (5 files)</summary>

- `data/README.md` - Data directory guide
- `data/DATA_DICTIONARY.md` - Field definitions
- `data/ONTOLOGY.md` - Conceptual relationships
- `data/ANCESTRY.md` - Data lineage
- `data/schema.json` - Schema definition

</details>

<details>
<summary><b>Research Documentation</b> (2 files)</summary>

- `research/README.md` - Research directory guide
- `research/RESEARCH_INDEX.json` - Master file index

</details>

## Graph Theory Analysis

### Centrality Measures

**Most Connected Nodes (Hub Documents):**
1. `docs/INDEX.md` - Central hub connecting all documentation
2. `README.md` - Entry point with many connections
3. `data/DATA_DICTIONARY.md` - Core data documentation

**Bridge Documents:**
- `docs/SYSTEM_ARCHITECTURE.md` - Connects system and data docs
- `data/README.md` - Connects data and research docs

### Documentation Paths

**From README to Data Documentation:**
```
README.md → docs/INDEX.md → data/DATA_DICTIONARY.md
README.md → data/DATA_DICTIONARY.md (direct)
```

**From README to Research Documentation:**
```
README.md → docs/INDEX.md → research/README.md
README.md → research/README.md (direct)
```

**From System to Data Documentation:**
```
docs/SYSTEM_ARCHITECTURE.md → data/DATA_DICTIONARY.md
docs/SYSTEM_ARCHITECTURE.md → data/schema.json
```

## Link Validation

<details>
<summary><b>Link Checker</b></summary>

Run the link checker to verify all links:

```bash
python scripts/utils/check_doc_links.py
```

This will:
- ✅ Check all internal links
- ✅ Identify broken links
- ✅ Generate documentation graph
- ✅ Create Mermaid visualization

</details>

## Navigation Tips

**Starting Points:**
- 🏠 **New Users:** Start with `README.md` → `QUICK_START.md`
- 📚 **Developers:** Start with `README.md` → `docs/SYSTEM_ARCHITECTURE.md`
- 📊 **Data Analysts:** Start with `README.md` → `data/DATA_DICTIONARY.md`
- 🔍 **Researchers:** Start with `README.md` → `research/README.md`

**Documentation Hub:**
- 📑 `docs/INDEX.md` - Central index of all documentation

**Quick Navigation:**
- Use the graph above to see relationships
- Click any node to navigate to that document
- Follow edges to discover related documentation

## Graph Statistics

| Metric | Value |
|--------|-------|
| **Total Nodes** | 173 documentation files |
| **Total Edges** | 110 links between files |
| **Categories** | 6 (root, system, data, research, guide, other) |
| **Average Connections** | 0.64 per node |
| **Hub Documents** | 3 (INDEX.md, README.md, DATA_DICTIONARY.md) |

## Related

- [Documentation Index](INDEX.md) - Complete index
- [Repository Structure](REPOSITORY_STRUCTURE.md) - File organization
- [System Architecture](SYSTEM_ARCHITECTURE.md) - Architecture details
