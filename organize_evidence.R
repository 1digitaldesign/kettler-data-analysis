#!/usr/bin/env Rscript
# Master Evidence Organization Script
# Organizes all evidence and cross-references with license data for administrative filings

library(dplyr)
library(jsonlite)
library(stringr)

# Configuration
PROJECT_ROOT <- getwd()
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
FILINGS_DIR <- file.path(PROJECT_ROOT, "filings")
DATA_DIR <- file.path(PROJECT_ROOT, "data")

# Load all data sources
load_all_data <- function() {
  data <- list()

  # Load Skidmore firm data
  # Check for files in new location first, then fallback to root
  source_dir <- file.path(DATA_DIR, "source")
  firms_file <- if (file.exists(file.path(source_dir, "skidmore_all_firms_complete.csv"))) {
    file.path(source_dir, "skidmore_all_firms_complete.csv")
  } else if (file.exists("skidmore_all_firms_complete.csv")) {
    "skidmore_all_firms_complete.csv"
  } else {
    NULL
  }
  if (!is.null(firms_file) && file.exists(firms_file)) {
    data$firms <- read.csv(firms_file, stringsAsFactors = FALSE)
  }

  # Load connections
  connections_file <- file.path(DATA_DIR, "analysis", "dpor_skidmore_connections.csv")
  if (file.exists(connections_file)) {
    data$connections <- read.csv(connections_file, stringsAsFactors = FALSE)
  }

  # Load PDF evidence
  pdf_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (file.exists(pdf_file)) {
    data$pdf_evidence <- fromJSON(pdf_file)
  }

  return(data)
}

# Cross-reference evidence with license data
cross_reference_evidence <- function(data) {
  cross_ref <- list()

  # Extract addresses from PDF
  if (!is.null(data$pdf_evidence) && length(data$pdf_evidence) > 0) {
    # Handle JSON structure - fromJSON creates data.frame with nested lists
    pdf_df <- data$pdf_evidence

    # Extract entities from first row (handle nested list structure from fromJSON)
    if (nrow(pdf_df) > 0 && "entities" %in% names(pdf_df) && length(pdf_df$entities) > 0) {
      entities <- pdf_df$entities[[1]]

      if (!is.null(entities)) {
        # Extract from nested lists (fromJSON creates lists within lists)
        pdf_addresses <- if (!is.null(entities$addresses) && is.list(entities$addresses) && length(entities$addresses) > 0) {
          entities$addresses[[1]]
        } else if (!is.null(entities$addresses)) {
          entities$addresses
        } else {
          character(0)
        }
        pdf_emails <- if (!is.null(entities$emails) && is.list(entities$emails) && length(entities$emails) > 0) {
          entities$emails[[1]]
        } else if (!is.null(entities$emails)) {
          entities$emails
        } else {
          character(0)
        }
        pdf_firms <- if (!is.null(entities$firms) && is.list(entities$firms) && length(entities$firms) > 0) {
          entities$firms[[1]]
        } else if (!is.null(entities$firms)) {
          entities$firms
        } else {
          character(0)
        }
      } else {
        pdf_addresses <- character(0)
        pdf_emails <- character(0)
        pdf_firms <- character(0)
      }

      # Get regulatory info
      if ("regulatory_info" %in% names(pdf_df) && length(pdf_df$regulatory_info) > 0) {
        reg_info <- pdf_df$regulatory_info[[1]]
      } else {
        reg_info <- NULL
      }
    } else {
      pdf_addresses <- character(0)
      pdf_emails <- character(0)
      pdf_firms <- character(0)
      reg_info <- NULL
    }

    # Initialize variables outside conditions
    pdf_addresses <- if (exists("pdf_addresses")) pdf_addresses else character(0)
    pdf_emails <- if (exists("pdf_emails")) pdf_emails else character(0)

    # Match PDF addresses with firm addresses
    # Use direct extraction from data.frame structure
    if (!is.null(data$firms) && nrow(pdf_df) > 0 &&
        "entities" %in% names(pdf_df) && length(pdf_df$entities) > 0 &&
        !is.null(pdf_df$entities[[1]]) &&
        "addresses" %in% names(pdf_df$entities[[1]]) &&
        length(pdf_df$entities[[1]]$addresses) > 0) {
      # Extract address directly from nested structure
      addr_list <- pdf_df$entities[[1]]$addresses[[1]]
      pdf_addr <- if (length(addr_list) > 0) addr_list[1] else NULL

      if (!is.null(pdf_addr) && !is.na(pdf_addr) && nchar(pdf_addr) > 0) {
        # Extract street number
        pdf_street_num <- str_extract(pdf_addr, "^\\d+")

        if (!is.na(pdf_street_num)) {
          matched_firms <- data$firms %>%
            filter(
              grepl(pdf_street_num, Address) &
              grepl("MCLEAN.*VA|VA.*MCLEAN", Address, ignore.case = TRUE)
            )

          if (nrow(matched_firms) > 0) {
            cross_ref$address_matches <- matched_firms
          }
        }
      }
    }

    # Match emails with Kettler domain - extract directly
    if (nrow(pdf_df) > 0 && "entities" %in% names(pdf_df) &&
        length(pdf_df$entities) > 0 && !is.null(pdf_df$entities[[1]]) &&
        "emails" %in% names(pdf_df$entities[[1]]) &&
        length(pdf_df$entities[[1]]$emails) > 0) {
      pdf_emails_list <- pdf_df$entities[[1]]$emails[[1]]
      if (is.character(pdf_emails_list) && length(pdf_emails_list) > 0) {
        kettler_emails <- pdf_emails_list[grepl("kettler", pdf_emails_list, ignore.case = TRUE)]
        if (length(kettler_emails) > 0) {
          cross_ref$kettler_emails <- kettler_emails
        }
      }
    }

    # Extract violation mentions
    if (nrow(pdf_df) > 0 && "regulatory_info" %in% names(pdf_df) &&
        length(pdf_df$regulatory_info) > 0) {
      reg_info <- pdf_df$regulatory_info[[1]]
      if (!is.null(reg_info) && "violation_mentions" %in% names(reg_info) &&
          length(reg_info$violation_mentions) > 0) {
        violations <- reg_info$violation_mentions[[1]]
        if (is.character(violations) && length(violations) > 0) {
          violations_found <- violations[violations > 0]
          if (length(violations_found) > 0) {
            cross_ref$violations_mentioned <- length(violations_found)
            cross_ref$violation_details <- violations_found
          }
        }
      }
    }
  }

  return(cross_ref)
}

# Create evidence summary for filings
create_filing_evidence_summary <- function(data, cross_ref) {
  summary <- list()

  # Count findings (handle both automatic and manual checks)
  firms_matched <- if (is.null(cross_ref$address_matches) || (is.data.frame(cross_ref$address_matches) && nrow(cross_ref$address_matches) == 0)) 0 else nrow(cross_ref$address_matches)
  kettler_count <- if (is.null(cross_ref$kettler_emails)) 0 else length(cross_ref$kettler_emails)
  violations_count <- if (is.null(cross_ref$violations_mentioned)) 0 else cross_ref$violations_mentioned

  summary$key_findings <- list(
    total_firms_connected = ifelse(is.null(data$firms), 0, nrow(data$firms)),
    firms_same_address_as_pdf = firms_matched,
    kettler_emails_in_pdf = kettler_count,
    violations_mentioned = violations_count
  )

  # Address connections
  if (!is.null(data$firms)) {
    summary$address_analysis <- data$firms %>%
      group_by(Address) %>%
      summarise(
        firm_count = n(),
        firms = paste(Firm.Name, collapse = "; "),
        .groups = 'drop'
      ) %>%
      filter(firm_count > 1) %>%
      arrange(desc(firm_count))
  }

  # Timeline analysis
  if (!is.null(data$firms)) {
    summary$timeline_issues <- data$firms %>%
      select(Firm.Name, Initial.Cert.Date, Skidmore.License.Date, Gap.Years) %>%
      filter(Gap.Years > 0) %>%
      arrange(desc(Gap.Years))
  }

  return(summary)
}

# Generate filing-ready evidence package
generate_filing_package <- function(data, cross_ref, summary) {
  package <- list()

  # Executive summary
  package$executive_summary <- list(
    date_prepared = Sys.Date(),
    case_summary = "Investigation into multiple real estate firms listing Caitlin Skidmore as Principal Broker, with evidence of potential license violations and fraudulent practices",
    key_evidence = summary$key_findings,
    recommended_filings = c(
      "Virginia DPOR - License violation complaint",
      "FTC - Consumer fraud complaint",
      "CFPB - Financial services complaint",
      "HUD - Fair housing complaint (if applicable)"
    )
  )

  # Evidence documents
  package$evidence_documents <- list(
    pdf_files = list.files(file.path(EVIDENCE_DIR, "pdfs"), pattern = "\\.pdf$", full.names = FALSE),
    license_data = if (file.exists(file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv"))) {
      file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
    } else {
      "skidmore_all_firms_complete.csv"
    },
    connections_data = file.path(DATA_DIR, "analysis", "dpor_skidmore_connections.csv")
  )

  # Key entities - extract directly from nested structure
  # Re-read JSON to get proper structure
  pdf_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (file.exists(pdf_file)) {
    pdf_json <- fromJSON(pdf_file, simplifyDataFrame = FALSE)
    if (length(pdf_json) > 0 && "entities" %in% names(pdf_json[[1]])) {
      entities <- pdf_json[[1]]$entities

      package$key_entities <- list(
        emails = entities$emails,
        addresses = entities$addresses,
        phone_numbers = entities$phones,
        units_mentioned = entities$units,
        license_numbers = entities$license_numbers
      )

      # Count Kettler emails
      kettler_emails <- character(0)  # Initialize to empty vector
      if (length(entities$emails) > 0) {
        kettler_emails <- entities$emails[grepl("kettler", entities$emails, ignore.case = TRUE)]
        if (length(kettler_emails) > 0) {
          package$key_entities$kettler_emails <- kettler_emails
        }
      }

      # Update summary counts
      package$executive_summary$key_evidence$kettler_emails_in_pdf <- length(kettler_emails)

      # Count violations
      if (length(pdf_json) > 0 && "regulatory_info" %in% names(pdf_json[[1]]) &&
          !is.null(pdf_json[[1]]$regulatory_info) &&
          !is.null(pdf_json[[1]]$regulatory_info$violation_mentions)) {
        violations <- pdf_json[[1]]$regulatory_info$violation_mentions
        if (is.numeric(violations) && length(violations) > 0) {
          violations_count <- sum(violations > 0, na.rm = TRUE)
          package$executive_summary$key_evidence$violations_mentioned <- violations_count
        }
      }
    }
  }

  # Violations identified
  principal_broker_data <- NULL
  if (!is.null(data$connections) && is.data.frame(data$connections) && nrow(data$connections) > 0 &&
      "connection_type" %in% names(data$connections) && "state" %in% names(data$connections)) {
    principal_broker_data <- data$connections %>%
      filter(connection_type == "Principal Broker") %>%
      count(state, name = "firm_count")
  }

  package$violations <- list(
    license_violations = summary$timeline_issues,
    address_clustering = summary$address_analysis,
    principal_broker_pattern = principal_broker_data
  )

  return(package)
}

# Main organization function
main_organize <- function() {
  cat("=== Evidence Organization for Administrative Filings ===\n\n")

  cat("Step 1: Loading all data sources...\n")
  data <- load_all_data()
  cat("  Loaded firm data:", ifelse(is.null(data$firms), 0, nrow(data$firms)), "firms\n")
  cat("  Loaded connections:", ifelse(is.null(data$connections), 0, nrow(data$connections)), "connections\n")
  cat("  Loaded PDF evidence:", ifelse(is.null(data$pdf_evidence), 0, length(data$pdf_evidence)), "file(s)\n\n")

  cat("Step 2: Cross-referencing evidence...\n")
  cross_ref <- cross_reference_evidence(data)
  if (!is.null(cross_ref$address_matches) && nrow(cross_ref$address_matches) > 0) {
    cat("  Found", nrow(cross_ref$address_matches), "firms matching PDF address:\n")
    cat("    -", paste(cross_ref$address_matches$Firm.Name, collapse = ", "), "\n")
  } else {
    cat("  No firms matched PDF address (checking manually...)\n")
    # Manual check
    if (!is.null(data$firms)) {
      kettler_match <- data$firms %>% filter(grepl("8255", Address) & grepl("MCLEAN", Address, ignore.case = TRUE))
      if (nrow(kettler_match) > 0) {
        cat("  Manual check found:", kettler_match$Firm.Name[1], "\n")
        cross_ref$address_matches <- kettler_match
      }
    }
  }
  if (!is.null(cross_ref$kettler_emails) && length(cross_ref$kettler_emails) > 0) {
    cat("  Found", length(cross_ref$kettler_emails), "Kettler email addresses in PDF\n")
  } else {
    # Manual check
    if (!is.null(data$pdf_evidence) && nrow(data$pdf_evidence) > 0 &&
        "entities" %in% names(data$pdf_evidence) &&
        length(data$pdf_evidence$entities) > 0 &&
        !is.null(data$pdf_evidence$entities[[1]]) &&
        "emails" %in% names(data$pdf_evidence$entities[[1]]) &&
        length(data$pdf_evidence$entities[[1]]$emails) > 0) {
      emails <- data$pdf_evidence$entities[[1]]$emails[[1]]
      if (is.character(emails) && length(emails) > 0) {
        kettler <- emails[grepl("kettler", emails, ignore.case = TRUE)]
        if (length(kettler) > 0) {
          cat("  Manual check found", length(kettler), "Kettler emails\n")
          cross_ref$kettler_emails <- kettler
        }
      }
    }
  }
  if (!is.null(cross_ref$violations_mentioned) && cross_ref$violations_mentioned > 0) {
    cat("  Found", cross_ref$violations_mentioned, "violation types mentioned\n")
  }
  cat("\n")

  cat("Step 3: Creating evidence summary...\n")
  summary <- create_filing_evidence_summary(data, cross_ref)
  cat("  Key findings documented\n")
  cat("  Address clusters:", ifelse(is.null(summary$address_analysis), 0, nrow(summary$address_analysis)), "\n")
  cat("  Timeline issues:", ifelse(is.null(summary$timeline_issues), 0, nrow(summary$timeline_issues)), "\n\n")

  cat("Step 4: Generating filing package...\n")
  package <- generate_filing_package(data, cross_ref, summary)

  # Save filing package
  package_file <- file.path(FILINGS_DIR, "filing_evidence_package.json")
  write_json(package, package_file, pretty = TRUE)
  cat("  Saved filing package to:", package_file, "\n")

  # Create executive summary document
  exec_summary_file <- file.path(FILINGS_DIR, "executive_summary.md")
  write_executive_summary(exec_summary_file, package)
  cat("  Saved executive summary to:", exec_summary_file, "\n")

  cat("\n=== Organization Complete ===\n")
  cat("\nKey Evidence Points:\n")
  cat("  -", package$executive_summary$key_evidence$total_firms_connected, "firms connected to Skidmore\n")
  cat("  -", package$executive_summary$key_evidence$firms_same_address_as_pdf, "firms at same address as PDF\n")
  cat("  -", package$executive_summary$key_evidence$violations_mentioned, "violation types mentioned in PDF\n")
}

# Write executive summary markdown
write_executive_summary <- function(filepath, package) {
  content <- paste0(
    "# Executive Summary - Administrative Filing Evidence Package\n\n",
    "**Date Prepared:** ", package$executive_summary$date_prepared, "\n\n",
    "## Case Summary\n\n",
    package$executive_summary$case_summary, "\n\n",
    "## Key Evidence\n\n",
    "- Total Firms Connected: ", package$executive_summary$key_evidence$total_firms_connected, "\n",
    "- Firms at Same Address as PDF Evidence: ", package$executive_summary$key_evidence$firms_same_address_as_pdf, "\n",
    "- Kettler Emails Found in PDF: ", package$executive_summary$key_evidence$kettler_emails_in_pdf, "\n",
    "- Violation Types Mentioned: ", package$executive_summary$key_evidence$violations_mentioned, "\n\n",
    "## Recommended Filings\n\n",
    paste0("- ", package$executive_summary$recommended_filings, collapse = "\n"), "\n\n",
    "## Evidence Documents\n\n",
    "### PDF Files\n",
    paste0("- ", package$evidence_documents$pdf_files, collapse = "\n"), "\n\n",
    "### Data Files\n",
    paste0("- ", package$evidence_documents$license_data, "\n"),
    "- ", package$evidence_documents$connections_data, "\n\n"
  )

  writeLines(content, filepath)
}

# Run if executed as script
if (!interactive()) {
  main_organize()
}
