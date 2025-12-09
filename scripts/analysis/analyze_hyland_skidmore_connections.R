#!/usr/bin/env Rscript
# Analyze connections between Edward Hyland and Skidmore firms
# Email analysis, address matching, corporate connections, timeline analysis

library(jsonlite)
library(dplyr)
library(stringr)

# Configuration
if (file.exists("research/evidence/all_entities_extracted.json")) {
  PROJECT_ROOT <- getwd()
} else if (file.exists("../research/all_entities_extracted.json")) {
  PROJECT_ROOT <- normalizePath("..")
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

DATA_DIR <- file.path(PROJECT_ROOT, "data")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_CONNECTIONS_DIR, "hyland_skidmore_connections.json")

# Load data
load_data <- function() {
  # Load entities
  entities_file <- file.path(RESEARCH_DIR, "all_entities_extracted.json")
  entities <- if (file.exists(entities_file)) {
    fromJSON(entities_file, simplifyDataFrame = FALSE)
  } else {
    list(emails = character(0), addresses = character(0))
  }

  # Load firms
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  firms <- if (file.exists(firms_file)) {
    read.csv(firms_file, stringsAsFactors = FALSE)
  } else {
    data.frame()
  }

  # Load Hyland verification
  hyland_file <- file.path(RESEARCH_DIR, "hyland_verification.json")
  hyland_info <- if (file.exists(hyland_file)) {
    fromJSON(hyland_file, simplifyDataFrame = FALSE)
  } else {
    list()
  }

  return(list(entities = entities, firms = firms, hyland = hyland_info))
}

# Analyze email connections
analyze_email_connections <- function(data) {
  cat("\n=== Analyzing Email Connections ===\n")

  connections <- list()

  # Check if Hyland email appears in firm-related contexts
  hyland_emails <- grep("ehyland@kettler\\.com", data$entities$emails, ignore.case = TRUE, value = TRUE)

  if (length(hyland_emails) > 0) {
    connections$hyland_email_found <- TRUE
    connections$hyland_email_count <- length(hyland_emails)

    # Check for Carlyle emails (connection to 800 Carlyle property)
    carlyle_emails <- grep("carlyle", data$entities$emails, ignore.case = TRUE, value = TRUE)
    if (length(carlyle_emails) > 0) {
      connections$carlyle_emails <- carlyle_emails
      connections$carlyle_connection <- TRUE
    }
  }

  return(connections)
}

# Analyze address connections
analyze_address_connections <- function(data) {
  cat("\n=== Analyzing Address Connections ===\n")

  connections <- list()

  # Hyland's known addresses
  hyland_addresses <- c(
    "8255 Greensboro Drive.*McLean.*VA.*22102",
    "800.*Carlyle|850.*Carlyle",
    "4900.*Seminary.*Alexandria.*VA"
  )

  # Check if any Skidmore firm addresses match Hyland addresses
  if (is.null(data$firms) || !is.data.frame(data$firms) || nrow(data$firms) == 0) {
    return(list(
      matched_addresses = list(),
      connection_found = FALSE
    ))
  }

  firm_addresses <- data$firms$Address
  matched_addresses <- list()

  for (firm_idx in 1:nrow(data$firms)) {
    firm_address <- data$firms$Address[firm_idx]
    firm_name <- data$firms$Firm.Name[firm_idx]

    # Check Kettler address match
    if (grepl("8255.*GREENSBORO", firm_address, ignore.case = TRUE)) {
      matched_addresses[[length(matched_addresses) + 1]] <- list(
        firm = firm_name,
        address = firm_address,
        connection_type = "kettler_headquarters"
      )
    }
  }

  connections$address_matches <- matched_addresses
  connections$match_count <- length(matched_addresses)

  return(connections)
}

# Analyze timeline connections
analyze_timeline_connections <- function(data) {
  cat("\n=== Analyzing Timeline Connections ===\n")

  connections <- list()

  # Hyland employment dates
  hyland_start <- "2022-09-01"  # Sep 2022 from LinkedIn
  hyland_start_date <- as.Date(hyland_start)

  # Skidmore license date
  skidmore_license_date <- as.Date("2025-05-30")

  # Firm license dates
  firms <- data$firms
  if (is.null(firms) || !is.data.frame(firms) || nrow(firms) == 0) {
    return(list(
      firms_before_skidmore = 0,
      firms_after_skidmore = 0,
      timeline_anomaly = FALSE
    ))
  }

  firms$Initial.Cert.Date.Parsed <- NA

  for (i in 1:nrow(firms)) {
    date_str <- firms$Initial.Cert.Date[i]
    if (!is.na(date_str) && date_str != "" && date_str != "DATA MISSING") {
      parsed_date <- tryCatch({
        as.Date(date_str, format = "%Y-%m-%d")
      }, error = function(e) NA)
      if (!is.na(parsed_date)) {
        firms$Initial.Cert.Date.Parsed[i] <- parsed_date
      }
    }
  }

  # Firms licensed after Hyland started at Kettler
  firms_after_hyland <- firms[!is.na(firms$Initial.Cert.Date.Parsed) &
                               firms$Initial.Cert.Date.Parsed > hyland_start_date, ]

  connections$firms_licensed_after_hyland_start <- nrow(firms_after_hyland)
  connections$firm_names_after_hyland <- firms_after_hyland$Firm.Name

  return(connections)
}

# Main analysis function
main_analysis <- function() {
  cat("=== Hyland-Skidmore Connections Analysis ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load data
  data <- load_data()

  # Analyze connections
  email_connections <- analyze_email_connections(data)
  address_connections <- analyze_address_connections(data)
  timeline_connections <- analyze_timeline_connections(data)

  # Combine results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    email_connections = email_connections,
    address_connections = address_connections,
    timeline_connections = timeline_connections,
    summary = list(
      email_connection_found = if (!is.null(email_connections$hyland_email_found)) email_connections$hyland_email_found else FALSE,
      address_matches = address_connections$match_count,
      firms_licensed_after_hyland = timeline_connections$firms_licensed_after_hyland_start
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Analysis Summary ===\n")
  cat("Email Connection:", if (results$summary$email_connection_found) "YES" else "NO", "\n")
  cat("Address Matches:", results$summary$address_matches, "\n")
  cat("Firms Licensed After Hyland Start:", results$summary$firms_licensed_after_hyland, "\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
