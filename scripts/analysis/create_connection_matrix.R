#!/usr/bin/env Rscript
# Create comprehensive connection matrix
# Documents Hyland-Firm, Firm-Firm, Kettler-Firm, and Violation-Entity connections

library(jsonlite)
library(dplyr)

# Configuration
if (file.exists("research/evidence/all_entities_extracted.json")) {
  PROJECT_ROOT <- getwd()
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
DATA_DIR <- file.path(PROJECT_ROOT, "data")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "connection_matrix.json")

# Load all data
load_all_data <- function() {
  # Firms
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  firms <- if (file.exists(firms_file)) {
    read.csv(firms_file, stringsAsFactors = FALSE)
  } else {
    data.frame()
  }

  # Hyland connections
  hyland_file <- file.path(RESEARCH_DIR, "hyland_skidmore_connections.json")
  hyland_conn <- if (file.exists(hyland_file)) {
    fromJSON(hyland_file, simplifyDataFrame = FALSE)
  } else {
    list()
  }

  # Shared resources
  shared_file <- file.path(RESEARCH_DIR, "shared_resources_analysis.json")
  shared <- if (file.exists(shared_file)) {
    fromJSON(shared_file, simplifyDataFrame = FALSE)
  } else {
    list()
  }

  return(list(firms = firms, hyland = hyland_conn, shared = shared))
}

# Create connection matrix
create_matrix <- function(data) {
  cat("=== Creating Connection Matrix ===\n")

  matrix <- list(
    creation_date = as.character(Sys.Date()),
    hyland_firm_connections = list(),
    firm_firm_connections = list(),
    kettler_firm_connections = list(),
    violation_entity_connections = list()
  )

  # Hyland-Firm connections
  if (length(data$hyland) > 0) {
    matrix$hyland_firm_connections <- list(
      email_connection = ifelse(is.null(data$hyland$email_connections$hyland_email_found), FALSE, data$hyland$email_connections$hyland_email_found),
      address_match = ifelse(is.null(data$hyland$address_connections$match_count), 0, data$hyland$address_connections$match_count),
      timeline_connection = ifelse(is.null(data$hyland$timeline_connections$firms_licensed_after_hyland_start), 0, data$hyland$timeline_connections$firms_licensed_after_hyland_start)
    )
  }

  # Firm-Firm connections (shared addresses)
  if (length(data$shared$shared_addresses) > 0) {
    matrix$firm_firm_connections <- list(
      shared_addresses = data$shared$shared_addresses,
      cluster_count = data$shared$shared_address_count
    )
  }

  # Kettler-Firm connections
  firms <- data$firms
  kettler_firm <- firms[firms$Firm.Name == "KETTLER MANAGEMENT INC", ]
  if (nrow(kettler_firm) > 0) {
    safe_col <- function(col) if (col %in% names(kettler_firm) && nrow(kettler_firm) > 0) kettler_firm[[col]][1] else NA
    matrix$kettler_firm_connections <- list(
      kettler_license_number = safe_col("License.Number"),
      kettler_address = safe_col("Address"),
      principal_broker = safe_col("Principal.Broker"),
      connection_type = "direct_license_match"
    )
  }

  # Summary
  matrix$summary <- list(
    total_firms = nrow(firms),
    hyland_connections = length(matrix$hyland_firm_connections),
    firm_firm_clusters = ifelse(is.null(matrix$firm_firm_connections$cluster_count), 0, matrix$firm_firm_connections$cluster_count),
    kettler_connected = nrow(kettler_firm) > 0
  )

  return(matrix)
}

# Main function
main <- function() {
  cat("=== Connection Matrix Creation ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load data
  data <- load_all_data()

  # Create matrix
  matrix <- create_matrix(data)

  # Save
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(matrix, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved connection matrix to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Matrix Summary ===\n")
  cat("Total Firms:", matrix$summary$total_firms, "\n")
  cat("Hyland Connections:", matrix$summary$hyland_connections, "\n")
  cat("Firm-Firm Clusters:", matrix$summary$firm_firm_clusters, "\n")
  cat("Kettler Connected:", matrix$summary$kettler_connected, "\n")

  cat("\n=== Complete ===\n")
}

if (!interactive()) {
  main()
}
