#!/usr/bin/env Rscript
# Extract full text from PDFs to find UPL evidence
# Specifically look for RA denial and interactive process language

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
OUTPUT_FILE <- file.path(RESEARCH_DIR, "upl_evidence_extracted.json")

# UPL indicators to search for
get_upl_indicators <- function() {
  indicators <- list(
    legal_terms = c(
      "reasonable accommodation",
      "denied",
      "denial",
      "interactive process",
      "ADA",
      "Americans with Disabilities Act",
      "Fair Housing Act",
      "FHA",
      "disability",
      "accommodation request",
      "undue hardship",
      "legal advice",
      "legal representation",
      "counsel",
      "attorney",
      "violation",
      "breach",
      "liability",
      "compliance",
      "legal requirement"
    ),
    actions_suggesting_upl = c(
      "denying",
      "determining",
      "advising",
      "recommending legal action",
      "interpreting law",
      "applying legal standards"
    )
  )
  return(indicators)
}

# Extract text from PDF evidence
extract_upl_evidence <- function() {
  cat("\n=== Extracting UPL Evidence from PDFs ===\n")

  # Load PDF evidence
  pdf_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (!file.exists(pdf_file)) {
    return(list())
  }

  pdf_data <- fromJSON(pdf_file, simplifyDataFrame = FALSE)
  indicators <- get_upl_indicators()

  upl_evidence <- list()

  # Search each PDF
  for (pdf in pdf_data) {
    if (!is.null(pdf$text_preview) && length(pdf$text_preview) > 0) {
      text <- paste(pdf$text_preview, collapse = " ")

      if (is.null(text) || is.na(text) || nchar(text) == 0) {
        next
      }

      # Check if Hyland is mentioned
      if (grepl("hyland|ehyland", text, ignore.case = TRUE)) {
        evidence <- list(
          file = if (!is.null(pdf$file) && length(pdf$file) > 0) pdf$file[[1]] else NA,
          file_path = if (!is.null(pdf$file_path) && length(pdf$file_path) > 0) pdf$file_path[[1]] else NA,
          hyland_mentioned = TRUE,
          legal_terms_found = c(),
          actions_found = c(),
          potential_upl = FALSE
        )

        # Search for legal terms
        for (term in indicators$legal_terms) {
          if (grepl(term, text, ignore.case = TRUE)) {
            evidence$legal_terms_found <- c(evidence$legal_terms_found, term)
          }
        }

        # Search for actions suggesting UPL
        for (action in indicators$actions_suggesting_upl) {
          if (grepl(action, text, ignore.case = TRUE)) {
            evidence$actions_found <- c(evidence$actions_found, action)
          }
        }

        # Determine if potential UPL
        if (length(evidence$legal_terms_found) > 0 &&
            (any(grepl("denied|denial", evidence$legal_terms_found, ignore.case = TRUE)) ||
             any(grepl("interactive process", evidence$legal_terms_found, ignore.case = TRUE)))) {
          evidence$potential_upl <- TRUE
          evidence$upl_severity <- "HIGH"
          evidence$upl_type <- "RA Denial and Legal Process Language"
        }

        if (length(evidence$legal_terms_found) > 0 || length(evidence$actions_found) > 0) {
          upl_evidence[[length(upl_evidence) + 1]] <- evidence
        }
      }
    }
  }

  return(upl_evidence)
}

# Main extraction
main_extraction <- function() {
  cat("=== UPL Evidence Extraction ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Extract evidence
  evidence <- extract_upl_evidence()

  # Count potential UPL cases
  potential_upl_count <- 0
  for (e in evidence) {
    if (!is.null(e$potential_upl) && e$potential_upl) {
      potential_upl_count <- potential_upl_count + 1
    }
  }

  # Create results
  results <- list(
    extraction_date = as.character(Sys.Date()),
    total_files_searched = 14,  # From PDF evidence
    files_with_upl_indicators = length(evidence),
    evidence = evidence,
    summary = list(
      potential_upl_cases = potential_upl_count,
      files_with_legal_terms = length(evidence),
      note = "Based on PDF text extraction. Full text review recommended."
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved evidence to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Extraction Summary ===\n")
  cat("Files with UPL Indicators:", results$files_with_upl_indicators, "\n")
  cat("Potential UPL Cases:", results$summary$potential_upl_cases, "\n")

  cat("\n=== Extraction Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_extraction()
}
