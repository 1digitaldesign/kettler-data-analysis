#!/usr/bin/env Rscript
# Demo Analysis Pipeline
# Uses existing Skidmore data to demonstrate the analysis workflow
# Note: Full web scraping may require state-specific implementations

cat("=== DPOR Analysis Pipeline Demo ===\n\n")

# Step 1: Load existing data
cat("Step 1: Loading existing Skidmore data...\n")
source("analyze_skidmore_connections.R")

skidmore_data <- load_skidmore_data()
firms_count <- if (!is.null(skidmore_data$firms_complete)) nrow(skidmore_data$firms_complete) else 0
licenses_count <- if (!is.null(skidmore_data$individual_licenses)) nrow(skidmore_data$individual_licenses) else 0
cat("  Loaded", firms_count, "known firms\n")
cat("  Loaded", licenses_count, "individual licenses\n\n")

# Step 2: Create sample DPOR results from existing data
cat("Step 2: Creating sample DPOR results from existing data...\n")
# Convert existing firm data to DPOR format
if (is.null(skidmore_data$firms_complete) || nrow(skidmore_data$firms_complete) == 0) {
  cat("  Warning: No firm data available, creating empty sample\n")
  sample_dpor <- data.frame(
    license_number = character(0),
    name = character(0),
    address = character(0),
    state = character(0),
    license_type = character(0),
    expiration_date = character(0),
    principal_broker = character(0),
    initial_cert_date = character(0),
    stringsAsFactors = FALSE
  )
} else {
  sample_dpor <- skidmore_data$firms_complete %>%
    mutate(
      license_number = License.Number,
      name = Firm.Name,
      address = Address,
      state = "VA",
      license_type = License.Type,
      expiration_date = Expiration.Date,
      principal_broker = Principal.Broker,
      initial_cert_date = Initial.Cert.Date
    ) %>%
    select(license_number, name, address, state, license_type,
           expiration_date, principal_broker, initial_cert_date)
}

# Save as sample raw data
write.csv(sample_dpor, "data/raw/sample_dpor_results.csv", row.names = FALSE)
cat("  Created sample data with", nrow(sample_dpor), "records\n")
cat("  Saved to: data/raw/sample_dpor_results.csv\n\n")

# Step 3: Clean data (Python - skip if transformers not available)
cat("Step 3: Cleaning data...\n")
cat("  Note: Python cleaning requires transformers library\n")
cat("  Running basic R cleaning instead...\n")

# Basic cleaning in R
cleaned_dpor <- sample_dpor %>%
  mutate(
    name_cleaned = stringr::str_trim(name),
    address_normalized = stringr::str_trim(address)
  )

write.csv(cleaned_dpor, "data/cleaned/dpor_all_cleaned.csv", row.names = FALSE)
cat("  Cleaned data saved to: data/cleaned/dpor_all_cleaned.csv\n\n")

# Step 4: Analyze connections
cat("Step 4: Analyzing connections...\n")
dpor_results <- cleaned_dpor
connections <- find_skidmore_connections(dpor_results, skidmore_data)
cat("  Found", nrow(connections), "connections\n")

if (nrow(connections) > 0) {
  write.csv(connections, "data/analysis/dpor_skidmore_connections.csv", row.names = FALSE)
  cat("  Saved connections to: data/analysis/dpor_skidmore_connections.csv\n")

  # Print summary
  cat("\n  Connection Summary:\n")
  print(table(connections$connection_type))
} else {
  cat("  No connections found in sample data\n")
}

cat("\n")

# Step 5: Validate data quality
cat("Step 5: Validating data quality...\n")
source("validate_data_quality.R")
main_validation()

cat("\n=== Demo Pipeline Complete ===\n")
cat("\nNext steps:\n")
cat("1. Implement state-specific web scraping for actual DPOR searches\n")
cat("2. Run full multi-state search: Rscript search_multi_state_dpor.R\n")
cat("3. Install Python transformers for advanced cleaning: pip install transformers\n")
cat("4. Generate full report: rmarkdown::render('dpor_analysis_report.Rmd')\n")
