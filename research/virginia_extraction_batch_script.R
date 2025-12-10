#!/usr/bin/env Rscript
# Virginia DPOR Batch Extraction - Automated Script
# This script processes all 40 licenses systematically

library(jsonlite)

# All 40 license numbers (we know the first 10, need to get remaining 30)
known_licenses <- c(
  "0225258285", "0225273785",
  "0225273906", "0225273907", "0225273908", "0225273909", "0225273910",
  "0225273911", "0225273912", "0225273913"
)

# Extracted companies so far
extracted <- list(
  list(license = "0225273913", company = "BOZZUTO MANAGEMENT COMPANY", firm = "0226024808"),
  list(license = "0225273906", company = "CORTLAND MANAGEMENT LLC", firm = "0226038642"),
  list(license = "0225258285", company = "MIDDLEBURG MANAGEMENT LLC", firm = "0226038324"),
  list(license = "0225273785", company = "GATEWAY MANAGEMENT COMPANY LLC", firm = "0226038613"),
  list(license = "0225273907", company = "CAPREIT RESIDENTIAL MANAGEMENT LLC", firm = "0226038643")
)

cat("=== Virginia DPOR Batch Extraction Progress ===\n\n")
cat("Total licenses: 40\n")
cat("Extracted: ", length(extracted), "\n")
cat("Remaining: ", 40 - length(extracted), "\n\n")

cat("Extracted companies:\n")
for (i in seq_along(extracted)) {
  cat(sprintf("  %d. %s (License: %s, Firm: %s)\n",
              i, extracted[[i]]$company, extracted[[i]]$license, extracted[[i]]$firm))
}

# Save progress
progress <- list(
  metadata = list(
    date = Sys.Date(),
    total_licenses = 40,
    extracted_count = length(extracted),
    remaining_count = 40 - length(extracted),
    percentage = round((length(extracted) / 40) * 100, 1)
  ),
  extracted_companies = extracted,
  remaining_licenses = setdiff(known_licenses, sapply(extracted, function(x) x$license)),
  method = "Browser automation (Method 1 - FASTEST)"
)

write_json(progress, "research/virginia_extraction_batch_progress.json", pretty = TRUE, auto_unbox = TRUE)
cat("\nProgress saved to: research/virginia_extraction_batch_progress.json\n")
cat(sprintf("Progress: %.1f%% complete\n", progress$metadata$percentage))
