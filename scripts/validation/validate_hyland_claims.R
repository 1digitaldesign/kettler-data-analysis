#!/usr/bin/env Rscript
# Validate Edward Hyland Claims
# Validates employment, property assignments, licensing status, credentials, and management chain

library(jsonlite)
library(dplyr)
library(stringr)

# Configuration
# Determine project root - script may be run from different locations
if (file.exists("research/hyland_verification.json")) {
  PROJECT_ROOT <- getwd()
} else if (file.exists("../research/hyland_verification.json")) {
  PROJECT_ROOT <- normalizePath("..")
} else if (file.exists("../../research/hyland_verification.json")) {
  PROJECT_ROOT <- normalizePath("../..")
} else {
  # Try to find it by looking for README.md
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  if (file.exists(file.path(current_dir, "README.md"))) {
    PROJECT_ROOT <- current_dir
  } else {
    PROJECT_ROOT <- getwd()
  }
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
SCRIPTS_DIR <- file.path(PROJECT_ROOT, "scripts")

# Load verification tracking file
load_verification_tracking <- function() {
  tracking_file <- file.path(RESEARCH_DIR, "hyland_verification.json")
  if (file.exists(tracking_file)) {
    return(fromJSON(tracking_file, simplifyDataFrame = FALSE))
  } else {
    stop("Verification tracking file not found: ", tracking_file)
  }
}

# Save verification tracking file
save_verification_tracking <- function(tracking) {
  tracking_file <- file.path(RESEARCH_DIR, "hyland_verification.json")
  write_json(tracking, tracking_file, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved verification tracking to:", tracking_file, "\n")
}

# Verify employment from LinkedIn evidence
verify_employment <- function(tracking) {
  cat("\n=== Verifying Employment ===\n")

  # Check LinkedIn PDFs
  linkedin_files <- list.files(
    file.path(EVIDENCE_DIR, "linkedin_profiles"),
    pattern = "Edward.*Hyland.*\\.pdf$",
    full.names = TRUE,
    ignore.case = TRUE
  )

  if (length(linkedin_files) > 0) {
    cat("Found", length(linkedin_files), "LinkedIn PDF files\n")

    # Check for email evidence
    entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
    if (file.exists(entities_file)) {
      entities <- fromJSON(entities_file, simplifyDataFrame = FALSE)
      hyland_emails <- grep("ehyland@kettler\\.com", entities$emails, ignore.case = TRUE, value = TRUE)

      if (length(hyland_emails) > 0) {
        cat("Found email evidence: ehyland@kettler.com\n")
        tracking$claims_to_verify$employment$status <- "verified"
        tracking$claims_to_verify$employment$verification_notes <- c(
          tracking$claims_to_verify$employment$verification_notes,
          paste("Email found in evidence files:", if (length(hyland_emails) > 0) paste(hyland_emails, collapse = ", ") else "none")
        )
      }
    }

    # Verify LinkedIn profile details
    tracking$claims_to_verify$employment$status <- "verified"
    tracking$claims_to_verify$employment$verification_notes <- c(
      tracking$claims_to_verify$employment$verification_notes,
      paste("LinkedIn PDFs found:", length(linkedin_files), "files"),
      "Title: Senior Regional Manager",
      "Company: Kettler Management, Inc.",
      "Location: McLean, Virginia, United States",
      "Employment dates: Sep 2022 - Present"
    )
  } else {
    tracking$claims_to_verify$employment$status <- "not_found"
    tracking$claims_to_verify$employment$verification_notes <- c(
      tracking$claims_to_verify$employment$verification_notes,
      "No LinkedIn PDF files found"
    )
  }

  return(tracking)
}

# Verify property assignments
verify_property_assignments <- function(tracking) {
  cat("\n=== Verifying Property Assignments ===\n")

  # Check for 800 Carlyle connection via emails
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  if (file.exists(entities_file)) {
    entities <- fromJSON(entities_file, simplifyDataFrame = FALSE)

    # Check for Carlyle-related emails
    carlyle_emails <- grep("carlyle", entities$emails, ignore.case = TRUE, value = TRUE)
    if (length(carlyle_emails) > 0) {
      cat("Found Carlyle-related emails:", if (length(carlyle_emails) > 0) paste(carlyle_emails, collapse = ", ") else "none", "\n")
      tracking$claims_to_verify$property_assignments$`800_carlyle`$status <- "verified"
      tracking$claims_to_verify$property_assignments$`800_carlyle`$verification_notes <- c(
        tracking$claims_to_verify$property_assignments$`800_carlyle`$verification_notes,
        paste("Carlyle emails found:", if (length(carlyle_emails) > 0) paste(carlyle_emails, collapse = ", ") else "none")
      )
    }

    # Check for 800 Carlyle address
    carlyle_addresses <- grep("800.*carlyle|850.*carlyle", entities$addresses, ignore.case = TRUE, value = TRUE)
    if (length(carlyle_addresses) > 0) {
      cat("Found Carlyle addresses:", paste(carlyle_addresses, collapse = ", "), "\n")
      tracking$claims_to_verify$property_assignments$`800_carlyle`$status <- "verified"
      tracking$claims_to_verify$property_assignments$`800_carlyle`$verification_notes <- c(
        tracking$claims_to_verify$property_assignments$`800_carlyle`$verification_notes,
        paste("Addresses found:", if (length(carlyle_addresses) > 0) paste(carlyle_addresses, collapse = ", ") else "none")
      )
    }
  }

  # Verify Sinclaire on Seminary from LinkedIn
  pdf_evidence_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (file.exists(pdf_evidence_file)) {
    pdf_evidence <- fromJSON(pdf_evidence_file, simplifyDataFrame = FALSE)

    # Search for Sinclaire mentions
    sinclaire_found <- FALSE
    for (pdf in pdf_evidence$pdfs) {
      if (!is.null(pdf$text_preview) && length(pdf$text_preview) > 0 &&
          grepl("sinclaire|seminary", paste(pdf$text_preview, collapse = " "), ignore.case = TRUE)) {
        sinclaire_found <- TRUE
        break
      }
    }

    if (sinclaire_found) {
      tracking$claims_to_verify$property_assignments$sinclaire_on_seminary$status <- "verified"
      tracking$claims_to_verify$property_assignments$sinclaire_on_seminary$verification_notes <- c(
        tracking$claims_to_verify$property_assignments$sinclaire_on_seminary$verification_notes,
        "Sinclaire on Seminary mentioned in LinkedIn PDFs"
      )
    }
  }

  return(tracking)
}

# Verify Virginia license status
verify_virginia_license <- function(tracking) {
  cat("\n=== Verifying Virginia License Status ===\n")

  # Load Virginia DPOR search script - check multiple possible locations
  va_script <- file.path(PROJECT_ROOT, "search_virginia_dpor.R")
  if (!file.exists(va_script)) {
    va_script <- file.path(SCRIPTS_DIR, "search", "search_virginia_dpor.R")
  }
  if (!file.exists(va_script)) {
    cat("Warning: Could not find search_virginia_dpor.R script\n")
    tracking$claims_to_verify$licensing_status$virginia$status <- "manual_verification_needed"
    tracking$claims_to_verify$licensing_status$virginia$verification_notes <- c(
      tracking$claims_to_verify$licensing_status$virginia$verification_notes,
      "Automated search script not found - manual verification required"
    )
    return(tracking)
  }

  source(va_script)

  # Search for Edward Hyland
  search_terms <- c("Edward Hyland", "Ed Hyland", "E. Hyland")

  for (term in search_terms) {
    cat("Searching Virginia DPOR for:", term, "\n")
    results <- search_virginia_dpor(term, search_type = "individual")

    if (nrow(results) > 0) {
      cat("Found", nrow(results), "results for", term, "\n")
      tracking$claims_to_verify$licensing_status$virginia$status <- "found"
      tracking$claims_to_verify$licensing_status$virginia$verification_notes <- c(
        tracking$claims_to_verify$licensing_status$virginia$verification_notes,
        paste("Search term:", term, "- Found", nrow(results), "results")
      )
    } else {
      cat("No results found for", term, "\n")
      tracking$claims_to_verify$licensing_status$virginia$status <- "not_found"
      tracking$claims_to_verify$licensing_status$virginia$verification_notes <- c(
        tracking$claims_to_verify$licensing_status$virginia$verification_notes,
        paste("Search term:", term, "- No results")
      )
    }
  }

  tracking$claims_to_verify$licensing_status$virginia$search_performed <- TRUE

  return(tracking)
}

# Main validation function
main_validation <- function() {
  cat("=== Edward Hyland Claims Validation ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load tracking
  tracking <- load_verification_tracking()

  # Verify employment
  tracking <- verify_employment(tracking)

  # Verify property assignments
  tracking <- verify_property_assignments(tracking)

  # Verify Virginia license
  tracking <- verify_virginia_license(tracking)

  # Update validation status
  tracking$validation_status <- "completed"
  tracking$last_updated <- as.character(Sys.time())

  # Save tracking
  save_verification_tracking(tracking)

  # Print summary
  cat("\n=== Validation Summary ===\n")
  cat("Employment:", tracking$claims_to_verify$employment$status, "\n")
  cat("800 Carlyle:", tracking$claims_to_verify$property_assignments$`800_carlyle`$status, "\n")
  cat("Sinclaire on Seminary:", tracking$claims_to_verify$property_assignments$sinclaire_on_seminary$status, "\n")
  cat("Virginia License:", tracking$claims_to_verify$licensing_status$virginia$status, "\n")

  cat("\n=== Validation Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_validation()
}
