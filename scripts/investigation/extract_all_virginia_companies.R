#!/usr/bin/env Rscript
# Systematic extraction of all 40 Virginia companies
# This script tracks progress and generates a comprehensive list

library(jsonlite)

# Known license numbers from Virginia DPOR search
# Pattern: Sequential numbers from 0225258285 to 0225273913+
virginia_licenses <- c(
  "0225258285", "0225273785",
  "0225273906", "0225273907", "0225273908", "0225273909", "0225273910",
  "0225273911", "0225273912", "0225273913"
)

# Companies already extracted
extracted_companies <- list(
  list(
    individual_license = "0225273913",
    company_name = "BOZZUTO MANAGEMENT COMPANY",
    firm_license = "0226024808",
    status = "confirmed"
  ),
  list(
    individual_license = "0225273906",
    company_name = "CORTLAND MANAGEMENT LLC",
    firm_license = "0226038642",
    status = "confirmed"
  )
)

# Generate full list of 40 license numbers
# Based on pattern, we need to find all licenses between the known range
# The search showed "Showing 1 to 10 of 40 entries", so there are 40 total

cat("=== Virginia DPOR - Complete Company Extraction ===\n\n")
cat("Total Licenses: 40\n")
cat("Extracted: ", length(extracted_companies), "\n")
cat("Remaining: ", 40 - length(extracted_companies), "\n\n")

# Create tracking structure
virginia_extraction <- list(
  metadata = list(
    date = Sys.Date(),
    state = "Virginia",
    broker = "Caitlin Skidmore",
    total_licenses = 40,
    extraction_method = "Browser automation - Related Licenses tab"
  ),
  extracted_companies = extracted_companies,
  remaining_licenses = list(
    note = "38 licenses remaining - need to extract company names via Related Licenses tab",
    sample_license_numbers = virginia_licenses[!virginia_licenses %in% sapply(extracted_companies, function(x) x$individual_license)]
  ),
  extraction_progress = list(
    total = 40,
    extracted = length(extracted_companies),
    remaining = 40 - length(extracted_companies),
    percentage = round((length(extracted_companies) / 40) * 100, 1)
  )
)

# Save progress
output_file <- "research/virginia_companies_extraction_progress.json"
write_json(virginia_extraction, output_file, pretty = TRUE, auto_unbox = TRUE)

cat(sprintf("Progress saved to: %s\n", output_file))
cat(sprintf("Extraction: %.1f%% complete\n", virginia_extraction$extraction_progress$percentage))
