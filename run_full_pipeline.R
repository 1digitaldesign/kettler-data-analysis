#!/usr/bin/env Rscript
# Master Pipeline Runner
# Executes the complete DPOR search and analysis pipeline

cat("========================================\n")
cat("DPOR Multi-State License Search Pipeline\n")
cat("========================================\n\n")

# Step 1: Search all states
cat("STEP 1: Searching all states for firms and Caitlin Skidmore...\n")
cat("This may take a while (searches 50 states x multiple firms/names)...\n")
cat("Press Ctrl+C to cancel, or wait to continue...\n")
Sys.sleep(5)

source("search_multi_state_dpor.R")
tryCatch({
  main_multi_state()
  cat("✓ Search complete\n\n")
}, error = function(e) {
  cat("✗ Search encountered errors:", e$message, "\n")
  cat("Continuing with available data...\n\n")
})

# Step 2: Clean data
cat("STEP 2: Cleaning data with Python/Hugging Face...\n")
system_result <- system("python clean_dpor_data.py", intern = TRUE)
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
source("analyze_skidmore_connections.R")
tryCatch({
  main_analysis()
  cat("✓ Connection analysis complete\n\n")
}, error = function(e) {
  cat("✗ Analysis encountered errors:", e$message, "\n\n")
})

# Step 4: Validate data quality
cat("STEP 4: Validating data quality...\n")
source("validate_data_quality.R")
tryCatch({
  main_validation()
  cat("✓ Data validation complete\n\n")
}, error = function(e) {
  cat("✗ Validation encountered errors:", e$message, "\n\n")
})

# Step 5: Generate outputs
cat("STEP 5: Generating final outputs...\n")
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
