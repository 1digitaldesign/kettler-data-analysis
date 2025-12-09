#!/usr/bin/env python3
"""
Example Usage of Architecture Module
Demonstrates design patterns for data-intensive applications
"""

from scripts.architecture import (
    # Repositories
    FirmRepository, FileRepository, VectorRepository, RepositoryFactory,

    # Services
    AnalysisService, ValidationService, ScrapingService,

    # Strategies
    FraudAnalysisStrategy, NexusAnalysisStrategy,
    ConnectionAnalysisStrategy, ViolationAnalysisStrategy,

    # Pipelines
    AnalysisPipeline, ETLPipeline,

    # Models
    Firm, Connection, Violation, Evidence, PropertyRecord,

    # Base classes
    BaseAnalyzer, BaseScraper, BaseValidator,
)

from scripts.utils.paths import DATA_SOURCE_DIR, DATA_SCRAPED_DIR, DATA_VECTORS_DIR


def example_repository_pattern():
    """Example: Repository Pattern for data access"""
    print("=== Repository Pattern Example ===")

    # Create firm repository
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
    firm_repo = RepositoryFactory.create_firm_repository(str(firms_file))

    # Find all firms
    all_firms = firm_repo.find_all()
    print(f"Total firms: {len(all_firms)}")

    # Find by principal broker
    skidmore_firms = firm_repo.find_by_principal_broker("Caitlin Skidmore")
    print(f"Firms with Caitlin Skidmore as broker: {len(skidmore_firms)}")

    # Find by address
    address_firms = firm_repo.find_by_address("8255 Greensboro")
    print(f"Firms at address: {len(address_firms)}")

    return firm_repo


def example_strategy_pattern(firm_repo: FirmRepository):
    """Example: Strategy Pattern for different analyses"""
    print("\n=== Strategy Pattern Example ===")

    # Create different analysis strategies
    fraud_strategy = FraudAnalysisStrategy(firm_repo)
    nexus_strategy = NexusAnalysisStrategy(firm_repo)
    connection_strategy = ConnectionAnalysisStrategy(firm_repo)
    violation_strategy = ViolationAnalysisStrategy(firm_repo)

    # Execute strategies
    firms = firm_repo.find_all()

    fraud_results = fraud_strategy.analyze(firms)
    print(f"Fraud patterns found: {fraud_results.get('suspicious_patterns_found', 0)}")

    nexus_results = nexus_strategy.analyze(firms)
    print(f"Largest cluster size: {nexus_results.get('largest_cluster_size', 0)}")

    connection_results = connection_strategy.analyze(firms)
    print(f"Total connections: {connection_results.get('total_connections', 0)}")

    violation_results = violation_strategy.analyze(firms)
    print(f"Total violations: {violation_results.get('total_violations', 0)}")

    return {
        'fraud': fraud_results,
        'nexus': nexus_results,
        'connections': connection_results,
        'violations': violation_results
    }


def example_service_layer(firm_repo: FirmRepository):
    """Example: Service Layer Pattern"""
    print("\n=== Service Layer Pattern Example ===")

    # Create analysis service
    analysis_service = AnalysisService(firm_repo)

    # Execute all analyses
    all_results = analysis_service.execute()
    print(f"Analysis types executed: {len(all_results)}")

    # Execute specific analysis
    fraud_results = analysis_service.analyze_fraud_patterns()
    print(f"Fraud patterns: {fraud_results.get('suspicious_patterns_found', 0)}")

    # Create validation service
    validation_service = ValidationService(firm_repo)

    # Validate a firm
    firms = firm_repo.find_all()
    if firms:
        validation_result = validation_service.execute('firm', firms[0])
        print(f"Firm validation: {'Valid' if validation_result['valid'] else 'Invalid'}")
        if validation_result.get('issues'):
            print(f"Issues: {validation_result['issues']}")

    return all_results


def example_pipeline_pattern(firm_repo: FirmRepository):
    """Example: Pipeline Pattern for sequential processing"""
    print("\n=== Pipeline Pattern Example ===")

    # Create analysis pipeline
    pipeline = AnalysisPipeline("Comprehensive Analysis Pipeline")

    # Add strategies to pipeline
    pipeline.add_strategy(FraudAnalysisStrategy(firm_repo))
    pipeline.add_strategy(NexusAnalysisStrategy(firm_repo))
    pipeline.add_strategy(ConnectionAnalysisStrategy(firm_repo))
    pipeline.add_strategy(ViolationAnalysisStrategy(firm_repo))

    # Execute pipeline
    firms = firm_repo.find_all()
    results = pipeline.execute_all(firms)

    print(f"Pipeline executed {len(results)} strategies")
    for strategy_name, result in results.items():
        print(f"  - {strategy_name}: {len(result)} keys")

    return results


def example_factory_pattern():
    """Example: Factory Pattern for object creation"""
    print("\n=== Factory Pattern Example ===")

    # Create repositories using factory
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
    firm_repo = RepositoryFactory.create_firm_repository(str(firms_file))

    file_repo = RepositoryFactory.create_file_repository(str(DATA_SCRAPED_DIR))

    vector_repo = RepositoryFactory.create_vector_repository(str(DATA_VECTORS_DIR))

    print(f"Created {type(firm_repo).__name__}")
    print(f"Created {type(file_repo).__name__}")
    print(f"Created {type(vector_repo).__name__}")

    return firm_repo, file_repo, vector_repo


def example_domain_models():
    """Example: Domain Models"""
    print("\n=== Domain Models Example ===")

    # Create Firm entity
    firm = Firm(
        firm_id="firm_001",
        firm_name="Example Property Management LLC",
        address="123 Main Street, Alexandria, VA 22314",
        principal_broker="Caitlin Skidmore",
        license_number="12345678",
        state="VA",
        phone="703-555-1234",
        email="info@example.com"
    )

    print(f"Created firm: {firm.firm_name}")
    print(f"Firm dict: {list(firm.to_dict().keys())}")

    # Create Violation entity
    from scripts.architecture.models import Violation, ViolationType

    violation = Violation(
        violation_id="viol_001",
        violation_type=ViolationType.LICENSE,
        entity_id=firm.firm_id,
        entity_type="firm",
        description="Missing license number",
        severity="high",
        evidence=["Firm registration check", "DPOR database search"]
    )

    print(f"Created violation: {violation.violation_type.value}")
    print(f"Severity: {violation.severity}")

    return firm, violation


def main():
    """Run all examples"""
    print("=" * 60)
    print("Architecture Module Examples")
    print("Design Patterns for Data-Intensive Applications")
    print("=" * 60)

    try:
        # Repository Pattern
        firm_repo = example_repository_pattern()

        # Strategy Pattern
        strategy_results = example_strategy_pattern(firm_repo)

        # Service Layer Pattern
        service_results = example_service_layer(firm_repo)

        # Pipeline Pattern
        pipeline_results = example_pipeline_pattern(firm_repo)

        # Factory Pattern
        repos = example_factory_pattern()

        # Domain Models
        models = example_domain_models()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError in examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
