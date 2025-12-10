#!/usr/bin/env Rscript
# Virginia DPOR Batch Extraction Script
# Uses browser automation via system calls or manual extraction tracking

library(jsonlite)
library(dplyr)

# Known license numbers (first 10 visible on page 1)
virginia_licenses <- c(
  "0225258285", "0225273785",
  "0225273906", "0225273907", "0225273908", "0225273909", "0225273910",
  "0225273911", "0225273912", "0225273913"
)

# Already extracted companies
extracted <- list(
  list(license = "0225273913", company = "BOZZUTO MANAGEMENT COMPANY", firm_license = "0226024808"),
  list(license = "0225273906", company = "CORTLAND MANAGEMENT LLC", firm_license = "0226038642"),
  list(license = "0225258285", company = "MIDDLEBURG MANAGEMENT LLC", firm_license = "0226038324")
)

# Remaining licenses to extract
remaining <- setdiff(virginia_licenses, sapply(extracted, function(x) x$license))

cat("=== Virginia DPOR Batch Extraction ===\n\n")
cat("Total licenses: ", length(virginia_licenses), "\n")
cat("Extracted: ", length(extracted), "\n")
cat("Remaining: ", length(remaining), "\n\n")

cat("Remaining licenses:\n")
for (lic in remaining) {
  cat("  - ", lic, "\n")
}

# Create extraction template
extraction_template <- list(
  metadata = list(
    date = Sys.Date(),
    method = "Browser automation / Manual extraction",
    status = "in_progress"
  ),
  extracted = extracted,
  remaining = remaining,
  instructions = list(
    step1 = "Navigate to https://www.dpor.virginia.gov/LicenseLookup",
    step2 = "Search for license number",
    step3 = "Click on license number button",
    step4 = "Click 'Related Licenses' tab",
    step5 = "Extract company name from table (second column)"
  )
)

write_json(extraction_template, "research/virginia_extraction_template.json", pretty = TRUE, auto_unbox = TRUE)
cat("\nExtraction template saved to: research/virginia_extraction_template.json\n")
