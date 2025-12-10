#!/usr/bin/env python3
"""
Master Pipeline Runner

Executes the complete DPOR search and analysis pipeline with integrated ETL/ELT.
Uses Python 3.14 features: match expressions, except expressions, modern type hints.
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional

from scripts.utils.paths import PROJECT_ROOT, SCRIPTS_DIR, DATA_DIR, RESEARCH_DIR

try:
    from scripts.etl.etl_pipeline import ETLPipeline
except ImportError:
    ETLPipeline = None


def run_search_states() -> bool:
    """
    Run multi-state search for firms and Caitlin Skidmore.

    Note: Search scripts still in R - conversion pending.
    Falls back gracefully if R is not available.

    Returns:
        bool: True if search completed successfully, False otherwise
    """
    print("STEP 1: Searching all states for firms and Caitlin Skidmore...")
    print("This may take a while (searches 50 states x multiple firms/names)...")
    print("Note: Search scripts still in R - conversion pending")

    search_script = PROJECT_ROOT / "bin" / "search_states.R"
    if not search_script.exists():
        print("⚠ Search script not found, skipping\n")
        return False

    try:
        result = subprocess.run(
            ["Rscript", str(search_script)],
            capture_output=True,
            text=True,
            timeout=3600
        )
        match result.returncode:
            case 0:
                print("✓ Search complete\n")
                return True
            case _:
                print(f"✗ Search encountered errors: {result.stderr}\n")
                print("Continuing with available data...\n")
                return False
    except subprocess.TimeoutExpired:
        print("✗ Search timed out\n")
        return False
    except FileNotFoundError:
        print("⚠ R not found, skipping search step\n")
        return False


def run_data_cleaning() -> bool:
    """
    Run data cleaning pipeline.

    Returns:
        bool: True if cleaning completed successfully, False otherwise
    """
    print("STEP 2: Cleaning data with Python...")

    clean_script = PROJECT_ROOT / "bin" / "clean_data.py"
    if not clean_script.exists():
        print("⚠ Clean script not found, skipping\n")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(clean_script)],
            capture_output=True,
            text=True
        )
        match result.returncode:
            case 0:
                print("✓ Data cleaning complete\n")
                if result.stdout:
                    print(result.stdout)
                return True
            case _:
                print(f"✗ Data cleaning failed with exit code: {result.returncode}\n")
                if result.stderr:
                    print(f"Error output:\n{result.stderr}\n")
                print("Stopping pipeline due to cleaning failure.\n")
                return False
    except Exception as e:
        print(f"✗ Data cleaning error: {e}\n")
        return False


def run_connection_analysis() -> bool:
    """
    Run connection analysis to identify Skidmore connections.

    Returns:
        bool: True if analysis completed successfully, False otherwise
    """
    print("STEP 3: Analyzing connections...")

    try:
        from bin.analyze_connections import main_analysis
        try:
            main_analysis()
            print("✓ Connection analysis complete\n")
            return True
        except Exception as e:
            print(f"✗ Analysis encountered errors: {e}\n")
            return False
    except ImportError:
        # Fallback to R version
        analyze_script = PROJECT_ROOT / "bin" / "analyze_connections.R"
        if analyze_script.exists():
            try:
                result = subprocess.run(
                    ["Rscript", str(analyze_script)],
                    capture_output=True,
                    text=True
                )
                match result.returncode:
                    case 0:
                        print("✓ Connection analysis complete\n")
                        return True
                    case _:
                        print(f"✗ Analysis encountered errors: {result.stderr}\n")
                        return False
            except FileNotFoundError:
                print("⚠ R not found, skipping analysis\n")
                return False
        else:
            print("⚠ Analysis script not found, skipping\n")
            return False


def run_data_validation() -> bool:
    """
    Run data quality validation.

    Returns:
        bool: True if validation completed successfully, False otherwise
    """
    print("STEP 4: Validating data quality...")

    try:
        from bin.validate_data import main_validation
        try:
            main_validation()
            print("✓ Data validation complete\n")
            return True
        except Exception as e:
            print(f"✗ Validation encountered errors: {e}\n")
            return False
    except ImportError:
        # Fallback to R version
        validate_script = PROJECT_ROOT / "bin" / "validate_data.R"
        if validate_script.exists():
            try:
                result = subprocess.run(
                    ["Rscript", str(validate_script)],
                    capture_output=True,
                    text=True
                )
                match result.returncode:
                    case 0:
                        print("✓ Data validation complete\n")
                        return True
                    case _:
                        print(f"✗ Validation encountered errors: {result.stderr}\n")
                        return False
            except FileNotFoundError:
                print("⚠ R not found, skipping validation\n")
                return False
        else:
            print("⚠ Validation script not found, skipping\n")
            return False


def run_etl_pipeline() -> bool:
    """Run ETL pipeline with vector embeddings."""
    print("STEP 5: Generating vector embeddings for all data (ETL/ELT)...")

    if ETLPipeline is None:
        print("⚠ ETL pipeline not available, skipping\n")
        return False

    try:
        pipeline = ETLPipeline()
        results = pipeline.run_full_pipeline(force=False)
        print("✓ Vector embeddings generated\n")
        return True
    except Exception as e:
        print(f"✗ ETL pipeline error: {e}\n")
        print("Continuing with pipeline...\n")
        return False


def run_output_generation() -> bool:
    """
    Generate all output reports and summaries.

    Returns:
        bool: True if generation completed successfully, False otherwise
    """
    print("STEP 6: Generating final outputs...")

    try:
        from bin.generate_reports import main_outputs
        try:
            main_outputs()
            print("✓ Output generation complete\n")
            return True
        except Exception as e:
            print(f"✗ Output generation encountered errors: {e}\n")
            return False
    except ImportError:
        # Fallback to R version
        output_script = PROJECT_ROOT / "bin" / "generate_reports.R"
        if output_script.exists():
            try:
                result = subprocess.run(
                    ["Rscript", str(output_script)],
                    capture_output=True,
                    text=True
                )
                match result.returncode:
                    case 0:
                        print("✓ Output generation complete\n")
                        return True
                    case _:
                        print(f"✗ Output generation encountered errors: {result.stderr}\n")
                        return False
            except FileNotFoundError:
                print("⚠ R not found, skipping output generation\n")
                return False
        else:
            print("⚠ Output generation script not found, skipping\n")
            return False


def main() -> None:
    """
    Main pipeline execution function.

    Runs the complete DPOR search and analysis pipeline:
    1. Multi-state search
    2. Data cleaning
    3. Connection analysis
    4. Data validation
    5. ETL pipeline
    6. Output generation
    """
    print("=" * 60)
    print("DPOR Multi-State License Search Pipeline (Python 3.14)")
    print("=" * 60)
    print()

    # Execute pipeline steps
    steps = [
        ("Search all states", run_search_states, False),  # Optional step
        ("Clean data", run_data_cleaning, True),  # Required step
        ("Analyze connections", run_connection_analysis, False),
        ("Validate data", run_data_validation, False),
        ("ETL pipeline", run_etl_pipeline, False),
        ("Generate outputs", run_output_generation, False),
    ]

    for step_name, step_func, required in steps:
        success = step_func()
        if not success and required:
            print(f"Pipeline stopped due to {step_name.lower()} failure.")
            return

    print("=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    print("\nCheck the following directories for results:")
    print("  - data/raw/        - Raw search results")
    print("  - data/cleaned/    - Cleaned data")
    print("  - research/        - Analysis outputs")
    print("  - data/vectors/   - Vector embeddings")
    print()


if __name__ == "__main__":
    main()
