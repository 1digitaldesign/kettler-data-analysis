#!/usr/bin/env Rscript
# Master Evidence Organization Script
# Organizes all evidence and cross-references with license data for administrative filings

library(dplyr)
library(jsonlite)
library(stringr)

# Load path utilities
source(file.path(dirname(normalizePath(commandArgs()[4])), "load_paths.R"))

# Helper functions
is_valid_df <- function(df) !is.null(df) && is.data.frame(df) && nrow(df) > 0
has_cols <- function(df, cols) is_valid_df(df) && all(cols %in% names(df))
safe_get <- function(x, default = character(0)) if (!is.null(x) && length(x) > 0) x[[1]] else default
safe_extract <- function(entities, field) {
  val <- entities[[field]]
  if (is.list(val) && length(val) > 0) val[[1]] else if (!is.null(val)) val else character(0)
}

# Load all data sources
load_all_data <- function() {
  data <- list()

  # Load Skidmore firm data
  firms_file <- file.path(DATA_SOURCE_DIR, "skidmore_all_firms_complete.csv")
  if (!file.exists(firms_file)) {
    # Try JSON version
    firms_file <- file.path(DATA_SOURCE_DIR, "skidmore_all_firms_complete.json")
  }

  if (file.exists(firms_file)) {
    if (grepl("\\.json$", firms_file)) {
      data$firms <- fromJSON(firms_file)
    } else {
      data$firms <- read.csv(firms_file, stringsAsFactors = FALSE)
    }
  }

  # Load connections and PDF evidence
  for (file_info in list(
    list(path = file.path(DATA_ANALYSIS_DIR, "dpor_skidmore_connections.csv"), key = "connections"),
    list(path = file.path(RESEARCH_EVIDENCE_DIR, "pdf_evidence_extracted.json"), key = "pdf_evidence", json = TRUE)
  )) {
    if (file.exists(file_info$path)) {
      data[[file_info$key]] <- if (isTRUE(file_info$json)) fromJSON(file_info$path) else read.csv(file_info$path, stringsAsFactors = FALSE)
    }
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

      pdf_addresses <- if (!is.null(entities)) safe_extract(entities, "addresses") else character(0)
      pdf_emails <- if (!is.null(entities)) safe_extract(entities, "emails") else character(0)
      pdf_firms <- if (!is.null(entities)) safe_extract(entities, "firms") else character(0)
      reg_info <- if ("regulatory_info" %in% names(pdf_df) && length(pdf_df$regulatory_info) > 0) pdf_df$regulatory_info[[1]] else NULL
    } else {
      pdf_addresses <- pdf_emails <- pdf_firms <- character(0)
      reg_info <- NULL
    }

    # Match PDF addresses with firm addresses
    if (has_cols(data$firms, "Address") && nrow(pdf_df) > 0 && "entities" %in% names(pdf_df) &&
        length(pdf_df$entities) > 0 && !is.null(pdf_df$entities[[1]]) &&
        "addresses" %in% names(pdf_df$entities[[1]]) && length(pdf_df$entities[[1]]$addresses) > 0) {
      pdf_addr <- safe_get(pdf_df$entities[[1]]$addresses[[1]])
      pdf_street_num <- if (!is.null(pdf_addr) && nchar(pdf_addr) > 0) str_extract(pdf_addr, "^\\d+") else NA

      if (!is.na(pdf_street_num)) {
        matched_firms <- data$firms %>%
          filter(grepl(pdf_street_num, Address) & grepl("MCLEAN.*VA|VA.*MCLEAN", Address, ignore.case = TRUE))
        if (nrow(matched_firms) > 0) cross_ref$address_matches <- matched_firms
      }
    }

    # Match emails with Kettler domain
    if (nrow(pdf_df) > 0 && "entities" %in% names(pdf_df) && length(pdf_df$entities) > 0 &&
        !is.null(pdf_df$entities[[1]]) && "emails" %in% names(pdf_df$entities[[1]]) &&
        length(pdf_df$entities[[1]]$emails) > 0) {
      pdf_emails_list <- safe_get(pdf_df$entities[[1]]$emails[[1]])
      kettler_emails <- if (is.character(pdf_emails_list) && length(pdf_emails_list) > 0) {
        pdf_emails_list[grepl("kettler", pdf_emails_list, ignore.case = TRUE)]
      } else character(0)
      if (length(kettler_emails) > 0) cross_ref$kettler_emails <- kettler_emails
    }

    # Extract violation mentions
    if (nrow(pdf_df) > 0 && "regulatory_info" %in% names(pdf_df) && length(pdf_df$regulatory_info) > 0) {
      violations <- safe_get(pdf_df$regulatory_info[[1]]$violation_mentions[[1]], default = numeric(0))
      violations_found <- if (is.numeric(violations) && length(violations) > 0) violations[violations > 0] else numeric(0)
      if (length(violations_found) > 0) {
        cross_ref$violations_mentioned <- length(violations_found)
        cross_ref$violation_details <- violations_found
      }
    }
  }

  return(cross_ref)
}

# Create evidence summary for filings
create_filing_evidence_summary <- function(data, cross_ref) {
  summary <- list()

  # Count findings
  summary$key_findings <- list(
    total_firms_connected = if (is.null(data$firms)) 0 else nrow(data$firms),
    firms_same_address_as_pdf = if (is.null(cross_ref$address_matches) || !is_valid_df(cross_ref$address_matches)) 0 else nrow(cross_ref$address_matches),
    kettler_emails_in_pdf = if (is.null(cross_ref$kettler_emails)) 0 else length(cross_ref$kettler_emails),
    violations_mentioned = if (is.null(cross_ref$violations_mentioned)) 0 else cross_ref$violations_mentioned
  )

  # Address connections
  if (has_cols(data$firms, c("Address", "Firm.Name"))) {
    summary$address_analysis <- data$firms %>%
      group_by(Address) %>%
      summarise(firm_count = n(), firms = paste(Firm.Name, collapse = "; "), .groups = 'drop') %>%
      filter(firm_count > 1) %>%
      arrange(desc(firm_count))
  }

  # Timeline analysis
  if (has_cols(data$firms, c("Firm.Name", "Gap.Years", "Initial.Cert.Date", "Skidmore.License.Date"))) {
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
      kettler_emails <- if (length(entities$emails) > 0) {
        entities$emails[grepl("kettler", entities$emails, ignore.case = TRUE)]
      } else character(0)
      if (length(kettler_emails) > 0) package$key_entities$kettler_emails <- kettler_emails

      # Update summary counts
      package$executive_summary$key_evidence$kettler_emails_in_pdf <- length(kettler_emails)

      # Count violations
      violations <- if (length(pdf_json) > 0 && "regulatory_info" %in% names(pdf_json[[1]]) &&
          !is.null(pdf_json[[1]]$regulatory_info$violation_mentions)) {
        pdf_json[[1]]$regulatory_info$violation_mentions
      } else numeric(0)
      if (is.numeric(violations) && length(violations) > 0) {
        package$executive_summary$key_evidence$violations_mentioned <- sum(violations > 0, na.rm = TRUE)
      }
    }
  }

  # Violations identified
  principal_broker_data <- if (has_cols(data$connections, c("connection_type", "state"))) {
    data$connections %>% filter(connection_type == "Principal Broker") %>% count(state, name = "firm_count")
  } else NULL

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
    if (has_cols(data$firms, "Address")) {
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
    if (nrow(data$pdf_evidence) > 0 && "entities" %in% names(data$pdf_evidence) &&
        length(data$pdf_evidence$entities) > 0 && !is.null(data$pdf_evidence$entities[[1]]) &&
        "emails" %in% names(data$pdf_evidence$entities[[1]]) && length(data$pdf_evidence$entities[[1]]$emails) > 0) {
      emails <- safe_get(data$pdf_evidence$entities[[1]]$emails[[1]])
      kettler <- if (is.character(emails) && length(emails) > 0) emails[grepl("kettler", emails, ignore.case = TRUE)] else character(0)
      if (length(kettler) > 0) {
        cat("  Manual check found", length(kettler), "Kettler emails\n")
        cross_ref$kettler_emails <- kettler
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
