# Law Reference Database

Comprehensive reference list of relevant jurisdictions with embedded vectors for semantic search and similarity matching.

## Overview

This database contains structured references to:
- **Federal Law** (U.S. Code) - Criminal and Civil
- **State Law** - Criminal and Civil for all analyzed states
- **Local Jurisdictions** - County and municipal codes

Each reference includes:
- Name and description
- URL to official source
- Key sections/statutes
- Relevance to property management investigations
- **Embedded vector** (384 dimensions) for semantic search

## Structure

### Federal Law

#### Criminal Law
- **Title 18** - Crimes and Criminal Procedure (fraud, conspiracy, RICO, money laundering)
- **Title 26** - Internal Revenue Code Criminal Provisions (tax evasion, fraud)
- **Title 15** - Commerce and Trade Criminal Provisions (securities fraud)

#### Civil Law
- **Title 15** - Commerce and Trade (consumer protection, antitrust)
- **Title 42** - Public Health and Welfare (civil rights, fair housing, ADA)
- **Title 28** - Judiciary and Judicial Procedure (jurisdiction, procedure)

### State Law

#### Analyzed States
1. **Virginia** - Primary focus state
   - Criminal: Title 18.2 (Crimes), Title 58.1 (Tax Criminal)
   - Civil: Title 54.1 (Professions), Title 55.1 (Property), Title 59.1 (Consumer Protection)

2. **Texas** - Extensive analysis
   - Criminal: Penal Code, Tax Code Criminal
   - Civil: Occupations Code, Property Code, Business Organizations Code

3. **Maryland**
   - Criminal: Criminal Law Code
   - Civil: Business Occupations, Real Property Code

4. **District of Columbia**
   - Criminal: Criminal Code
   - Civil: Municipal Regulations Title 17 (Real Estate)

5. **Pennsylvania**
   - Criminal: Crimes Code
   - Civil: Real Estate Licensing Act

6. **North Carolina**
   - Criminal: General Statutes Criminal Law
   - Civil: Real Estate License Law

7. **New Jersey**
   - Criminal: Criminal Code
   - Civil: Real Estate License Act

8. **New York**
   - Criminal: Penal Law
   - Civil: Real Property Law

9. **Connecticut**
   - Criminal: General Statutes Criminal Law
   - Civil: Real Estate License Law

### Local Jurisdictions

- **Virginia**: Fairfax County, Arlington County, City of Alexandria
- **Texas**: Dallas County, Harris County
- **Maryland**: Montgomery County, Prince George's County
- **District of Columbia**: D.C. Municipal Regulations

## Usage

### Loading the Reference Data

```python
import json
from pathlib import Path

ref_file = Path("ref/law/jurisdiction_references.json")
with open(ref_file, 'r') as f:
    references = json.load(f)
```

### Accessing Embeddings

Each jurisdiction entry contains:
- `embedding`: List of 384 float values (normalized vector)
- `embedding_text`: The text used to generate the embedding

```python
# Access federal criminal law embedding
federal_criminal = references["federal"]["criminal"]["title_18"]
embedding = federal_criminal["embedding"]
text = federal_criminal["embedding_text"]
```

### Semantic Search

Use cosine similarity to find relevant jurisdictions:

```python
import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Find jurisdictions similar to a query
model = SentenceTransformer('all-MiniLM-L6-v2')
query = "real estate licensing violations"
query_embedding = model.encode(query, normalize_embeddings=True)

# Compare against all references
for jurisdiction in get_all_jurisdictions(references):
    similarity = cosine_similarity(query_embedding, jurisdiction["embedding"])
    if similarity > 0.7:  # threshold
        print(f"{jurisdiction['name']}: {similarity:.3f}")
```

## Embedding Model

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Normalization**: Yes (L2 normalized)
- **Purpose**: Semantic similarity search and clustering

## File Structure

```
ref/law/
├── README.md                          # This file
└── jurisdiction_references.json       # Complete reference database with embeddings
```

## Statistics

- **Total Jurisdictions**: 40+ references
- **Federal References**: 6 (3 criminal, 3 civil)
- **State References**: 18 (9 states × 2 categories)
- **Local References**: 8+ localities
- **Embedding Dimensions**: 384
- **File Size**: ~1.5 MB (with embeddings)

## Focus Areas

### Primary Focus: Criminal Law
1. Fraud and false statements
2. Conspiracy
3. Money laundering
4. Tax violations
5. Securities fraud

### Secondary Focus: Civil Law
1. Professional licensing violations
2. Consumer protection
3. Property and landlord-tenant law
4. Civil rights and fair housing
5. Business entity compliance

## Updates

- **Created**: 2025-12-11
- **Version**: 1.0.0
- **Last Updated**: 2025-12-11

## Related Documentation

- [U.S. Code](https://www.law.cornell.edu/uscode/text) - Official federal law source
- [Virginia Code](https://law.lis.virginia.gov/vacode/) - Official Virginia law source
- State-specific legal databases linked in JSON file

## Notes

- All URLs point to official legal sources (Cornell LII, state legislatures, etc.)
- Key sections are representative, not exhaustive
- Embeddings are generated from structured text including name, description, key sections, and relevance
- Focus is on property management, real estate licensing, and related violations
