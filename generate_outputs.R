#!/usr/bin/env Rscript
# Generate All Outputs and Reports
# Master script to generate all analysis outputs

library(dplyr)

source("analyze_skidmore_connections.R")
source("validate_data_quality.R")

# Generate summary CSV files
generate_summary_csvs <- function() {
  cat("Generating summary CSV files...\n")

  # Load data
  connections_file <- file.path("data/analysis", "dpor_skidmore_connections.csv")
  validated_file <- file.path("data/analysis", "dpor_validated.csv")

  if (file.exists(connections_file)) {
    connections <- read.csv(connections_file, stringsAsFactors = FALSE)

    if (nrow(connections) > 0 && "state" %in% names(connections) && "firm_name" %in% names(connections)) {
      # Summary by state
      summary_by_state <- connections %>%
        group_by(state) %>%
        summarise(
          firm_count = n_distinct(firm_name),
          connection_count = n(),
          .groups = 'drop'
        ) %>%
        arrange(desc(connection_count))

      write.csv(summary_by_state, "dpor_multi_state_summary.csv", row.names = FALSE)
      cat("Saved state summary to: dpor_multi_state_summary.csv\n")
    } else {
      cat("Warning: Connections file exists but is empty or missing required columns\n")
    }

    if (nrow(connections) > 0 && "connection_type" %in% names(connections) && "firm_name" %in% names(connections)) {
      # Summary by connection type
      summary_by_type <- connections %>%
        group_by(connection_type) %>%
        summarise(
          firm_count = n_distinct(firm_name),
          connection_count = n(),
          .groups = 'drop'
        ) %>%
        arrange(desc(connection_count))

      write.csv(summary_by_type, "dpor_connection_type_summary.csv", row.names = FALSE)
      cat("Saved connection type summary to: dpor_connection_type_summary.csv\n")
    }
  }

  if (file.exists(validated_file)) {
    validated <- read.csv(validated_file, stringsAsFactors = FALSE)

    # High-quality records only
    high_quality <- validated %>%
      filter(
        (license_valid == TRUE | is.na(license_valid)),
        (address_valid == TRUE | is.na(address_valid)),
        (is_duplicate == FALSE | is.na(is_duplicate))
      )

    write.csv(high_quality, "dpor_high_quality_records.csv", row.names = FALSE)
    cat("Saved high-quality records to: dpor_high_quality_records.csv\n")
  }
}

# Main output generation
main_outputs <- function() {
  cat("=== Generating All Outputs ===\n\n")

  # Run analysis
  cat("Step 1: Running connection analysis...\n")
  main_analysis()

  cat("\nStep 2: Running data quality validation...\n")
  main_validation()

  cat("\nStep 3: Generating summary CSV files...\n")
  generate_summary_csvs()

  cat("\n=== All Outputs Generated ===\n")
  cat("\nOutput files:\n")
  cat("  - data/analysis/dpor_skidmore_connections.csv\n")
  cat("  - data/analysis/dpor_validated.csv\n")
  cat("  - data/analysis/analysis_summary.json\n")
  cat("  - data/analysis/data_quality_report.json\n")
  cat("  - dpor_multi_state_summary.csv\n")
  cat("  - dpor_connection_type_summary.csv\n")
  cat("  - dpor_high_quality_records.csv\n")
}

# Run if executed as script
if (!interactive()) {
  main_outputs()
}
