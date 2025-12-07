#!/usr/bin/env Rscript
# Extract Evidence from Excel Documents
# Extracts data from Excel files for fraud investigation

library(readxl)
library(dplyr)
library(jsonlite)
library(stringr)

# Configuration
EVIDENCE_DIR <- "../../evidence/excel_files"
OUTPUT_DIR <- "../../research"
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)

# Extract data from Excel file
extract_excel_data <- function(excel_path) {
  tryCatch({
    # Get sheet names
    sheet_names <- excel_sheets(excel_path)

    extracted <- list(
      file = basename(excel_path),
      file_path = excel_path,
      sheets = list()
    )

    # Extract data from each sheet
    for (sheet_name in sheet_names) {
      tryCatch({
        data <- read_excel(excel_path, sheet = sheet_name)

        # Extract key information
        sheet_data <- list(
          sheet_name = sheet_name,
          row_count = nrow(data),
          col_count = ncol(data),
          column_names = names(data),
          sample_data = if (nrow(data) > 0) {
            # Get first few rows as sample
            head(data, min(5, nrow(data)))
          } else {
            NULL
          }
        )

        # Extract entities (emails, addresses, phone numbers, dates)
        if (nrow(data) > 0) {
          all_text <- paste(as.character(unlist(data)), collapse = " ")

          # Extract emails
          email_pattern <- "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
          emails <- unique(unlist(str_extract_all(all_text, email_pattern)))

          # Extract phone numbers
          phone_pattern <- "\\b(\\+?1[-.]?)?\\(?([0-9]{3})\\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\\b"
          phones <- unique(unlist(str_extract_all(all_text, phone_pattern)))

          # Extract dates
          date_pattern <- "(?i)\\b(\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}|\\d{4}[-]\\d{2}[-]\\d{2}|(January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{1,2},?\\s+\\d{4})\\b"
          dates <- unique(unlist(str_extract_all(all_text, regex(date_pattern, ignore_case = TRUE))))

          # Extract addresses
          address_pattern <- "(?i)\\d+\\s+[A-Za-z0-9\\s,.-]+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Court|Ct|Way|Place|Pl)[^,]*,\\s*[A-Za-z\\s]+,\\s*[A-Z]{2}\\s+\\d{5}"
          addresses <- unique(unlist(str_extract_all(all_text, regex(address_pattern, ignore_case = TRUE))))

          sheet_data$entities <- list(
            emails = emails,
            phones = phones,
            dates = dates,
            addresses = addresses
          )
        }

        extracted$sheets[[length(extracted$sheets) + 1]] <- sheet_data

      }, error = function(e) {
        cat("  Error reading sheet", sheet_name, ":", e$message, "\n")
      })
    }

    return(extracted)

  }, error = function(e) {
    cat("Error extracting from", excel_path, ":", e$message, "\n")
    return(NULL)
  })
}

# Process all Excel files
process_all_excel <- function() {
  excel_files <- list.files(EVIDENCE_DIR, pattern = "\\.(xlsx|xls)$", full.names = TRUE, ignore.case = TRUE)

  if (length(excel_files) == 0) {
    cat("No Excel files found in", EVIDENCE_DIR, "\n")
    return()
  }

  cat("Processing", length(excel_files), "Excel file(s)...\n\n")

  all_extracted <- list()

  for (excel_file in excel_files) {
    cat("Processing:", basename(excel_file), "\n")

    extracted <- extract_excel_data(excel_file)

    if (!is.null(extracted)) {
      all_extracted[[length(all_extracted) + 1]] <- extracted

      # Print summary
      total_emails <- sum(sapply(extracted$sheets, function(s) length(s$entities$emails)))
      total_addresses <- sum(sapply(extracted$sheets, function(s) length(s$entities$addresses)))
      cat("  Sheets:", length(extracted$sheets), "| Emails:", total_emails, "| Addresses:", total_addresses, "\n")
    }
  }

  # Save extracted data
  output_file <- file.path(OUTPUT_DIR, "excel_evidence_extracted.json")
  write_json(all_extracted, output_file, pretty = TRUE)
  cat("\nSaved extracted data to:", output_file, "\n")

  # Create summary CSV
  summary_data <- data.frame(
    file = sapply(all_extracted, function(x) x$file),
    sheets = sapply(all_extracted, function(x) length(x$sheets)),
    total_rows = sapply(all_extracted, function(x) sum(sapply(x$sheets, function(s) s$row_count))),
    emails = sapply(all_extracted, function(x) sum(sapply(x$sheets, function(s) length(s$entities$emails)))),
    addresses = sapply(all_extracted, function(x) sum(sapply(x$sheets, function(s) length(s$entities$addresses)))),
    stringsAsFactors = FALSE
  )

  summary_file <- file.path(OUTPUT_DIR, "excel_evidence_summary.csv")
  write.csv(summary_data, summary_file, row.names = FALSE)
  cat("Saved summary to:", summary_file, "\n")

  return(all_extracted)
}

# Main execution
if (!interactive()) {
  # Check if readxl is installed
  if (!require(readxl, quietly = TRUE)) {
    cat("Installing readxl package...\n")
    install.packages("readxl", repos = "https://cran.rstudio.com/")
    library(readxl)
  }

  process_all_excel()
}
