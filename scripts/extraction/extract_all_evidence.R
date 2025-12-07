#!/usr/bin/env Rscript
# Extract All Evidence - Master Script
# Extracts data from all PDFs and Excel files in evidence directory

library(pdftools)
library(jsonlite)

# Configuration
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")

# Source extraction scripts
source(file.path(PROJECT_ROOT, "scripts", "extraction", "extract_pdf_evidence.R"))
source(file.path(PROJECT_ROOT, "scripts", "extraction", "extract_excel_evidence.R"))

# Main function
main_extract_all <- function() {
  cat("=== Extracting All Evidence ===\n\n")

  # Extract PDFs from all subdirectories
  cat("Step 1: Extracting PDF evidence...\n")
  pdf_dirs <- c(
    file.path(EVIDENCE_DIR, "pdfs"),
    file.path(EVIDENCE_DIR, "emails"),
    file.path(EVIDENCE_DIR, "legal_documents"),
    file.path(EVIDENCE_DIR, "linkedin_profiles"),
    file.path(EVIDENCE_DIR, "airbnb"),
    file.path(EVIDENCE_DIR, "accommodation_forms"),
    file.path(EVIDENCE_DIR, "correspondence")
  )

  all_pdf_extracted <- list()
  for (pdf_dir in pdf_dirs) {
    if (dir.exists(pdf_dir)) {
      # Temporarily set EVIDENCE_DIR for PDF extraction
      original_dir <- EVIDENCE_DIR
      EVIDENCE_DIR <<- pdf_dir

      pdf_results <- process_all_pdfs()
      if (!is.null(pdf_results) && length(pdf_results) > 0) {
        all_pdf_extracted <- c(all_pdf_extracted, pdf_results)
      }

      EVIDENCE_DIR <<- original_dir
    }
  }

  # Extract Excel files
  cat("\nStep 2: Extracting Excel evidence...\n")
  excel_results <- process_all_excel()

  # Combine all results
  cat("\nStep 3: Combining all evidence...\n")
  combined_evidence <- list(
    pdfs = all_pdf_extracted,
    excel = excel_results,
    extraction_date = Sys.Date()
  )

  # Save combined evidence
  combined_file <- file.path(RESEARCH_DIR, "all_evidence_extracted.json")
  write_json(combined_evidence, combined_file, pretty = TRUE)
  cat("Saved combined evidence to:", combined_file, "\n")

  cat("\n=== Extraction Complete ===\n")
  cat("PDF files processed:", length(all_pdf_extracted), "\n")
  cat("Excel files processed:", ifelse(is.null(excel_results), 0, length(excel_results)), "\n")
}

# Run if executed as script
if (!interactive()) {
  main_extract_all()
}
