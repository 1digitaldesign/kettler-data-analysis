# Architecture Module - Design Patterns for Data-Intensive Applications

## Overview

This module implements proper software architecture using design patterns specifically suited for data-intensive applications.

## Design Patterns Implemented

### 1. Repository Pattern (`repository.py`)
**Purpose:** Abstract data access layer

- **FirmRepository**: Manages Firm entities
- **FileRepository**: Generic file-based storage
- **VectorRepository**: Vector database operations

**Benefits:**
- Decouples business logic from data access
- Easy to swap data sources
- Centralized data access logic

### 2. Factory Pattern (`factory.py`)
**Purpose:** Create objects without specifying exact classes

- **ProcessorFactory**: Creates processors
- **AnalyzerFactory**: Creates analyzers
- **ScraperFactory**: Creates scrapers
- **RepositoryFactory**: Creates repositories

**Benefits:**
- Flexible object creation
- Easy to add new types
- Centralized creation logic

### 3. Strategy Pattern (`strategy.py`)
**Purpose:** Define family of algorithms, make them interchangeable

- **FraudAnalysisStrategy**: Fraud pattern detection
- **NexusAnalysisStrategy**: Nexus pattern detection
- **ConnectionAnalysisStrategy**: Connection analysis
- **ViolationAnalysisStrategy**: Violation detection

**Benefits:**
- Easy to add new analysis types
- Algorithms are interchangeable
- Clean separation of concerns

### 4. Template Method Pattern (`base.py`)
**Purpose:** Define skeleton of algorithm in base class

- **BaseProcessor**: Template for all processors
- **BaseAnalyzer**: Template for analyzers
- **BaseScraper**: Template for scrapers
- **BaseValidator**: Template for validators

**Benefits:**
- Code reuse
- Consistent structure
- Easy to extend

### 5. Pipeline Pattern (`pipeline.py`)
**Purpose:** Sequential data processing stages

- **DataPipeline**: Generic pipeline
- **ETLPipeline**: Extract-Transform-Load pipeline
- **AnalysisPipeline**: Multi-strategy analysis

**Benefits:**
- Modular processing
- Easy to add/remove stages
- Clear data flow

### 6. Chain of Responsibility (`base.py`, `pipeline.py`)
**Purpose:** Pass requests along chain of handlers

- **BaseValidator**: Validation chain
- **PipelineStage**: Processing chain

**Benefits:**
- Flexible request handling
- Easy to add new handlers
- Decoupled request/response

### 7. Service Layer Pattern (`services.py`)
**Purpose:** Business logic abstraction

- **AnalysisService**: Analysis operations
- **ValidationService**: Validation operations
- **ScrapingService**: Scraping operations

**Benefits:**
- Clean business logic
- Reusable services
- Easy to test

### 8. Facade Pattern (`services.py`)
**Purpose:** Simplified interface to complex subsystem

- **AnalysisService**: Simplifies analysis operations
- **ScrapingService**: Simplifies scraping operations

**Benefits:**
- Simple interface
- Hides complexity
- Easy to use

## Domain Models (`models.py`)

### Entities
- **Firm**: Real estate firm entity
- **Connection**: Connection between entities
- **Violation**: Violation entity
- **Evidence**: Evidence entity
- **PropertyRecord**: Property record entity

### Value Objects
- **ViolationType**: Enumeration
- **ConnectionType**: Enumeration
- **AnalysisResult**: DTO for results

## Usage Examples

### Using Repository Pattern

```python
from scripts.architecture import FirmRepository, RepositoryFactory

# Create repository
firm_repo = RepositoryFactory.create_firm_repository("data/source/firms.json")

# Find firms
all_firms = firm_repo.find_all()
firm = firm_repo.find_by_id("firm_123")
broker_firms = firm_repo.find_by_principal_broker("Caitlin Skidmore")
```

### Using Strategy Pattern

```python
from scripts.architecture import (
    FraudAnalysisStrategy, NexusAnalysisStrategy,
    FirmRepository, RepositoryFactory
)

firm_repo = RepositoryFactory.create_firm_repository("data/source/firms.json")

# Use different strategies
fraud_strategy = FraudAnalysisStrategy(firm_repo)
fraud_results = fraud_strategy.analyze(firm_repo.find_all())

nexus_strategy = NexusAnalysisStrategy(firm_repo)
nexus_results = nexus_strategy.analyze(firm_repo.find_all())
```

### Using Service Layer

```python
from scripts.architecture import AnalysisService, RepositoryFactory

firm_repo = RepositoryFactory.create_firm_repository("data/source/firms.json")
analysis_service = AnalysisService(firm_repo)

# Execute analyses
all_results = analysis_service.execute()
fraud_results = analysis_service.analyze_fraud_patterns()
```

### Using Pipeline Pattern

```python
from scripts.architecture import ETLPipeline, PipelineStage

class ExtractStage(PipelineStage):
    def execute(self, data):
        # Extract logic
        return extracted_data

class TransformStage(PipelineStage):
    def execute(self, data):
        # Transform logic
        return transformed_data

# Build pipeline
pipeline = ETLPipeline()
pipeline.add_stage(ExtractStage("extract"))
pipeline.add_stage(TransformStage("transform"))

result = pipeline.execute(source_data)
```

## Architecture Benefits

1. **Separation of Concerns**: Clear boundaries between layers
2. **Testability**: Easy to mock and test components
3. **Maintainability**: Changes isolated to specific patterns
4. **Scalability**: Easy to add new features
5. **Reusability**: Components can be reused
6. **Flexibility**: Easy to swap implementations

## Migration Path

The refactored architecture can gradually replace the unified modules:

1. **Phase 1**: Use alongside existing unified modules
2. **Phase 2**: Migrate high-traffic paths to new architecture
3. **Phase 3**: Complete migration, deprecate unified modules

## Performance Considerations

- **Repository caching**: Reduces I/O operations
- **Strategy pattern**: Allows algorithm optimization per strategy
- **Pipeline pattern**: Enables parallel processing
- **Service layer**: Centralized caching and optimization

## Future Enhancements

1. **Observer Pattern**: For event-driven processing
2. **Command Pattern**: For undoable operations
3. **Builder Pattern**: For complex object construction
4. **Adapter Pattern**: For integrating external APIs
5. **Decorator Pattern**: For adding features dynamically
