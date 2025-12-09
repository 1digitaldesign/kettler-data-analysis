#!/usr/bin/env Rscript
# Analyze All Evidence
# Cross-references all extracted evidence (PDFs, Excel) with license data

library(dplyr)
library(jsonlite)
library(stringr)

# Configuration
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
FILINGS_DIR <- file.path(PROJECT_ROOT, "filings")
DATA_DIR <- file.path(PROJECT_ROOT, "data")

# Load all evidence
load_all_evidence <- function() {
  evidence <- list()

  # Load PDF evidence (use simplifyDataFrame=FALSE to preserve structure)
  pdf_file <- file.path(RESEARCH_EVIDENCE_DIR, "pdf_evidence_extracted.json")
  if (file.exists(pdf_file)) {
    evidence$pdfs <- fromJSON(pdf_file, simplifyDataFrame = FALSE)
  }

  # Load Excel evidence
  excel_file <- file.path(RESEARCH_EVIDENCE_DIR, "excel_evidence_extracted.json")
  if (file.exists(excel_file)) {
    evidence$excel <- fromJSON(excel_file, simplifyDataFrame = FALSE)
  }

  # Load license data
  # Check for files in new location first, then fallback to root
  source_dir <- file.path(DATA_DIR, "source")
  firms_file <- if (file.exists(file.path(source_dir, "skidmore_all_firms_complete.csv"))) {
    file.path(source_dir, "skidmore_all_firms_complete.csv")
  } else if (file.exists(file.path(PROJECT_ROOT, "skidmore_all_firms_complete.csv"))) {
    file.path(PROJECT_ROOT, "skidmore_all_firms_complete.csv")
  } else {
    NULL
  }
  if (!is.null(firms_file) && file.exists(firms_file)) {
    evidence$firms <- read.csv(firms_file, stringsAsFactors = FALSE)
  }

  return(evidence)
}

# Extract all entities from evidence
extract_all_entities <- function(evidence) {
  entities <- list(
    emails = character(0),
    addresses = character(0),
    phone_numbers = character(0),
    names = character(0),
    dates = character(0),
    license_numbers = character(0)
  )

  # Extract from PDFs (now using simplifyDataFrame=FALSE, so it's a list)
  if (!is.null(evidence$pdfs) && is.list(evidence$pdfs)) {
    for (pdf in evidence$pdfs) {
      if (!is.null(pdf$entities) && is.list(pdf$entities)) {
        # Extract entities directly from list structure
        if (!is.null(pdf$entities$emails)) {
          entities$emails <- c(entities$emails, unlist(pdf$entities$emails))
        }
        if (!is.null(pdf$entities$addresses)) {
          entities$addresses <- c(entities$addresses, unlist(pdf$entities$addresses))
        }
        if (!is.null(pdf$entities$phones)) {
          entities$phone_numbers <- c(entities$phone_numbers, unlist(pdf$entities$phones))
        }
        if (!is.null(pdf$entities$dates)) {
          entities$dates <- c(entities$dates, unlist(pdf$entities$dates))
        }
        if (!is.null(pdf$entities$license_numbers)) {
          entities$license_numbers <- c(entities$license_numbers, unlist(pdf$entities$license_numbers))
        }
      }
    }
  }

  # Extract from Excel files
  if (!is.null(evidence$excel) && length(evidence$excel) > 0) {
    for (excel in evidence$excel) {
      if (!is.null(excel$sheets)) {
        for (sheet in excel$sheets) {
          if (!is.null(sheet$entities)) {
            entities$emails <- c(entities$emails, unlist(sheet$entities$emails))
            entities$addresses <- c(entities$addresses, unlist(sheet$entities$addresses))
            entities$phone_numbers <- c(entities$phone_numbers, unlist(sheet$entities$phones))
            entities$dates <- c(entities$dates, unlist(sheet$entities$dates))
          }
        }
      }
    }
  }

  # Remove duplicates and empty values
  entities <- lapply(entities, function(x) unique(x[x != "" & !is.na(x)]))

  return(entities)
}

# Cross-reference entities with license data
cross_reference_entities <- function(entities, firms) {
  matches <- list()

  # Match emails
  if (!is.null(firms) && length(entities$emails) > 0) {
    kettler_emails <- entities$emails[grepl("kettler", entities$emails, ignore.case = TRUE)]
    matches$kettler_emails <- kettler_emails
  }

  # Match addresses
  if (!is.null(firms) && length(entities$addresses) > 0) {
    matched_firms <- NULL

    for (addr in entities$addresses) {
      # Extract street number
      street_num <- str_extract(addr, "^\\d+")
      city_state <- str_extract(addr, "[A-Za-z]+,\\s*[A-Z]{2}")
      if (!is.na(street_num) && !is.na(city_state)) {
        firm_matches <- firms %>%
          filter(grepl(street_num, Address) &
                 grepl(city_state, Address, ignore.case = TRUE))

        if (nrow(firm_matches) > 0) {
          new_match <- data.frame(address = addr, firm_matches, stringsAsFactors = FALSE)
          if (is.null(matched_firms)) {
            matched_firms <- new_match
          } else {
            matched_firms <- rbind(matched_firms, new_match)
          }
        }
      }
    }

    matches$address_matches <- if (is.null(matched_firms)) data.frame() else matched_firms
  }

  return(matches)
}

# Generate comprehensive evidence summary
generate_evidence_summary <- function(evidence, entities, matches) {
  summary <- list(
    extraction_date = Sys.Date(),
    total_pdfs = ifelse(is.null(evidence$pdfs), 0, length(evidence$pdfs)),
    total_excel_files = ifelse(is.null(evidence$excel), 0, length(evidence$excel)),
    entities_found = list(
      total_emails = length(entities$emails),
      total_addresses = length(entities$addresses),
      total_phones = length(entities$phone_numbers),
      total_dates = length(entities$dates),
      kettler_emails = length(matches$kettler_emails),
      address_matches = ifelse(is.null(matches$address_matches), 0, nrow(matches$address_matches))
    ),
    key_findings = list(
      kettler_email_addresses = matches$kettler_emails,
      matched_addresses = if (!is.null(matches$address_matches) && nrow(matches$address_matches) > 0) {
        matches$address_matches
      } else {
        NULL
      }
    )
  )

  return(summary)
}

# Main analysis
main_analysis <- function() {
  cat("=== Analyzing All Evidence ===\n\n")

  cat("Loading evidence...\n")
  evidence <- load_all_evidence()
  cat("  PDFs:", ifelse(is.null(evidence$pdfs), 0, length(evidence$pdfs)), "\n")
  cat("  Excel files:", ifelse(is.null(evidence$excel), 0, length(evidence$excel)), "\n")
  cat("  Firms:", ifelse(is.null(evidence$firms), 0, nrow(evidence$firms)), "\n\n")

  cat("Extracting entities...\n")
  entities <- extract_all_entities(evidence)
  cat("  Emails:", length(entities$emails), "\n")
  cat("  Addresses:", length(entities$addresses), "\n")
  cat("  Phone numbers:", length(entities$phone_numbers), "\n")
  cat("  Dates:", length(entities$dates), "\n\n")

  cat("Cross-referencing with license data...\n")
  matches <- cross_reference_entities(entities, evidence$firms)
  cat("  Kettler emails:", length(matches$kettler_emails), "\n")
  cat("  Address matches:", ifelse(is.null(matches$address_matches), 0, nrow(matches$address_matches)), "\n\n")

  cat("Generating summary...\n")
  summary <- generate_evidence_summary(evidence, entities, matches)

  # Save summary
  summary_file <- file.path(RESEARCH_EVIDENCE_DIR, "all_evidence_summary.json")
  write_json(summary, summary_file, pretty = TRUE)
  cat("Saved summary to:", summary_file, "\n")

  # Save entities
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  write_json(entities, entities_file, pretty = TRUE)
  cat("Saved entities to:", entities_file, "\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
