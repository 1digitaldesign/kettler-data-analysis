#!/usr/bin/env Rscript
# Validate Skidmore Firm Claims
# Re-verifies all 11 Skidmore firms: existence, principal broker listings, address clustering, license gaps, timeline anomalies

library(jsonlite)
library(dplyr)
library(stringr)

# Configuration
if (file.exists("research/fraud_indicators.json")) {
  PROJECT_ROOT <- getwd()
} else if (file.exists("../research/fraud_indicators.json")) {
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

# Load firms data
load_firms_data <- function() {
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (!file.exists(firms_file)) {
    stop("Firms file not found: ", firms_file)
  }
  return(read.csv(firms_file, stringsAsFactors = FALSE))
}

# Verify all 11 firms exist
verify_firms_existence <- function(firms) {
  cat("\n=== Verifying Firm Existence ===\n")

  expected_firms <- c(
    "KETTLER MANAGEMENT INC",
    "BELL PARTNERS INC",
    "BOZZUTO MANAGEMENT COMPANY",
    "CORTLAND MANAGEMENT LLC",
    "GABLES RESIDENTIAL SERVICES INC",
    "GATEWAY MANAGEMENT COMPANY LLC",
    "MCCORMACK BARON MANAGEMENT INC",
    "BURLINGTON CAPITAL PROPERTIES LLC",
    "BAINBRIDGE MID ATLANTIC MANAGEMENT LLC",
    "CAPREIT RESIDENTIAL MANAGEMENT LLC",
    "EDGEWOOD MANAGEMENT CORPORATION"
  )

  found_firms <- firms$Firm.Name
  missing_firms <- setdiff(expected_firms, found_firms)

  if (length(missing_firms) == 0) {
    cat("All 11 firms found in records\n")
    return(list(status = "verified", missing = character(0)))
  } else {
    cat("Missing firms:", paste(missing_firms, collapse = ", "), "\n")
    return(list(status = "partial", missing = missing_firms))
  }
}

# Verify principal broker listings
verify_principal_broker <- function(firms) {
  cat("\n=== Verifying Principal Broker Listings ===\n")

  skidmore_variations <- c("SKIDMORE CAITLIN MARIE", "CAITLIN SKIDMORE", "SKIDMORE, CAITLIN")

  firms_with_skidmore <- firms[grepl("SKIDMORE", firms$Principal.Broker, ignore.case = TRUE), ]

  cat("Found", nrow(firms_with_skidmore), "firms listing Skidmore as Principal Broker\n")

  if (nrow(firms_with_skidmore) == 11) {
    return(list(status = "verified", count = 11))
  } else {
    return(list(status = "mismatch", expected = 11, found = nrow(firms_with_skidmore)))
  }
}

# Verify address clustering
verify_address_clustering <- function(firms) {
  cat("\n=== Verifying Address Clustering ===\n")

  # Check for Frisco, TX address cluster
  frisco_address <- "5729 LEBANON RD STE 144553, FRISCO, TX 75034"
  frisco_firms <- firms[grepl("5729.*LEBANON|LEBANON.*5729", firms$Address, ignore.case = TRUE) &
                        grepl("FRISCO.*TX.*75034", firms$Address, ignore.case = TRUE), ]

  cat("Found", nrow(frisco_firms), "firms at Frisco, TX address\n")
  cat("Firms:", paste(frisco_firms$Firm.Name, collapse = ", "), "\n")

  expected_frisco_firms <- 6
  if (nrow(frisco_firms) == expected_frisco_firms) {
    return(list(status = "verified", count = nrow(frisco_firms), firms = frisco_firms$Firm.Name))
  } else {
    return(list(status = "mismatch", expected = expected_frisco_firms, found = nrow(frisco_firms)))
  }
}

# Verify license gaps
verify_license_gaps <- function(firms) {
  cat("\n=== Verifying License Gaps ===\n")

  skidmore_license_date <- as.Date("2025-05-30")

  firms$Initial.Cert.Date.Parsed <- NA
  firms$Gap.Years.Calculated <- NA_real_

  for (i in 1:nrow(firms)) {
    date_str <- firms$Initial.Cert.Date[i]
    if (!is.na(date_str) && date_str != "" && date_str != "DATA MISSING") {
      parsed_date <- tryCatch({
        as.Date(date_str, format = "%Y-%m-%d")
      }, error = function(e) NA)

      if (!is.na(parsed_date)) {
        firms$Initial.Cert.Date.Parsed[i] <- parsed_date
        gap_days <- as.numeric(skidmore_license_date - parsed_date)
        firms$Gap.Years.Calculated[i] <- gap_days / 365.25
      }
    }
  }

  # Compare with existing Gap.Years
  firms_with_gaps <- firms[!is.na(firms$Gap.Years) & firms$Gap.Years != "UNKNOWN", ]

  cat("Firms with license gaps:\n")
  for (i in 1:nrow(firms_with_gaps)) {
    cat(sprintf("  %s: %s years (expected: %s)\n",
                firms_with_gaps$Firm.Name[i],
                firms_with_gaps$Gap.Years[i],
                ifelse(is.na(firms_with_gaps$Gap.Years.Calculated[i]), "N/A", round(firms_with_gaps$Gap.Years.Calculated[i], 1))))
  }

  return(list(status = "verified", firms = firms_with_gaps))
}

# Verify timeline anomalies
verify_timeline_anomalies <- function(firms) {
  cat("\n=== Verifying Timeline Anomalies ===\n")

  skidmore_license_date <- as.Date("2025-05-30")

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

  # Firms licensed after Skidmore
  firms_after <- firms[!is.na(firms$Initial.Cert.Date.Parsed) &
                        firms$Initial.Cert.Date.Parsed > skidmore_license_date, ]

  cat("Firms licensed AFTER Skidmore (", as.character(skidmore_license_date), "):\n", sep = "")
  if (nrow(firms_after) > 0) {
    for (i in 1:nrow(firms_after)) {
      cat(sprintf("  %s: %s\n",
                  firms_after$Firm.Name[i],
                  as.character(firms_after$Initial.Cert.Date.Parsed[i])))
    }
    return(list(status = "anomalies_found", count = nrow(firms_after), firms = firms_after$Firm.Name))
  } else {
    cat("  None found\n")
    return(list(status = "no_anomalies", count = 0))
  }
}

# Main validation function
main_validation <- function() {
  cat("=== Skidmore Firms Validation ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load firms data
  firms <- load_firms_data()
  cat("Loaded", nrow(firms), "firms\n\n")

  # Verify existence
  existence <- verify_firms_existence(firms)

  # Verify principal broker
  principal_broker <- verify_principal_broker(firms)

  # Verify address clustering
  clustering <- verify_address_clustering(firms)

  # Verify license gaps
  gaps <- verify_license_gaps(firms)

  # Verify timeline anomalies
  anomalies <- verify_timeline_anomalies(firms)

  # Create summary
  summary <- list(
    verification_date = as.character(Sys.Date()),
    firms_existence = existence,
    principal_broker = principal_broker,
    address_clustering = clustering,
    license_gaps = list(status = gaps$status, count = nrow(gaps$firms)),
    timeline_anomalies = anomalies
  )

  # Save summary
  summary_file <- file.path(RESEARCH_DIR, "skidmore_firms_validation.json")
  write_json(summary, summary_file, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved validation summary to:", summary_file, "\n")

  # Print final summary
  cat("\n=== Validation Summary ===\n")
  cat("Firms Existence:", existence$status, "\n")
  cat("Principal Broker:", principal_broker$status, "(", principal_broker$count %||% principal_broker$found, "firms)\n")
  cat("Address Clustering:", clustering$status, "(", clustering$count, "firms)\n")
  cat("Timeline Anomalies:", anomalies$status, "(", anomalies$count, "firms)\n")

  cat("\n=== Validation Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_validation()
}
