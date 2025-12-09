#!/usr/bin/env python3
"""
Master Pipeline Runner (Python)
Executes the complete DPOR search and analysis pipeline with integrated ETL/ELT
"""

import sys
import subprocess
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from scripts.utils.paths import PROJECT_ROOT, SCRIPTS_DIR, DATA_DIR, RESEARCH_DIR
from scripts.etl.etl_pipeline import ETLPipeline

def run_search_states():
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

    # For now, check if R script exists and can be run
    search_script = PROJECT_ROOT / "bin" / "search_states.R"
    if search_script.exists():
        try:
            result = subprocess.run(
                ["Rscript", str(search_script)],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            if result.returncode == 0:
                print("✓ Search complete\n")
                return True
            else:
                print(f"✗ Search encountered errors: {result.stderr}\n")
                print("Continuing with available data...\n")
                return False
        except subprocess.TimeoutExpired:
            print("✗ Search timed out\n")
            return False
        except FileNotFoundError:
            print("⚠ R not found, skipping search step\n")
            return False
    else:
        print("⚠ Search script not found, skipping\n")
        return False

def run_data_cleaning():
    """
    Run data cleaning pipeline.

    Cleans and standardizes license data from multiple state DPOR searches.
    Uses Hugging Face transformers for entity extraction and normalization.

    Returns:
        bool: True if cleaning completed successfully, False otherwise
    """
    """Run data cleaning with Python/Hugging Face"""
    print("STEP 2: Cleaning data with Python/Hugging Face...")

    clean_script = PROJECT_ROOT / "bin" / "clean_data.py"
    if clean_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(clean_script)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Data cleaning complete\n")
                if result.stdout:
                    print(result.stdout)
                return True
            else:
                print(f"✗ Data cleaning failed with exit code: {result.returncode}\n")
                if result.stderr:
                    print(f"Error output:\n{result.stderr}\n")
                print("Stopping pipeline due to cleaning failure.\n")
                return False
        except Exception as e:
            print(f"✗ Data cleaning error: {e}\n")
            return False
    else:
        print("⚠ Clean script not found, skipping\n")
        return False

def run_connection_analysis():
    """
    Run connection analysis to identify Skidmore connections.

    Analyzes DPOR results to find firms connected to Caitlin Skidmore
    through principal broker relationships, addresses, or firm names.

    Returns:
        bool: True if analysis completed successfully, False otherwise
    """
    """Run connection analysis"""
    print("STEP 3: Analyzing connections...")

    # Import Python version if available
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
                if result.returncode == 0:
                    print("✓ Connection analysis complete\n")
                    return True
                else:
                    print(f"✗ Analysis encountered errors: {result.stderr}\n")
                    return False
            except FileNotFoundError:
                print("⚠ R not found, skipping analysis\n")
                return False
        else:
            print("⚠ Analysis script not found, skipping\n")
            return False

def run_data_validation():
    """
    Run data quality validation.

    Validates license numbers, flags duplicates, validates addresses and dates,
    and generates quality reports.

    Returns:
        bool: True if validation completed successfully, False otherwise
    """
    """Run data quality validation"""
    print("STEP 4: Validating data quality...")

    # Import Python version if available
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
                if result.returncode == 0:
                    print("✓ Data validation complete\n")
                    return True
                else:
                    print(f"✗ Validation encountered errors: {result.stderr}\n")
                    return False
            except FileNotFoundError:
                print("⚠ R not found, skipping validation\n")
                return False
        else:
            print("⚠ Validation script not found, skipping\n")
            return False

def run_etl_pipeline():
    """Run ETL pipeline with vector embeddings"""
    print("STEP 5: Generating vector embeddings for all data (ETL/ELT)...")

    try:
        pipeline = ETLPipeline()
        results = pipeline.run_full_pipeline(force=False)

        print("✓ Vector embeddings generated\n")
        return True
    except Exception as e:
        print(f"✗ ETL pipeline error: {e}\n")
        print("Continuing with pipeline...\n")
        return False

def run_output_generation():
    """
    Generate all output reports and summaries.

    Creates summary CSV files, quality reports, and analysis outputs.

    Returns:
        bool: True if generation completed successfully, False otherwise
    """
    """Generate final outputs"""
    print("STEP 6: Generating final outputs...")

    # Import Python version if available
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
                if result.returncode == 0:
                    print("✓ Output generation complete\n")
                    return True
                else:
                    print(f"✗ Output generation encountered errors: {result.stderr}\n")
                    return False
            except FileNotFoundError:
                print("⚠ R not found, skipping output generation\n")
                return False
        else:
            print("⚠ Output generation script not found, skipping\n")
            return False

def main():
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
    """Main pipeline execution"""
    print("=" * 60)
    print("DPOR Multi-State License Search Pipeline (Python)")
    print("=" * 60)
    print()

    # Step 1: Search all states
    run_search_states()

    # Step 2: Clean data
    if not run_data_cleaning():
        print("Pipeline stopped due to cleaning failure.")
        return

    # Step 3: Analyze connections
    run_connection_analysis()

    # Step 4: Validate data quality
    run_data_validation()

    # Step 5: Generate vector embeddings (ETL/ELT)
    run_etl_pipeline()

    # Step 6: Generate outputs
    run_output_generation()

    print("=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    print("\nCheck the following directories for results:")
    print("  - data/raw/        - Raw search results")
    print("  - data/cleaned/    - Cleaned data")
    print("  - data/analysis/  - Analysis outputs")
    print("  - data/vectors/   - Vector embeddings")
    print("\nKey output files:")
    print("  - dpor_multi_state_summary.csv")
    print("  - dpor_connection_type_summary.csv")
    print("  - dpor_high_quality_records.csv")
    print()

if __name__ == "__main__":
    main()
