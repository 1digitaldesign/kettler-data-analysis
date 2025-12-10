# Data Ontology

![Ontology](https://img.shields.io/badge/ontology-complete-brightgreen)
![Entities](https://img.shields.io/badge/entities-7-blue)
![Relationships](https://img.shields.io/badge/relationships-9-orange)

Conceptual model defining core entities, relationships, and properties in the Kettler Data Analysis domain.

## Overview

This ontology describes the semantic structure of the data, focusing on **what** entities exist, **how** they relate to each other, and **what properties** they possess.

> 📘 Complements [Data Dictionary](./DATA_DICTIONARY.md) (technical field definitions) and [Schema](./schema.json) (FK/PK relationships).

## Core Concepts

### Entity Types

<details>
<summary><b>1. Firm</b> (`Firm`)</summary>

A licensed real estate firm entity.

**Properties:**
- ✅ Unique license number (10-digit Virginia DPOR)
- ✅ Legal name
- ✅ Business address
- ✅ Principal broker (Individual)
- ✅ License dates (initial certification, expiration)
- ✅ State jurisdiction

**Key Characteristics:**
- Primary identifier: `firm_license`
- Can have multiple connections to other firms
- Can be associated with violations
- Can be analyzed in research outputs

</details>

<details>
<summary><b>2. Individual</b> (`Individual`)</summary>

A person holding a real estate license.

**Properties:**
- ✅ Unique license number (10-digit)
- ✅ Name
- ✅ Address
- ✅ License type
- ✅ Regulatory board
- ✅ State jurisdiction
- ✅ License expiration date

**Key Characteristics:**
- Primary identifier: `license_number`
- Can be a principal broker for firms
- Can have multiple licenses (different states/types)
- Can be connected to firms
- Can be associated with violations

</details>

<details>
<summary><b>3. License</b> (`License`)</summary>

A regulatory authorization to practice real estate.

**Properties:**
- ✅ License number
- ✅ Type (Firm or Individual)
- ✅ State jurisdiction
- ✅ Dates (certification, expiration)
- ✅ Regulatory board

**Key Characteristics:**
- Can be a Firm License or Individual License
- Has temporal validity (expiration dates)
- Subject to regulatory oversight

</details>

<details>
<summary><b>4. Connection</b> (`Connection`)</summary>

A relationship between entities (firm-to-firm, firm-to-individual).

**Properties:**
- ✅ Connection type
- ✅ Connection details
- ✅ State context
- ✅ Verification status
- ✅ Analysis date

**Key Characteristics:**
- Represents various relationship types
- Can be verified or unverified
- Temporal (can change over time)

</details>

<details>
<summary><b>5. Violation</b> (`Violation`)</summary>

A regulatory violation identified through analysis.

**Properties:**
- ✅ Violation type
- ✅ Severity level
- ✅ Description
- ✅ Evidence files
- ✅ Identified date
- ✅ State jurisdiction

**Key Characteristics:**
- Can be associated with firms or individuals
- Has severity classification (High, Medium, Low)
- Supported by evidence
- Temporal (identified at a specific date)

</details>

<details>
<summary><b>6. Evidence</b> (`Evidence`)</summary>

A document or data source supporting research findings.

**Properties:**
- ✅ File path
- ✅ Evidence type
- ✅ Extracted data
- ✅ Extraction date
- ✅ Source description

**Key Characteristics:**
- Can support violations
- Can be various types (PDF, Excel, Email, etc.)
- Contains extracted entities and data
- Temporal (extracted at a specific date)

</details>

<details>
<summary><b>7. Research Output</b> (`ResearchOutput`)</summary>

An analysis result or finding from research activities.

**Properties:**
- ✅ Category
- ✅ File path
- ✅ Analysis date
- ✅ Findings summary
- ✅ Status
- ✅ Metadata

**Key Characteristics:**
- Can reference firms or individuals
- Categorized by research type
- Has completion status
- Temporal (analyzed at a specific date)

</details>

## Relationships

### Primary Relationships

<details>
<summary><b>Firm HAS Principal Broker</b> (`Firm` → `Individual`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Firm (1) → Individual (0..1)
- **Properties:** Principal broker name stored on firm
- **FK:** `firms.individual_license` → `individual_licenses.license_number` (optional)

</details>

<details>
<summary><b>Individual HOLDS License</b> (`Individual` → `License`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Individual (1) → License (1..*)
- **Properties:** License number is primary identifier

</details>

<details>
<summary><b>Firm CONNECTED_TO Firm</b> (`Firm` → `Firm`)</summary>

- **Type:** Many-to-Many (via Connection entity)
- **Cardinality:** Firm (1) → Connection (0..*) → Firm (1)
- **Properties:** Connection type, details, verification status

</details>

<details>
<summary><b>Firm CONNECTED_TO Individual</b> (`Firm` → `Individual`)</summary>

- **Type:** Many-to-Many (via Connection entity)
- **Cardinality:** Firm (1) → Connection (0..*) → Individual (1)
- **Properties:** Connection type (e.g., "Principal Broker")

</details>

<details>
<summary><b>Firm VIOLATES Regulation</b> (`Firm` → `Violation`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Firm (1) → Violation (0..*)
- **Properties:** Violation type, severity, description

</details>

<details>
<summary><b>Individual VIOLATES Regulation</b> (`Individual` → `Violation`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Individual (1) → Violation (0..*)
- **Properties:** Violation type, severity, description

</details>

<details>
<summary><b>Violation SUPPORTED_BY Evidence</b> (`Violation` → `Evidence`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Violation (1) → Evidence (0..*)
- **Properties:** Evidence type, extracted data, source

</details>

<details>
<summary><b>Firm ANALYZED_IN Research</b> (`Firm` → `ResearchOutput`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Firm (1) → ResearchOutput (0..*)
- **Properties:** Research category, findings summary, analysis date

</details>

<details>
<summary><b>Individual ANALYZED_IN Research</b> (`Individual` → `ResearchOutput`)</summary>

- **Type:** One-to-Many
- **Cardinality:** Individual (1) → ResearchOutput (0..*)
- **Properties:** Research category, findings summary, analysis date

</details>

## Concept Hierarchy

```mermaid
graph TB
    Entity[Entity]
    Entity --> Firm[Firm<br/>firm_license]
    Entity --> Individual[Individual<br/>license_number]
    Entity --> License[License<br/>license_number]
    Entity --> Connection[Connection<br/>connection_id]
    Entity --> Violation[Violation<br/>violation_id]
    Entity --> Evidence[Evidence<br/>evidence_id]
    Entity --> Research[ResearchOutput<br/>research_id]

    Firm -->|HAS| Individual
    Individual -->|HOLDS| License
    Firm -->|CONNECTED_TO| Connection
    Individual -->|CONNECTED_TO| Connection
    Firm -->|VIOLATES| Violation
    Individual -->|VIOLATES| Violation
    Violation -->|SUPPORTED_BY| Evidence
    Firm -->|ANALYZED_IN| Research
    Individual -->|ANALYZED_IN| Research

    style Firm fill:#FFE5E5
    style Individual fill:#E5F3FF
    style License fill:#E5FFE5
    style Connection fill:#FFF5E5
    style Violation fill:#FFE5F5
    style Evidence fill:#F5E5FF
    style Research fill:#E5FFFF
```

## Relationship Cardinalities

| From Entity | Relationship | To Entity | Cardinality | Notes |
|-------------|--------------|-----------|-------------|-------|
| Firm | HAS Principal Broker | Individual | 1:0..1 | One firm has one principal broker (optional FK) |
| Individual | HOLDS | License | 1:1..* | One individual can hold multiple licenses |
| Firm | CONNECTED_TO | Firm | 1:0..* | Via Connection entity (many-to-many) |
| Firm | CONNECTED_TO | Individual | 1:0..* | Via Connection entity (many-to-many) |
| Firm | VIOLATES | Violation | 1:0..* | One firm can have multiple violations |
| Individual | VIOLATES | Violation | 1:0..* | One individual can have multiple violations |
| Violation | SUPPORTED_BY | Evidence | 1:0..* | One violation can have multiple evidence files |
| Firm | ANALYZED_IN | ResearchOutput | 1:0..* | One firm can be analyzed in multiple research outputs |
| Individual | ANALYZED_IN | ResearchOutput | 1:0..* | One individual can be analyzed in multiple research outputs |

## Business Rules

<details>
<summary><b>License Rules</b></summary>

1. ✅ Every firm must have a principal broker
2. ✅ License numbers are unique within their type (Firm vs Individual)
3. ✅ Licenses have expiration dates; expired licenses may still be relevant for historical analysis

</details>

<details>
<summary><b>Connection Rules</b></summary>

1. ✅ Connections can be verified or unverified
2. ✅ Connections have specific types that define the relationship
3. ✅ Firm-to-firm connections are bidirectional

</details>

<details>
<summary><b>Violation Rules</b></summary>

1. ✅ Violations should be supported by evidence files
2. ✅ All violations have a severity classification
3. ✅ Violations must be associated with at least one firm or individual

</details>

<details>
<summary><b>Research Rules</b></summary>

1. ✅ All research outputs belong to a category
2. ✅ Research outputs have a completion status
3. ✅ Research outputs can reference firms or individuals (optional)

</details>

## Ontology Diagram

```mermaid
graph TB
    subgraph "Core Entities"
        Firm[Firm<br/>firm_license]
        Individual[Individual<br/>license_number]
        License[License<br/>license_number]
    end

    subgraph "Relationships"
        Connection[Connection<br/>connection_id]
        Violation[Violation<br/>violation_id]
        Evidence[Evidence<br/>evidence_id]
        Research[ResearchOutput<br/>research_id]
    end

    Firm -->|HAS Principal Broker| Individual
    Individual -->|HOLDS| License
    Firm <-->|CONNECTED_TO| Connection
    Individual <-->|CONNECTED_TO| Connection
    Firm -->|VIOLATES| Violation
    Individual -->|VIOLATES| Violation
    Violation -->|SUPPORTED_BY| Evidence
    Firm -->|ANALYZED_IN| Research
    Individual -->|ANALYZED_IN| Research

    style Firm fill:#FFE5E5
    style Individual fill:#E5F3FF
    style License fill:#E5FFE5
    style Connection fill:#FFF5E5
    style Violation fill:#FFE5F5
    style Evidence fill:#F5E5FF
    style Research fill:#E5FFFF
```

## Related Documentation

### Data documentation
- 📚 [Data Catalog](./DATA_CATALOG.md) - Data asset catalog and discoverability
- 🛡️ [Data Governance](./GOVERNANCE.md) - Governance framework and policies
- 📋 [Data Dictionary](./DATA_DICTIONARY.md) - Technical field definitions
- 📊 [Schema Definition](./schema.json) - FK/PK relationships
- 🔗 [Data Ancestry](./ANCESTRY.md) - Data lineage and transformations
- 📄 [Metadata Schema](./metadata.json) - Metadata structure definition
- 📁 [Data README](./README.md) - Data directory guide

### System documentation
- 📑 [Documentation Index](../docs/INDEX.md) - Complete documentation index
- 🏗️ [System Architecture](../docs/SYSTEM_ARCHITECTURE.md) - System architecture overview
- 📁 [Repository Structure](../docs/REPOSITORY_STRUCTURE.md) - File organization
