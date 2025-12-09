# Tool Recommendations for Kettler Data Analysis

**Date:** December 9, 2024  
**Status:** Research Complete - Implementation Recommendations

## Executive Summary

After analyzing the codebase and researching current best practices, this document provides recommendations for tools to fill data gaps and improve analysis capabilities. The project currently has many "framework" placeholders that need real data collection and processing.

## Current State Analysis

### Missing Data Identified

1. **Scraped Data** (`data/scraped/`)
   - Airbnb listings: Framework placeholder, no actual listings
   - VRBO listings: Framework placeholder, no actual listings
   - Front website data: Minimal scraping results
   - STR listings analysis: Needs actual listing data

2. **Research Data** (`research/`)
   - Connection matrix: Mostly empty (0 connections found)
   - Violations: Mostly framework status, needs verification
   - Fraud indicators: Limited data
   - Filing recommendations: Sparse data

3. **Analysis Outputs** (`data/analysis/`)
   - Many directories are empty (only `.gitkeep` files)
   - Needs actual analysis results

## Tool Recommendations by Use Case

### 1. Web Scraping Tools

#### **Primary Recommendation: Playwright**

**Why Playwright:**
- Faster than Selenium (2-3x performance improvement)
- Better JavaScript rendering for modern sites
- Excellent for Airbnb, VRBO, and dynamic websites
- Built-in auto-waiting and network interception
- Cross-browser support (Chromium, Firefox, WebKit)

**Implementation:**
```python
# Add to requirements.txt
playwright>=1.40.0
playwright-stealth>=1.0.6  # Anti-detection
```

**Use Cases:**
- Airbnb listing scraping
- VRBO listing scraping
- Dynamic website scraping
- Form submissions and interactions

#### **Alternative: Scrapy + Splash**

**Why Scrapy:**
- Best for large-scale scraping
- Asynchronous by default
- Built-in rate limiting and retry logic
- Excellent for static content

**When to Use:**
- Bulk data collection
- Static websites
- High-volume scraping

#### **API Services (Recommended for Production)**

**ZenRows** - Universal Scraper API
- Handles anti-bot protection automatically
- Dynamic IP rotation
- JavaScript rendering
- Built-in Airbnb/VRBO support
- **Cost:** Pay-per-use, free trial available

**ScraperAPI** - Real Estate Focused
- Dedicated real estate scraper APIs
- Advanced anti-bot technology
- Global proxy network
- **Cost:** Subscription-based

**Outscraper** - VRBO Specialist
- Pre-built VRBO scraper
- Bulk scraping support
- CSV/Excel export
- **Cost:** Pay-per-scrape

**Recommendation:** Use Playwright for development/testing, ZenRows or ScraperAPI for production scraping.

### 2. Data Analysis Tools

#### **Current: Pandas**
- Already in use
- Good for small-medium datasets
- Familiar API

#### **Recommended Addition: Polars**

**Why Polars:**
- 10-30x faster than Pandas for large datasets
- Lower memory usage
- Lazy evaluation
- Better for data processing pipelines
- Built on Rust (performance)

**Implementation:**
```python
# Add to requirements.txt
polars>=0.19.0
```

**Use Cases:**
- Processing large DPOR search results
- Analyzing connection matrices
- Data cleaning and transformation
- Aggregations and joins

**Migration Path:**
- Keep Pandas for existing code
- Use Polars for new data processing
- Gradually migrate high-performance paths

#### **For Very Large Datasets: Dask**

**When to Use:**
- Datasets > 10GB
- Distributed processing needed
- Parallel computation required

**Implementation:**
```python
# Add to requirements.txt
dask>=2024.1.0
dask[dataframe]>=2024.1.0
```

### 3. Vector Database Tools

#### **Current: FAISS**
- Already implemented
- Good for in-memory search
- High performance

#### **Recommended Addition: Qdrant**

**Why Qdrant:**
- Better metadata filtering
- Persistent storage (FAISS is in-memory)
- REST API for web integration
- Better for production deployments
- Lower latency (2-8ms vs FAISS variable)

**Implementation:**
```python
# Add to requirements.txt
qdrant-client>=1.7.0
```

**Use Cases:**
- Persistent vector storage
- Metadata filtering (filter by date, source, etc.)
- Web API integration
- Production deployments

**Migration Path:**
- Keep FAISS for development
- Use Qdrant for production
- Migrate gradually

#### **Alternative: Weaviate**

**When to Use:**
- Need GraphQL API
- Want built-in vectorization
- Need hybrid search (vector + keyword)
- Complex semantic search requirements

### 4. Real Estate Data APIs

#### **Recommended: ZenRows**

**Features:**
- Pre-built Airbnb scraper
- Anti-bot protection handled
- JavaScript rendering
- Proxy rotation
- **Cost:** Pay-per-use

**Implementation:**
```python
# Add to requirements.txt
zenrows>=1.0.0
```

#### **Alternative: ScraperAPI**

**Features:**
- Real estate focused
- Dedicated endpoints
- Higher success rate
- **Cost:** Subscription

### 5. Browser Automation Tools

#### **Current: Selenium (in requirements)**
- Works but slower
- More resource-intensive

#### **Recommended: Playwright**

**Advantages:**
- Faster execution
- Better modern web support
- Built-in network interception
- Auto-waiting
- Better debugging tools

**Implementation:**
```python
# Replace selenium with playwright
playwright>=1.40.0
```

### 6. Data Validation Tools

#### **Recommended: Great Expectations**

**Why:**
- Data quality validation
- Automated testing
- Documentation generation
- Profiling

**Implementation:**
```python
# Add to requirements.txt
great-expectations>=0.18.0
```

**Use Cases:**
- Validate scraped data quality
- Check data completeness
- Ensure data consistency
- Generate data quality reports

### 7. API Development Tools

#### **Current: FastAPI**
- Already implemented
- Excellent choice
- Keep using

#### **Recommended Addition: Pydantic V2**

**Why:**
- Better performance
- Improved validation
- Better error messages

**Implementation:**
```python
# Already in requirements.txt
pydantic>=2.5.0  # Ensure V2
```

## Implementation Priority

### Phase 1: Critical (Immediate)
1. **Playwright** - Replace Selenium for scraping
2. **Polars** - Improve data processing performance
3. **ZenRows API** - Real Airbnb/VRBO data collection
4. **Qdrant** - Persistent vector storage

### Phase 2: Important (Next Sprint)
1. **Great Expectations** - Data quality validation
2. **Dask** - Large dataset processing
3. **ScraperAPI** - Backup scraping service

### Phase 3: Enhancement (Future)
1. **Weaviate** - Advanced semantic search
2. **Apache Sedona** - Spatial data analysis (if needed)
3. **PyGWalker** - Interactive data exploration

## Specific Recommendations for Missing Data

### 1. Airbnb/VRBO Listings

**Tool:** Playwright + ZenRows API
**Action:**
- Implement Playwright scraper for development
- Use ZenRows API for production
- Target: Collect 100+ listings per platform

### 2. Connection Matrix

**Tool:** Polars for data processing
**Action:**
- Use Polars to process DPOR search results
- Cross-reference firm data
- Build connection graph
- Target: Identify all connections

### 3. Violations Data

**Tool:** Great Expectations + Playwright
**Action:**
- Validate license data quality
- Scrape regulatory databases
- Cross-reference violations
- Target: Complete violation matrix

### 4. STR Listings Analysis

**Tool:** Playwright + Polars
**Action:**
- Scrape all STR platforms
- Process with Polars
- Match to building addresses
- Target: Complete STR violation analysis

## Code Examples

### Playwright Scraper Example

```python
from playwright.sync_api import sync_playwright

def scrape_airbnb_playwright(address: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.airbnb.com/s/{address}")
        # Wait for listings to load
        page.wait_for_selector('[data-testid="listing-card"]')
        listings = page.query_selector_all('[data-testid="listing-card"]')
        results = []
        for listing in listings:
            title = listing.query_selector('h3').inner_text()
            price = listing.query_selector('[data-testid="price"]').inner_text()
            results.append({'title': title, 'price': price})
        browser.close()
        return results
```

### Polars Data Processing Example

```python
import polars as pl

# Load and process DPOR data
df = pl.read_csv("data/source/skidmore_all_firms_complete.csv")
connections = (
    df
    .group_by("Principal.Broker")
    .agg([
        pl.count("Firm.Name").alias("firm_count"),
        pl.col("Firm.Name").unique().alias("firms")
    ])
    .filter(pl.col("firm_count") > 1)
)
```

### Qdrant Vector Storage Example

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient("localhost", port=6333)
client.create_collection(
    collection_name="evidence_vectors",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)
```

## Cost Analysis

### Free/Open Source
- Playwright: Free
- Polars: Free
- Qdrant: Free (self-hosted)
- FAISS: Free
- Scrapy: Free

### Paid Services (Estimated Monthly)
- ZenRows: $49-299/month (based on usage)
- ScraperAPI: $49-499/month (based on requests)
- Outscraper: Pay-per-scrape (~$0.01-0.10 per listing)

**Recommendation:** Start with free tools, add paid APIs only when needed for production.

## Migration Strategy

1. **Week 1-2:** Implement Playwright scraping
2. **Week 3:** Add Polars for data processing
3. **Week 4:** Integrate ZenRows API
4. **Week 5:** Set up Qdrant for vector storage
5. **Week 6:** Add Great Expectations validation

## Conclusion

The recommended tool stack will significantly improve:
- **Data Collection:** Playwright + APIs for real data
- **Data Processing:** Polars for performance
- **Data Storage:** Qdrant for persistence
- **Data Quality:** Great Expectations for validation

This will transform the project from "framework" placeholders to a fully functional data analysis system.
