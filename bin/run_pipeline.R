#!/usr/bin/env Rscript
# Master Pipeline Runner
# Executes the complete DPOR search and analysis pipeline

# Load path utilities
source(file.path(dirname(normalizePath(commandArgs()[4])), "load_paths.R"))

cat("========================================\n")
cat("DPOR Multi-State License Search Pipeline\n")
cat("========================================\n\n")

# Step 1: Search all states
cat("STEP 1: Searching all states for firms and Caitlin Skidmore...\n")
cat("This may take a while (searches 50 states x multiple firms/names)...\n")
cat("Press Ctrl+C to cancel, or wait to continue...\n")
Sys.sleep(5)

source_bin("search_states.R")
tryCatch({
  main_multi_state()
  cat("✓ Search complete\n\n")
}, error = function(e) {
  cat("✗ Search encountered errors:", e$message, "\n")
  cat("Continuing with available data...\n\n")
})

# Step 2: Clean data
cat("STEP 2: Cleaning data with Python/Hugging Face...\n")
# Try python3 first, fallback to python
python_cmd <- if (system("which python3 > /dev/null 2>&1", ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
  "python3"
} else {
  "python"
}
clean_script <- file.path(BIN_DIR, "clean_data.py")
system_result <- system(paste(python_cmd, clean_script), intern = TRUE)
exit_code <- attr(system_result, "status")
if (!is.null(exit_code) && exit_code != 0) {
  cat("✗ Data cleaning failed with exit code:", exit_code, "\n")
  cat("Error output:\n")
  if (length(system_result) > 0) {
    cat(paste(system_result, collapse = "\n"), "\n")
  }
  cat("Stopping pipeline due to cleaning failure.\n")
  stop("Data cleaning failed")
} else {
  if (length(system_result) > 0) {
    cat(paste(system_result, collapse = "\n"), "\n")
  }
  cat("✓ Data cleaning complete\n\n")
}

# Step 3: Analyze connections
cat("STEP 3: Analyzing connections...\n")
source_bin("analyze_connections.R")
tryCatch({
  main_analysis()
  cat("✓ Connection analysis complete\n\n")
}, error = function(e) {
  cat("✗ Analysis encountered errors:", e$message, "\n\n")
})

# Step 4: Validate data quality
cat("STEP 4: Validating data quality...\n")
source_bin("validate_data.R")
tryCatch({
  main_validation()
  cat("✓ Data validation complete\n\n")
}, error = function(e) {
  cat("✗ Validation encountered errors:", e$message, "\n\n")
})

# Step 5: Generate vector embeddings (ETL)
cat("STEP 5: Generating vector embeddings for all data...\n")
python_cmd <- if (system("which python3 > /dev/null 2>&1", ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
  "python3"
} else {
  "python"
}
etl_script <- file.path(getwd(), "scripts", "etl", "etl_pipeline.py")
if (file.exists(etl_script)) {
  tryCatch({
    system_result <- system(paste(python_cmd, etl_script), intern = TRUE)
    exit_code <- attr(system_result, "status")
    if (!is.null(exit_code) && exit_code != 0) {
      cat("✗ ETL pipeline encountered errors (exit code:", exit_code, ")\n")
      cat("Continuing with pipeline...\n\n")
    } else {
      if (length(system_result) > 0) {
        cat(paste(system_result, collapse = "\n"), "\n")
      }
      cat("✓ Vector embeddings generated\n\n")
    }
  }, error = function(e) {
    cat("✗ ETL pipeline error:", e$message, "\n")
    cat("Continuing with pipeline...\n\n")
  })
} else {
  cat("⚠ ETL script not found, skipping vector embeddings\n\n")
}

# Step 6: Generate outputs
cat("STEP 6: Generating final outputs...\n")
source("generate_outputs.R")
tryCatch({
  main_outputs()
  cat("✓ Output generation complete\n\n")
}, error = function(e) {
  cat("✗ Output generation encountered errors:", e$message, "\n\n")
})

cat("========================================\n")
cat("Pipeline Complete!\n")
cat("========================================\n")
cat("\nCheck the following directories for results:\n")
cat("  - data/raw/        - Raw search results\n")
cat("  - data/cleaned/    - Cleaned data\n")
cat("  - data/analysis/  - Analysis outputs\n")
cat("\nKey output files:\n")
cat("  - dpor_multi_state_summary.csv\n")
cat("  - dpor_connection_type_summary.csv\n")
cat("  - dpor_high_quality_records.csv\n")
cat("\n")
