#!/usr/bin/env Rscript
# Analyze Skidmore Connections
# Identifies connections between firms and Caitlin Skidmore from DPOR data

library(dplyr)
library(stringr)
if (!require(data.table, quietly = TRUE)) {
  cat("Warning: data.table not available, using base R alternatives\n")
}
library(jsonlite)

# Configuration
DATA_DIR <- "data"
CLEANED_DIR <- file.path(DATA_DIR, "cleaned")
ANALYSIS_DIR <- file.path(DATA_DIR, "analysis")
dir.create(ANALYSIS_DIR, showWarnings = FALSE, recursive = TRUE)

# Load existing Skidmore data
load_skidmore_data <- function() {
  # Check for files in new location first, then fallback to root
  source_dir <- file.path(DATA_DIR, "source")
  firms_file <- if (file.exists(file.path(source_dir, "skidmore_all_firms_complete.csv"))) {
    file.path(source_dir, "skidmore_all_firms_complete.csv")
  } else if (file.exists("skidmore_all_firms_complete.csv")) {
    "skidmore_all_firms_complete.csv"
  } else {
    stop("Cannot find skidmore_all_firms_complete.csv in data/source/ or root directory")
  }

  firms_db_file <- if (file.exists(file.path(source_dir, "skidmore_firms_database.csv"))) {
    file.path(source_dir, "skidmore_firms_database.csv")
  } else if (file.exists("skidmore_firms_database.csv")) {
    "skidmore_firms_database.csv"
  } else {
    stop("Cannot find skidmore_firms_database.csv in data/source/ or root directory")
  }

  licenses_file <- if (file.exists(file.path(source_dir, "skidmore_individual_licenses.csv"))) {
    file.path(source_dir, "skidmore_individual_licenses.csv")
  } else if (file.exists("skidmore_individual_licenses.csv")) {
    "skidmore_individual_licenses.csv"
  } else {
    stop("Cannot find skidmore_individual_licenses.csv in data/source/ or root directory")
  }

  firms_complete <- read.csv(firms_file, stringsAsFactors = FALSE)
  firms_db <- read.csv(firms_db_file, stringsAsFactors = FALSE)
  individual_licenses <- read.csv(licenses_file, stringsAsFactors = FALSE)

  return(list(
    firms_complete = firms_complete,
    firms_db = firms_db,
    individual_licenses = individual_licenses
  ))
}

# Load cleaned DPOR search results
load_dpor_results <- function() {
  cleaned_file <- file.path(CLEANED_DIR, "dpor_all_cleaned.csv")

  if (file.exists(cleaned_file)) {
    return(read.csv(cleaned_file, stringsAsFactors = FALSE))
  }

  # Fallback to raw files
  raw_files <- list.files(file.path(DATA_DIR, "raw"), pattern = "*.csv", full.names = TRUE)

  if (length(raw_files) > 0) {
    all_results <- list()
    for (file in raw_files) {
      df <- read.csv(file, stringsAsFactors = FALSE)
      all_results[[length(all_results) + 1]] <- df
    }
    return(bind_rows(all_results))
  }

  return(data.frame())
}

# Normalize names for matching
normalize_name <- function(name) {
  if (is.na(name) || name == "") return("")

  name <- toupper(name)
  name <- str_remove_all(name, "[[:punct:]]")
  name <- str_replace_all(name, "\\s+", " ")
  name <- str_trim(name)

  return(name)
}

# Find firms connected to Skidmore
find_skidmore_connections <- function(dpor_results, skidmore_data) {
  connections <- data.frame(
    firm_name = character(),
    license_number = character(),
    state = character(),
    connection_type = character(),
    connection_detail = character(),
    skidmore_license = character(),
    stringsAsFactors = FALSE
  )

  # Extract Skidmore name variations
  skidmore_names <- c(
    "SKIDMORE",
    "CAITLIN SKIDMORE",
    "CAITLIN MARIE SKIDMORE",
    "SKIDMORE CAITLIN",
    "SKIDMORE CAITLIN MARIE"
  )

  skidmore_normalized <- sapply(skidmore_names, normalize_name)

  # Extract Skidmore addresses from individual licenses
  if (!is.null(skidmore_data$individual_licenses) &&
      "address" %in% names(skidmore_data$individual_licenses)) {
    skidmore_addresses <- unique(skidmore_data$individual_licenses$address)
    skidmore_addresses <- skidmore_addresses[!is.na(skidmore_addresses) & skidmore_addresses != ""]
  } else {
    skidmore_addresses <- character(0)
  }

  # Extract known firm addresses from Skidmore data
  if (!is.null(skidmore_data$firms_complete) &&
      "Address" %in% names(skidmore_data$firms_complete)) {
    known_firm_addresses <- unique(skidmore_data$firms_complete$Address)
    known_firm_addresses <- known_firm_addresses[!is.na(known_firm_addresses) & known_firm_addresses != ""]
  } else {
    known_firm_addresses <- character(0)
  }

  if (nrow(dpor_results) == 0) {
    return(connections)
  }

  # Check each DPOR result
  for (i in 1:nrow(dpor_results)) {
    row <- dpor_results[i, ]

    firm_name <- if ("name" %in% names(row)) row$name else ""
    firm_name_cleaned <- if ("name_cleaned" %in% names(row)) row$name_cleaned else firm_name
    license_number <- if ("license_number" %in% names(row)) row$license_number else ""
    address <- if ("address" %in% names(row)) row$address else ""
    address_norm <- if ("address_normalized" %in% names(row)) row$address_normalized else address
    principal_broker <- if ("principal_broker" %in% names(row)) row$principal_broker else ""
    state <- if ("state" %in% names(row)) row$state else ""

    connection_found <- FALSE
    connection_type <- ""
    connection_detail <- ""
    skidmore_license <- ""

    # Check 1: Principal broker is Skidmore
    if (principal_broker != "") {
      principal_normalized <- normalize_name(principal_broker)
      for (skidmore_norm in skidmore_normalized) {
        if (grepl(skidmore_norm, principal_normalized, ignore.case = TRUE)) {
          connection_found <- TRUE
          connection_type <- "Principal Broker"
          connection_detail <- paste("Listed as Principal Broker:", principal_broker)
          break
        }
      }
    }

    # Check 2: Same address as Skidmore licenses
    if (!connection_found && address_norm != "") {
      address_normalized <- normalize_name(address_norm)
      for (skidmore_addr in skidmore_addresses) {
        skidmore_addr_norm <- normalize_name(skidmore_addr)
        if (address_normalized == skidmore_addr_norm ||
            grepl(skidmore_addr_norm, address_normalized, ignore.case = TRUE)) {
          connection_found <- TRUE
          connection_type <- "Same Address"
          connection_detail <- paste("Same address as Skidmore license:", skidmore_addr)
          break
        }
      }
    }

    # Check 3: Same address as known firms
    if (!connection_found && address_norm != "") {
      address_normalized <- normalize_name(address_norm)
      for (firm_addr in known_firm_addresses) {
        firm_addr_norm <- normalize_name(firm_addr)
        if (address_normalized == firm_addr_norm ||
            grepl(firm_addr_norm, address_normalized, ignore.case = TRUE)) {
          connection_found <- TRUE
          connection_type <- "Same Address as Known Firm"
          connection_detail <- paste("Same address as known firm:", firm_addr)
          break
        }
      }
    }

    # Check 4: Firm name matches known firms
    if (!connection_found && firm_name_cleaned != "") {
      firm_normalized <- normalize_name(firm_name_cleaned)
      if (!is.null(skidmore_data$firms_complete) &&
          "Firm.Name" %in% names(skidmore_data$firms_complete)) {
        known_firms <- unique(skidmore_data$firms_complete$Firm.Name)
      } else {
        known_firms <- character(0)
      }
      for (known_firm in known_firms) {
        known_firm_norm <- normalize_name(known_firm)
        if (firm_normalized == known_firm_norm ||
            grepl(known_firm_norm, firm_normalized, ignore.case = TRUE)) {
          connection_found <- TRUE
          connection_type <- "Known Firm Match"
          connection_detail <- paste("Matches known firm:", known_firm)
          break
        }
      }
    }

    if (connection_found) {
      connections <- rbind(connections, data.frame(
        firm_name = firm_name_cleaned,
        license_number = license_number,
        state = state,
        connection_type = connection_type,
        connection_detail = connection_detail,
        skidmore_license = skidmore_license,
        stringsAsFactors = FALSE
      ))
    }
  }

  return(connections)
}

# Generate connection network analysis
generate_network_analysis <- function(connections, skidmore_data) {
  network <- list()

  # Count connections by type
  network$connections_by_type <- connections %>%
    group_by(connection_type) %>%
    summarise(count = n(), .groups = 'drop')

  # Count connections by state
  network$connections_by_state <- connections %>%
    group_by(state) %>%
    summarise(count = n(), .groups = 'drop')

  # Unique firms connected
  network$unique_firms <- connections %>%
    distinct(firm_name) %>%
    nrow()

  # Address clusters
  if ("address" %in% names(connections)) {
    network$address_clusters <- connections %>%
      group_by(address) %>%
      summarise(firm_count = n_distinct(firm_name), .groups = 'drop') %>%
      arrange(desc(firm_count))
  }

  return(network)
}

# Create summary statistics
create_summary_stats <- function(connections, dpor_results, skidmore_data) {
  stats <- list()

  stats$total_dpor_results <- nrow(dpor_results)
  stats$total_connections <- nrow(connections)

  if (nrow(connections) > 0 && "firm_name" %in% names(connections)) {
    stats$unique_connected_firms <- length(unique(connections$firm_name))
  } else {
    stats$unique_connected_firms <- 0
  }

  if (nrow(connections) > 0 && "state" %in% names(connections)) {
    stats$states_with_connections <- length(unique(connections$state))
  } else {
    stats$states_with_connections <- 0
  }

  # Connection types breakdown
  if (nrow(connections) > 0 && "connection_type" %in% names(connections)) {
    stats$connection_types <- connections %>%
      group_by(connection_type) %>%
      summarise(count = n(), .groups = 'drop') %>%
      arrange(desc(count))
  } else {
    stats$connection_types <- data.frame(connection_type = character(0), count = integer(0))
  }

  # States breakdown
  if (nrow(connections) > 0 && "state" %in% names(connections)) {
    stats$states <- connections %>%
      group_by(state) %>%
      summarise(count = n(), .groups = 'drop') %>%
      arrange(desc(count))
  } else {
    stats$states <- data.frame(state = character(0), count = integer(0))
  }

  # Known firms from original data
  if (!is.null(skidmore_data$firms_complete) && nrow(skidmore_data$firms_complete) > 0 &&
      "Firm.Name" %in% names(skidmore_data$firms_complete)) {
    stats$known_firms_count <- nrow(skidmore_data$firms_complete)
    stats$known_firms <- skidmore_data$firms_complete$Firm.Name
  } else {
    stats$known_firms_count <- 0
    stats$known_firms <- character(0)
  }

  return(stats)
}

# Main analysis function
main_analysis <- function() {
  cat("Loading data...\n")

  # Load existing Skidmore data
  skidmore_data <- load_skidmore_data()
  firms_count <- if (!is.null(skidmore_data$firms_complete)) nrow(skidmore_data$firms_complete) else 0
  licenses_count <- if (!is.null(skidmore_data$individual_licenses)) nrow(skidmore_data$individual_licenses) else 0
  cat("Loaded", firms_count, "known firms\n")
  cat("Loaded", licenses_count, "Skidmore individual licenses\n")

  # Load DPOR search results
  dpor_results <- load_dpor_results()
  cat("Loaded", nrow(dpor_results), "DPOR search results\n")

  if (nrow(dpor_results) == 0) {
    cat("No DPOR results found. Run search scripts first.\n")
    return()
  }

  # Find connections
  cat("\nAnalyzing connections...\n")
  connections <- find_skidmore_connections(dpor_results, skidmore_data)
  cat("Found", nrow(connections), "connections\n")

  # Save connections
  connections_file <- file.path(ANALYSIS_DIR, "dpor_skidmore_connections.csv")
  write.csv(connections, connections_file, row.names = FALSE)
  cat("Saved connections to:", connections_file, "\n")

  # Generate network analysis
  cat("\nGenerating network analysis...\n")
  network <- generate_network_analysis(connections, skidmore_data)

  # Create summary statistics
  stats <- create_summary_stats(connections, dpor_results, skidmore_data)

  # Save summary
  summary_file <- file.path(ANALYSIS_DIR, "analysis_summary.json")
  summary_json <- list(
    statistics = stats,
    network = network,
    timestamp = Sys.time()
  )
  write_json(summary_json, summary_file, pretty = TRUE)
  cat("Saved summary to:", summary_file, "\n")

  # Print summary
  cat("\n=== Analysis Summary ===\n")
  cat("Total DPOR Results:", stats$total_dpor_results, "\n")
  cat("Total Connections Found:", stats$total_connections, "\n")
  cat("Unique Connected Firms:", stats$unique_connected_firms, "\n")
  cat("States with Connections:", stats$states_with_connections, "\n")

  cat("\nConnection Types:\n")
  print(stats$connection_types)

  cat("\nTop States:\n")
  print(head(stats$states, 10))

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
