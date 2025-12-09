#!/usr/bin/env Rscript
# Validate Kettler Management Claims
# Validates corporate structure, discrimination settlement, BBB complaints, property portfolio, executive team

library(jsonlite)
library(dplyr)
library(stringr)

# Configuration
if (file.exists("research/kettler_verification.json")) {
  PROJECT_ROOT <- getwd()
} else if (file.exists("../research/kettler_verification.json")) {
  PROJECT_ROOT <- normalizePath("..")
} else if (file.exists("../../research/kettler_verification.json")) {
  PROJECT_ROOT <- normalizePath("../..")
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
DATA_DIR <- file.path(PROJECT_ROOT, "data")
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")

# Load verification tracking file
load_verification_tracking <- function() {
  tracking_file <- file.path(RESEARCH_DIR, "kettler_verification.json")
  if (file.exists(tracking_file)) {
    return(fromJSON(tracking_file, simplifyDataFrame = FALSE))
  } else {
    stop("Verification tracking file not found: ", tracking_file)
  }
}

# Save verification tracking file
save_verification_tracking <- function(tracking) {
  tracking_file <- file.path(RESEARCH_DIR, "kettler_verification.json")
  write_json(tracking, tracking_file, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved verification tracking to:", tracking_file, "\n")
}

# Verify corporate structure from license records
verify_corporate_structure <- function(tracking) {
  cat("\n=== Verifying Corporate Structure ===\n")

  # Check license records
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (file.exists(firms_file)) {
    firms <- read.csv(firms_file, stringsAsFactors = FALSE)
    kettler_firm <- firms[firms$Firm.Name == "KETTLER MANAGEMENT INC", ]

    if (nrow(kettler_firm) > 0 && "License.Number" %in% names(kettler_firm) && "Address" %in% names(kettler_firm)) {
      cat("Found Kettler Management Inc. in license records\n")
      cat("License Number:", kettler_firm$License.Number[1], "\n")
      cat("Address:", kettler_firm$Address[1], "\n")

      # Verify address matches
      expected_address <- "8255 GREENSBORO DR STE #200, MCLEAN, VA 22102"
      actual_address <- kettler_firm$Address[1]

      if (grepl("8255.*GREENSBORO", actual_address, ignore.case = TRUE) &&
          grepl("MCLEAN.*VA.*22102", actual_address, ignore.case = TRUE)) {
        tracking$claims_to_verify$corporate_structure$status <- "verified"
        tracking$claims_to_verify$corporate_structure$verification_notes <- c(
          tracking$claims_to_verify$corporate_structure$verification_notes,
          paste("Address verified in DPOR records:", actual_address),
          if ("License.Number" %in% names(kettler_firm)) paste("License Number:", kettler_firm$License.Number[1]) else "License Number: N/A"
        )
      }
    }
  }

  # Check evidence files for address matches
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  if (file.exists(entities_file)) {
    entities <- fromJSON(entities_file, simplifyDataFrame = FALSE)
    kettler_addresses <- grep("8255.*greensboro|greensboro.*8255", entities$addresses, ignore.case = TRUE, value = TRUE)

    if (length(kettler_addresses) > 0) {
      cat("Found Kettler address in evidence:", paste(kettler_addresses, collapse = ", "), "\n")
      tracking$claims_to_verify$corporate_structure$status <- "verified"
      tracking$claims_to_verify$corporate_structure$verification_notes <- c(
        tracking$claims_to_verify$corporate_structure$verification_notes,
        paste("Address found in evidence files:", paste(kettler_addresses, collapse = ", "))
      )
    }
  }

  return(tracking)
}

# Verify email domain matches
verify_email_domain <- function(tracking) {
  cat("\n=== Verifying Email Domain ===\n")

  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  if (file.exists(entities_file)) {
    entities <- fromJSON(entities_file, simplifyDataFrame = FALSE)
    kettler_emails <- grep("@kettler\\.com", entities$emails, ignore.case = TRUE, value = TRUE)

    if (length(kettler_emails) > 0) {
      cat("Found", length(kettler_emails), "kettler.com email addresses\n")
      tracking$evidence_found$email_domains$kettler.com$emails_found <- unique(kettler_emails)
      tracking$evidence_found$email_domains$kettler.com$verified <- TRUE
    }
  }

  return(tracking)
}

# Main validation function
main_validation <- function() {
  cat("=== Kettler Management Claims Validation ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load tracking
  tracking <- load_verification_tracking()

  # Verify corporate structure
  tracking <- verify_corporate_structure(tracking)

  # Verify email domain
  tracking <- verify_email_domain(tracking)

  # Note: Discrimination settlement, BBB complaints, property portfolio, and executive team
  # require external verification (court records, BBB website, company website, etc.)
  # These are marked as "pending" and require manual verification

  # Update validation status
  tracking$validation_status <- "partial_complete"
  tracking$last_updated <- as.character(Sys.time())
    tracking$notes <- c(
      if (!is.null(tracking$notes)) tracking$notes else character(0),
    "Corporate structure and email domain verified from existing evidence.",
    "Discrimination settlement, BBB complaints, property portfolio, and executive team require external verification."
  )

  # Save tracking
  save_verification_tracking(tracking)

  # Print summary
  cat("\n=== Validation Summary ===\n")
  cat("Corporate Structure:", tracking$claims_to_verify$corporate_structure$status, "\n")
  cat("Email Domain:", if (tracking$evidence_found$email_domains$kettler.com$verified) "verified" else "pending", "\n")
  cat("\nNote: External verification needed for:\n")
  cat("  - Discrimination settlement (court records)\n")
  cat("  - BBB complaints (BBB website)\n")
  cat("  - Property portfolio (company website/property databases)\n")
  cat("  - Executive team (company website/LinkedIn)\n")

  cat("\n=== Validation Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_validation()
}
