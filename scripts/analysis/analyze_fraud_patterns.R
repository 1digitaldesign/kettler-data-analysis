#!/usr/bin/env Rscript
# Analyze Fraud Patterns
# Identifies patterns and connections for administrative filings

library(dplyr)
library(stringr)
library(jsonlite)

# Configuration
DATA_DIR <- "../../data"
RESEARCH_DIR <- "../../research"
FILINGS_DIR <- "../../filings"
EVIDENCE_DIR <- "../../evidence"

# Load all relevant data
load_all_evidence <- function() {
  evidence <- list()

  # Load Skidmore firm data
  # Check for files in new location first, then fallback to root
  source_dir <- file.path(DATA_DIR, "source")
  firms_file <- if (file.exists(file.path(source_dir, "skidmore_all_firms_complete.csv"))) {
    file.path(source_dir, "skidmore_all_firms_complete.csv")
  } else if (file.exists("../../skidmore_all_firms_complete.csv")) {
    "../../skidmore_all_firms_complete.csv"
  } else {
    NULL
  }
  if (!is.null(firms_file) && file.exists(firms_file)) {
    evidence$firms <- read.csv(firms_file, stringsAsFactors = FALSE)
  }

  # Load DPOR connections
  connections_file <- file.path(DATA_DIR, "analysis", "dpor_skidmore_connections.csv")
  if (file.exists(connections_file)) {
    evidence$connections <- read.csv(connections_file, stringsAsFactors = FALSE)
  }

  # Load extracted PDF evidence
  pdf_evidence_file <- file.path(RESEARCH_EVIDENCE_DIR, "pdf_evidence_extracted.json")
  if (file.exists(pdf_evidence_file)) {
    evidence$pdf_data <- fromJSON(pdf_evidence_file)
  }

  return(evidence)
}

# Identify fraud indicators
identify_fraud_indicators <- function(evidence) {
  indicators <- list()

  # License-related fraud indicators
  if (!is.null(evidence$firms)) {
    # Check for license gaps
    indicators$license_gaps <- evidence$firms %>%
      filter(Gap.Years > 0) %>%
      select(Firm.Name, License.Number, Gap.Years, Notes)

    # Check for same address patterns (potential shell companies)
    address_counts <- evidence$firms %>%
      group_by(Address) %>%
      summarise(firm_count = n(), .groups = 'drop') %>%
      filter(firm_count > 1) %>%
      arrange(desc(firm_count))

    indicators$address_clusters <- address_counts
  }

  # Connection patterns
  if (!is.null(evidence$connections)) {
    # Multiple firms with same principal broker
    indicators$principal_broker_pattern <- evidence$connections %>%
      filter(connection_type == "Principal Broker") %>%
      group_by(state) %>%
      summarise(firm_count = n_distinct(firm_name), .groups = 'drop') %>%
      arrange(desc(firm_count))
  }

  # Timeline analysis
  if (!is.null(evidence$firms)) {
    # Firms licensed after Skidmore (potential backdating)
    indicators$timeline_issues <- evidence$firms %>%
      filter(!is.na(Initial.Cert.Date) & Initial.Cert.Date != "") %>%
      mutate(
        cert_date = as.Date(Initial.Cert.Date),
        skidmore_date = as.Date("2025-05-30"),
        licensed_after = cert_date > skidmore_date
      ) %>%
      filter(licensed_after) %>%
      select(Firm.Name, Initial.Cert.Date, Skidmore.License.Date)
  }

  return(indicators)
}

# Generate filing recommendations
generate_filing_recommendations <- function(indicators, evidence) {
  recommendations <- list()

  # Federal filings
  recommendations$federal <- list()

  if (nrow(indicators$license_gaps) > 0) {
    recommendations$federal$ftc <- list(
      reason = "Multiple firms with significant license gaps and same principal broker",
      evidence_count = nrow(indicators$license_gaps),
      priority = "High"
    )
  }

  if (!is.null(indicators$address_clusters) && nrow(indicators$address_clusters) > 0) {
    recommendations$federal$cfpb <- list(
      reason = "Address clustering suggests potential shell company scheme",
      evidence_count = nrow(indicators$address_clusters),
      priority = "High"
    )
  }

  # State filings
  recommendations$state <- list()

  if (!is.null(indicators$principal_broker_pattern) &&
      is.data.frame(indicators$principal_broker_pattern) &&
      nrow(indicators$principal_broker_pattern) > 0) {
    for (i in 1:nrow(indicators$principal_broker_pattern)) {
      state <- indicators$principal_broker_pattern$state[i]
      firm_count <- indicators$principal_broker_pattern$firm_count[i]

      recommendations$state[[state]] <- list(
        reason = paste("Multiple firms (", firm_count, ") listing same principal broker"),
        evidence_count = firm_count,
        priority = "High",
        filing_type = "License violation complaint"
      )
    }
  }

  # Local filings
  recommendations$local <- list(
    consumer_protection = list(
      reason = "Potential consumer fraud and deceptive business practices",
      priority = "Medium"
    )
  )

  return(recommendations)
}

# Create filing checklist
create_filing_checklist <- function(recommendations, evidence) {
  checklist <- data.frame(
    agency = character(),
    filing_type = character(),
    priority = character(),
    evidence_available = character(),
    status = character(),
    notes = character(),
    stringsAsFactors = FALSE
  )

  # Add federal filings
  if (length(recommendations$federal) > 0) {
    for (agency in names(recommendations$federal)) {
      rec <- recommendations$federal[[agency]]
      checklist <- rbind(checklist, data.frame(
        agency = toupper(agency),
        filing_type = "Federal complaint",
        priority = rec$priority,
        evidence_available = ifelse(is.null(rec$evidence_count), "Yes", paste(rec$evidence_count, "items")),
        status = "Pending",
        notes = rec$reason,
        stringsAsFactors = FALSE
      ))
    }
  }

  # Add state filings
  if (length(recommendations$state) > 0) {
    for (state in names(recommendations$state)) {
      rec <- recommendations$state[[state]]
      checklist <- rbind(checklist, data.frame(
        agency = paste("State:", state),
        filing_type = rec$filing_type,
        priority = rec$priority,
        evidence_available = paste(rec$evidence_count, "firms"),
        status = "Pending",
        notes = rec$reason,
        stringsAsFactors = FALSE
      ))
    }
  }

  return(checklist)
}

# Main analysis
main_analysis <- function() {
  cat("Loading evidence...\n")
  evidence <- load_all_evidence()

  cat("Identifying fraud indicators...\n")
  indicators <- identify_fraud_indicators(evidence)

  cat("Generating filing recommendations...\n")
  recommendations <- generate_filing_recommendations(indicators, evidence)

  cat("Creating filing checklist...\n")
  checklist <- create_filing_checklist(recommendations, evidence)

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  dir.create(FILINGS_DIR, showWarnings = FALSE, recursive = TRUE)

  indicators_file <- file.path(RESEARCH_ANOMALIES_DIR, "fraud_indicators.json")
  write_json(indicators, indicators_file, pretty = TRUE)
  cat("Saved fraud indicators to:", indicators_file, "\n")

  recommendations_file <- file.path(RESEARCH_SUMMARIES_DIR, "filing_recommendations.json")
  write_json(recommendations, recommendations_file, pretty = TRUE)
  cat("Saved filing recommendations to:", recommendations_file, "\n")

  checklist_file <- file.path(FILINGS_DIR, "filing_checklist.csv")
  write.csv(checklist, checklist_file, row.names = FALSE)
  cat("Saved filing checklist to:", checklist_file, "\n")

  # Print summary
  cat("\n=== Fraud Pattern Analysis Summary ===\n")
  cat("License Gaps Found:", ifelse(is.null(indicators$license_gaps), 0, nrow(indicators$license_gaps)), "\n")
  cat("Address Clusters Found:", ifelse(is.null(indicators$address_clusters), 0, nrow(indicators$address_clusters)), "\n")
  cat("Federal Filings Recommended:", length(recommendations$federal), "\n")
  cat("State Filings Recommended:", length(recommendations$state), "\n")
  cat("\nFiling Checklist:\n")
  print(checklist)
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
