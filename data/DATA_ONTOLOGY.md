# Data Ontology

**Version:** 1.0.0
**Last Updated:** 2025-12-08
**Status:** Active

## Overview

This document defines the data ontology for the Kettler Data Analysis project. An ontology provides a formal representation of the concepts, entities, relationships, and terminology used throughout the data architecture. It serves as the semantic foundation for data understanding, integration, and governance.

## Purpose

- **Semantic Clarity**: Establish clear definitions for all data concepts
- **Interoperability**: Enable consistent data interpretation across systems
- **Governance**: Provide foundation for data quality and compliance
- **Discovery**: Facilitate data discovery and understanding
- **Integration**: Support data integration and transformation

## Core Concepts

### 1. Entity Types

#### 1.1 Firm (Business Entity)
**Definition**: A legal business entity licensed to conduct real estate operations.

**Attributes**:
- `firm_license` (Identifier): Unique license number issued by regulatory authority
- `firm_name` (Name): Legal business name
- `firm_type` (Classification): Legal entity structure (Corporation, LLC, LP, etc.)
- `address` (Location): Business address
- `state` (Jurisdiction): State where license is issued
- `dba_name` (Alias): "Doing Business As" name if applicable

**Relationships**:
- Has Principal Broker → Individual
- Has License → License Record
- Located In → State/Jurisdiction
- Connected To → Other Firms (via connections)

**Constraints**:
- Must have valid license number (10 digits)
- Must have principal broker assigned
- License must be active (not expired)

#### 1.2 Individual (Person)
**Definition**: A licensed real estate professional.

**Attributes**:
- `license_number` (Identifier): Unique license number
- `name` (Name): Full legal name
- `address` (Location): Address associated with license
- `license_type` (Classification): Type of license (Individual)

**Relationships**:
- Licensed In → State/Jurisdiction
- Serves As → Principal Broker (for firms)
- Has License → License Record

**Constraints**:
- Name must match official records
- License must be valid

#### 1.3 License (Regulatory Record)
**Definition**: A regulatory authorization to conduct real estate business.

**Attributes**:
- `license_number` (Identifier): Unique license identifier
- `license_type` (Classification): Firm or Individual license
- `initial_cert_date` (Temporal): Date license was first issued
- `expiration_date` (Temporal): Date license expires
- `state` (Jurisdiction): Issuing state
- `board` (Authority): Regulatory board

**Relationships**:
- Issued To → Firm or Individual
- Issued By → Regulatory Authority
- Valid In → State/Jurisdiction

**Constraints**:
- Expiration date must be after initial certification date
- License number must be unique within jurisdiction

#### 1.4 Connection (Relationship)
**Definition**: A relationship between two entities indicating shared characteristics or associations.

**Attributes**:
- `connection_type` (Classification): Type of connection
  - Same Address
  - Same Principal Broker
  - Same License Date
  - Other
- `connection_strength` (Measure): Strength of connection (0-1 scale)
- `connection_detail` (Description): Detailed explanation of connection

**Relationships**:
- Connects → Firm to Firm
- Based On → Shared Attribute

**Constraints**:
- Must connect two distinct entities
- Connection type must be valid

#### 1.5 Listing (Property Listing)
**Definition**: A short-term rental property listing from various platforms.

**Attributes**:
- `listing_id` (Identifier): Unique listing identifier
- `platform` (Source): Platform where listing appears
- `property_address` (Location): Property address
- `property_name` (Name): Listing title/name
- `scraped_date` (Temporal): Date listing was scraped

**Relationships**:
- Listed On → Platform
- Located At → Address
- Managed By → Firm (potential)

**Constraints**:
- Must have valid address
- Platform must be recognized

### 2. Classification Systems

#### 2.1 Firm Type Taxonomy
```
Firm Type
├── Corporation
├── Limited Liability Company (LLC)
│   ├── LLC - Limited Liability Company
│   └── Solely owned LLC
├── Limited Partnership (LP)
│   ├── LP - Limited Partnership
│   └── LLP - Limited Liability Partnership
└── Other
```

#### 2.2 License Type Taxonomy
```
License Type
├── Real Estate Firm License
└── Real Estate Individual License
```

#### 2.3 Connection Type Taxonomy
```
Connection Type
├── Same Address
├── Same Principal Broker
├── Same License Date
└── Other
```

#### 2.4 Platform Taxonomy
```
Platform
├── Airbnb
├── VRBO
├── Front Website
└── Other
```

### 3. Temporal Concepts

#### 3.1 License Timeline
- **Initial Certification Date**: When license was first issued
- **Expiration Date**: When license expires
- **Gap Years**: Years between firm license and principal broker license
- **Verification Date**: When data was verified/updated

#### 3.2 Data Lifecycle
- **Collection Date**: When data was collected
- **Scraped Date**: When data was scraped
- **Verification Date**: When data was verified
- **Last Updated**: When data was last modified

### 4. Geographic Concepts

#### 4.1 Jurisdiction Hierarchy
```
Jurisdiction
├── Federal (US)
├── State
│   ├── VA (Virginia)
│   ├── TX (Texas)
│   ├── NC (North Carolina)
│   ├── MD (Maryland)
│   └── Other States
└── Local (County/City)
```

#### 4.2 Address Components
- **Street Address**: Street number and name
- **Suite/Unit**: Suite or unit number
- **City**: City name
- **State**: Two-letter state code
- **ZIP Code**: Postal code

### 5. Data Quality Concepts

#### 5.1 Completeness
- **Complete**: All required fields present
- **Incomplete**: Missing required fields
- **Needs Verification**: Data requires manual verification

#### 5.2 Validity
- **Valid**: Data conforms to schema
- **Invalid**: Data violates schema constraints
- **Unknown**: Validity cannot be determined

#### 5.3 Accuracy
- **Verified**: Data verified against source
- **Unverified**: Data not yet verified
- **Estimated**: Data is an estimate

## Relationships

### Primary Relationships

1. **Firm → Individual** (Principal Broker)
   - Type: One-to-Many
   - Cardinality: One firm has one principal broker, one individual can be principal broker for many firms
   - Constraint: Principal broker must be licensed

2. **Firm → License**
   - Type: One-to-One
   - Cardinality: One firm has one license
   - Constraint: License must be active

3. **Individual → License**
   - Type: One-to-Many
   - Cardinality: One individual can have multiple licenses (different states)
   - Constraint: Each license is unique

4. **Firm → Firm** (Connection)
   - Type: Many-to-Many
   - Cardinality: Firms can have multiple connections
   - Constraint: No self-connections

5. **Firm → Address**
   - Type: Many-to-One
   - Cardinality: Multiple firms can share same address
   - Constraint: Address must be valid

6. **Listing → Platform**
   - Type: Many-to-One
   - Cardinality: Multiple listings per platform
   - Constraint: Platform must be recognized

### Derived Relationships

1. **Firm → State** (Jurisdiction)
   - Derived from: License state
   - Type: Many-to-One

2. **Firm → Connection Type**
   - Derived from: Shared attributes
   - Type: Many-to-Many

## Business Rules

### Rule 1: Principal Broker Requirement
- **Rule**: Every firm must have a principal broker
- **Constraint**: Principal broker must be licensed individual
- **Validation**: `principal_broker IS NOT NULL AND principal_broker IN (SELECT name FROM individual_licenses)`

### Rule 2: License Uniqueness
- **Rule**: License numbers must be unique within jurisdiction
- **Constraint**: No duplicate license numbers
- **Validation**: `UNIQUE(license_number, state)`

### Rule 3: License Expiration
- **Rule**: Expiration date must be after initial certification date
- **Constraint**: `expiration_date > initial_cert_date`
- **Validation**: Date comparison

### Rule 4: Address Consistency
- **Rule**: Firms at same address should be investigated for connections
- **Constraint**: Address matching algorithm
- **Validation**: Normalized address comparison

### Rule 5: Gap Year Calculation
- **Rule**: Gap years calculated as difference between firm license date and principal broker license date
- **Constraint**: `gap_years = firm.initial_cert_date - principal_broker.license_date`
- **Validation**: Date arithmetic

## Terminology Dictionary

### Core Terms

| Term | Definition | Synonyms |
|------|------------|----------|
| **Firm** | Legal business entity licensed for real estate operations | Company, Business Entity |
| **Principal Broker** | Licensed individual responsible for firm operations | Broker, License Holder |
| **License** | Regulatory authorization to conduct business | Permit, Certification |
| **Connection** | Relationship between entities based on shared attributes | Relationship, Link |
| **Listing** | Property listing on rental platform | Property, Rental |
| **Jurisdiction** | Geographic area of regulatory authority | State, Region |
| **Gap Years** | Years between firm license and principal broker license | Time Gap, License Gap |

### Data Quality Terms

| Term | Definition |
|------|------------|
| **Complete** | All required fields present |
| **Verified** | Data confirmed against source |
| **Needs Verification** | Data requires manual review |
| **Valid** | Data conforms to schema |
| **Invalid** | Data violates constraints |

### Temporal Terms

| Term | Definition |
|------|------------|
| **Initial Cert Date** | Date license was first issued |
| **Expiration Date** | Date license expires |
| **Verification Date** | Date data was verified |
| **Scraped Date** | Date data was collected |

## Ontology Versioning

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-08 | Initial ontology definition |

### Change Management

- **Major Version**: Breaking changes to core concepts
- **Minor Version**: New concepts or relationships added
- **Patch Version**: Clarifications or corrections

## Usage Guidelines

### For Data Modelers
- Use ontology terms consistently in data models
- Reference ontology when defining new entities
- Document deviations from ontology

### For Developers
- Use ontology terms in code comments and documentation
- Validate data against ontology constraints
- Report ontology violations

### For Analysts
- Reference ontology for data interpretation
- Use ontology terms in reports
- Validate analysis against business rules

### For Data Stewards
- Use ontology for data quality checks
- Reference ontology in data governance policies
- Maintain ontology accuracy

## References

- [Schema Definition](./schema.json)
- [Schema Documentation](./SCHEMA.md)
- [Data Architecture](./DATA_ARCHITECTURE.md)
- [Quick Reference](./QUICK_REFERENCE.md)

## Maintenance

**Owner**: Data Architecture Team
**Review Cycle**: Quarterly
**Last Review**: 2025-12-08
**Next Review**: 2026-03-08
