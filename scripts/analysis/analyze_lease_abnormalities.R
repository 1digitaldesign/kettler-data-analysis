#!/usr/bin/env Rscript
# Detailed analysis of lease agreement abnormalities
# Focus on violations, unusual terms, and connections to investigation

library(jsonlite)
library(stringr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_TIMELINES_DIR, "lease_abnormalities_detailed.json")

analyze_lease_abnormalities <- function() {
  cat("=== Detailed Lease Abnormality Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  lease_file <- file.path(EVIDENCE_DIR, "LeaseRenewalAgreement_6102025.txt")
  if (!file.exists(lease_file)) {
    stop("Lease file not found")
  }

  content <- readLines(lease_file, warn = FALSE)
  text <- paste(content, collapse = "\n")
  text_lower <- tolower(text)

  abnormalities <- list()

  # 1. Security Deposit Abnormality
  # $300 security deposit is extremely low for $2325/month rent
  # Standard is typically 1-2 months rent
  security_deposit <- 300
  monthly_rent <- 2325
  deposit_ratio <- security_deposit / monthly_rent

  if (deposit_ratio < 0.2) {
    abnormalities$low_security_deposit <- list(
      type = "unusually_low_security_deposit",
      description = "Security deposit is abnormally low relative to monthly rent",
      security_deposit = security_deposit,
      monthly_rent = monthly_rent,
      ratio = round(deposit_ratio, 3),
      standard_ratio = "0.5-2.0 months",
      severity = "medium",
      potential_reason = "May indicate financial risk or unusual lease terms"
    )
  }

  # 2. Owner vs Manager Discrepancy
  # Owner is "Azure Carlyle LP" but manager is "Kettler Management"
  # Need to verify connection
  if (grepl("azure carlyle", text_lower) && grepl("kettler", text_lower)) {
    abnormalities$owner_manager_discrepancy <- list(
      type = "owner_manager_separation",
      description = "Owner entity differs from management company",
      owner = "Azure Carlyle LP",
      manager = "Kettler Management",
      severity = "high",
      investigation_needed = "Verify relationship between Azure Carlyle LP and Kettler"
    )
  }

  # 3. Check for STR restrictions
  # Look for subletting or short-term rental prohibitions
  str_prohibitions <- grepl("sublet|sublease|short.?term|transient|airbnb|vrbo", text_lower)
  if (!str_prohibitions) {
    abnormalities$missing_str_prohibition <- list(
      type = "missing_str_prohibition",
      description = "Lease may not explicitly prohibit short-term rentals",
      severity = "medium",
      note = "Given 90+ STR violations, lease should explicitly prohibit"
    )
  }

  # 4. Check for reasonable accommodation language
  accommodation_language <- grepl("reasonable accommodation|disability|ada|fair housing act", text_lower)
  if (accommodation_language) {
    abnormalities$accommodation_language_found <- list(
      type = "accommodation_language_in_lease",
      description = "Reasonable accommodation language found in lease",
      severity = "high",
      relevance = "Given UPL investigation regarding RA denial"
    )
  }

  # 5. Check for attorney fee provisions
  attorney_fees <- grepl("attorney.*fee|legal.*fee|reasonable.*attorney", text_lower)
  if (attorney_fees) {
    abnormalities$attorney_fee_provision <- list(
      type = "attorney_fee_provision",
      description = "Attorney fee provisions found",
      severity = "low",
      note = "Standard provision but relevant given UPL investigation"
    )
  }

  # 6. Check for unusual fees
  # Look for excessive or unusual fees
  unusual_fees <- c(
    "amenity fee.*500",
    "animal.*500",
    "parking.*125",
    "trash.*10",
    "pest.*2.75"
  )

  fees_found <- list()
  for (fee_pattern in unusual_fees) {
    if (grepl(fee_pattern, text_lower)) {
      fees_found[[fee_pattern]] <- TRUE
    }
  }

  if (length(fees_found) > 0) {
    abnormalities$unusual_fees <- list(
      type = "multiple_additional_fees",
      description = "Multiple additional fees beyond base rent",
      fees = names(fees_found),
      severity = "low",
      note = "Amenity fee of $500 is significant"
    )
  }

  # 7. Check lease dates
  # Lease signed 02/26/2025, begins 04/17/2025, ends 05/16/2026
  # Check for timeline issues
  lease_signed <- "2025-02-26"
  lease_begins <- "2025-04-17"
  lease_ends <- "2026-05-16"

  abnormalities$lease_timeline <- list(
    type = "lease_timeline",
    signed_date = lease_signed,
    begins_date = lease_begins,
    ends_date = lease_ends,
    term_months = 13,
    note = "13-month lease term"
  )

  # 8. Check for Kettler Management contact info
  kettler_contact <- str_extract(text, regex("800.*John.*Carlyle.*22314.*703.*299.*7599", ignore_case = TRUE))
  if (!is.na(kettler_contact)) {
    abnormalities$kettler_contact_info <- list(
      type = "management_contact_info",
      description = "Kettler Management contact information found",
      address = "800 John Carlyle Street, Alexandria, VA 22314",
      phone = "(703)299-7599",
      severity = "low"
    )
  }

  # Compile results
  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      analysis_type = "detailed_lease_abnormality_analysis",
      file = lease_file
    ),
    abnormalities = abnormalities,
    summary = list(
      total_abnormalities = length(abnormalities),
      high_severity = sum(sapply(abnormalities, function(x) if(!is.null(x$severity)) x$severity == "high" else FALSE)),
      medium_severity = sum(sapply(abnormalities, function(x) if(!is.null(x$severity)) x$severity == "medium" else FALSE)),
      low_severity = sum(sapply(abnormalities, function(x) if(!is.null(x$severity)) x$severity == "low" else FALSE))
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved detailed analysis to:", OUTPUT_FILE, "\n")

  cat("\n=== Summary ===\n")
  cat("Total abnormalities:", results$summary$total_abnormalities, "\n")
  cat("High severity:", results$summary$high_severity, "\n")
  cat("Medium severity:", results$summary$medium_severity, "\n")
  cat("Low severity:", results$summary$low_severity, "\n")

  return(results)
}

if (!interactive()) analyze_lease_abnormalities()
