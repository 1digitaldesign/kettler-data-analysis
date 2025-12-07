#!/usr/bin/env Rscript
# Investigate Edward Hyland's potential unauthorized practice of law
# Focus on RA denial and interactive process statements

library(jsonlite)
library(stringr)

# Configuration
if (file.exists("research/all_entities_extracted.json")) {
  PROJECT_ROOT <- getwd()
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "hyland_upl_investigation.json")

# Load PDF evidence
load_pdf_evidence <- function() {
  pdf_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (!file.exists(pdf_file)) {
    return(list())
  }
  return(fromJSON(pdf_file, simplifyDataFrame = FALSE))
}

# Search for UPL indicators
investigate_upl <- function(pdf_data) {
  cat("\n=== Investigating Unauthorized Practice of Law ===\n")

  upl_indicators <- list()

  # Search for legal language that suggests legal advice
  legal_keywords <- c(
    "interactive process",
    "reasonable accommodation",
    "denied",
    "legal",
    "attorney",
    "counsel",
    "advice",
    "representation",
    "ADA",
    "Fair Housing",
    "FHA",
    "violation",
    "breach",
    "liability",
    "compliance"
  )

  # Search each PDF
  for (pdf in pdf_data) {
    if (!is.null(pdf$text_preview)) {
      text <- paste(pdf$text_preview, collapse = " ")

      # Check for Hyland's name
      if (grepl("hyland|ehyland", text, ignore.case = TRUE)) {
        # Check for legal language
        found_keywords <- c()
        for (keyword in legal_keywords) {
          if (grepl(keyword, text, ignore.case = TRUE)) {
            found_keywords <- c(found_keywords, keyword)
          }
        }

        if (length(found_keywords) > 0) {
          upl_indicators[[length(upl_indicators) + 1]] <- list(
            file = pdf$file[[1]],
            file_path = pdf$file_path[[1]],
            keywords_found = found_keywords,
            context = "Hyland mentioned with legal language",
            potential_upl = TRUE
          )
        }
      }
    }
  }

  return(upl_indicators)
}

# Analyze RA denial
analyze_ra_denial <- function(pdf_data) {
  cat("\n=== Analyzing RA Denial ===\n")

  ra_analysis <- list()

  # Search for RA-related content
  for (pdf in pdf_data) {
    if (!is.null(pdf$text_preview)) {
      text <- paste(pdf$text_preview, collapse = " ")

      # Check for RA denial language
      if (grepl("reasonable accommodation|denied|denial", text, ignore.case = TRUE) &&
          grepl("hyland|ehyland", text, ignore.case = TRUE)) {

        ra_analysis$denial_found <- TRUE
        ra_analysis$file <- pdf$file[[1]]
        ra_analysis$file_path <- pdf$file_path[[1]]

        # Extract relevant text
        sentences <- strsplit(text, "[.!?]")[[1]]
        relevant_sentences <- sentences[grepl("accommodation|denied|denial", sentences, ignore.case = TRUE)]
        ra_analysis$relevant_text <- relevant_sentences[1:min(5, length(relevant_sentences))]
      }

      # Check for interactive process language
      if (grepl("interactive process", text, ignore.case = TRUE) &&
          grepl("hyland|ehyland", text, ignore.case = TRUE)) {

        ra_analysis$interactive_process_mentioned <- TRUE
        if (is.null(ra_analysis$file)) {
          ra_analysis$file <- pdf$file[[1]]
          ra_analysis$file_path <- pdf$file_path[[1]]
        }

        # Extract relevant text
        sentences <- strsplit(text, "[.!?]")[[1]]
        relevant_sentences <- sentences[grepl("interactive", sentences, ignore.case = TRUE)]
        ra_analysis$interactive_process_text <- relevant_sentences[1:min(5, length(relevant_sentences))]
      }
    }
  }

  return(ra_analysis)
}

# Check if Hyland is licensed to practice law
check_law_license <- function() {
  cat("\n=== Checking Law License ===\n")

  # Load Hyland verification
  hyland_file <- file.path(RESEARCH_DIR, "hyland_verification.json")
  if (!file.exists(hyland_file)) {
    return(list(license_check = "NOT_PERFORMED"))
  }

  hyland <- fromJSON(hyland_file, simplifyDataFrame = FALSE)

  # Check for law license in credentials
  law_license_found <- FALSE

  # Note: Would need to search state bar associations
  # This is a placeholder for that search

  return(list(
    law_license_found = law_license_found,
    note = "State bar association search needed",
    violation_if_no_license = "Unauthorized Practice of Law (UPL)"
  ))
}

# Main investigation
main_investigation <- function() {
  cat("=== Edward Hyland UPL Investigation ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load PDF evidence
  pdf_data <- load_pdf_evidence()
  cat("Loaded", length(pdf_data), "PDF files\n")

  # Investigate UPL indicators
  upl_indicators <- investigate_upl(pdf_data)

  # Analyze RA denial
  ra_analysis <- analyze_ra_denial(pdf_data)

  # Check law license
  law_license_check <- check_law_license()

  # Create results
  results <- list(
    investigation_date = as.character(Sys.Date()),
    subject = "Edward Hyland",
    role = "Senior Regional Manager",
    employer = "Kettler Management Inc.",
    upl_indicators = upl_indicators,
    ra_denial_analysis = ra_analysis,
    law_license_check = law_license_check,
    conclusions = list(
      potential_upl = length(upl_indicators) > 0,
      ra_denial_found = ra_analysis$denial_found %||% FALSE,
      interactive_process_mentioned = ra_analysis$interactive_process_mentioned %||% FALSE,
      violation_type = if (length(upl_indicators) > 0) "Unauthorized Practice of Law" else "None identified",
      severity = if (length(upl_indicators) > 0) "HIGH" else "UNKNOWN"
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved investigation results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Investigation Summary ===\n")
  cat("UPL Indicators Found:", length(upl_indicators), "\n")
  cat("RA Denial Found:", results$conclusions$ra_denial_found, "\n")
  cat("Interactive Process Mentioned:", results$conclusions$interactive_process_mentioned, "\n")
  cat("Potential UPL:", results$conclusions$potential_upl, "\n")

  cat("\n=== Investigation Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_investigation()
}
