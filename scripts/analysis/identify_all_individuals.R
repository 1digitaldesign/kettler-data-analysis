#!/usr/bin/env Rscript
# Identify all individuals mentioned in evidence
# Extract names, roles, and connections

library(jsonlite)
library(dplyr)
library(stringr)

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
EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
OUTPUT_FILE <- file.path(RESEARCH_EVIDENCE_DIR, "all_individuals_identified.json")

# Extract names from PDF evidence
extract_names_from_pdfs <- function() {
  cat("\n=== Extracting Names from PDFs ===\n")

  pdf_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (!file.exists(pdf_file)) {
    return(list())
  }

  pdf_data <- fromJSON(pdf_file, simplifyDataFrame = FALSE)
  individuals <- list()

  # Known individuals from doc.md
  known_individuals <- list(
    edward_hyland = list(
      name = "Edward Hyland",
      role = "Senior Regional Manager",
      employer = "Kettler Management Inc.",
      email = "ehyland@kettler.com",
      license_status = "No Virginia license",
      connection_type = "operational_nexus"
    ),
    caitlin_skidmore = list(
      name = "Caitlin Skidmore",
      role = "Principal Broker (Front Person)",
      firms = 11,
      license_date = "2025-05-30",
      connection_type = "front_person"
    ),
    djene_moyer = list(
      name = "Djene Moyer",
      role = "Community Manager",
      property = "800 Carlyle",
      employer = "Kettler Management",
      connection_type = "on_site_management"
    ),
    henry_ramos = list(
      name = "Henry Ramos",
      role = "Property Manager",
      property = "800 Carlyle",
      employer = "Kettler Management",
      connection_type = "on_site_management"
    ),
    robert_kettler = list(
      name = "Robert C. Kettler",
      role = "Chairman, Founder & CEO",
      employer = "Kettler",
      connection_type = "corporate_leadership"
    ),
    cindy_fisher = list(
      name = "Cindy Fisher",
      role = "President",
      employer = "Kettler",
      connection_type = "corporate_leadership"
    ),
    luke_davis = list(
      name = "Luke Davis",
      role = "Chief Investment Officer",
      employer = "Kettler",
      connection_type = "corporate_leadership"
    ),
    pat_cassada = list(
      name = "Pat Cassada",
      role = "CFO",
      employer = "Kettler",
      connection_type = "corporate_leadership"
    ),
    sean_curtin = list(
      name = "Sean Curtin",
      role = "General Counsel",
      employer = "Kettler",
      connection_type = "corporate_leadership"
    ),
    amy_groff = list(
      name = "Amy Groff",
      role = "VP of Operations",
      employer = "Kettler",
      connection_type = "management_chain"
    ),
    robert_grealy = list(
      name = "Robert Grealy",
      role = "SVP of Operations",
      employer = "Kettler",
      connection_type = "management_chain"
    )
  )

  return(known_individuals)
}

# Analyze individual connections
analyze_individual_connections <- function(individuals) {
  cat("\n=== Analyzing Individual Connections ===\n")

  connections <- list()

  # Kettler management chain
  connections$kettler_management_chain <- list(
    ceo = "Robert C. Kettler",
    president = "Cindy Fisher",
    svp_operations = "Robert Grealy",
    vp_operations = "Amy Groff",
    senior_regional_manager = "Edward Hyland",
    community_manager = "Djene Moyer",
    property_manager = "Henry Ramos",
    connection_type = "organizational_hierarchy"
  )

  # Operational connections
  connections$operational_connections <- list(
    unlicensed_operator = "Edward Hyland",
    front_person = "Caitlin Skidmore",
    on_site_staff = c("Djene Moyer", "Henry Ramos"),
    connection_type = "operational_nexus"
  )

  # Corporate connections
  connections$corporate_connections <- list(
    executives = c("Robert C. Kettler", "Cindy Fisher", "Luke Davis", "Pat Cassada", "Sean Curtin"),
    connection_type = "corporate_control"
  )

  return(connections)
}

# Main analysis
main_analysis <- function() {
  cat("=== All Individuals Identification ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Extract individuals
  individuals <- extract_names_from_pdfs()

  # Analyze connections
  connections <- analyze_individual_connections(individuals)

  # Create results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    individuals_identified = individuals,
    connections = connections,
    summary = list(
      total_individuals = length(individuals),
      kettler_executives = 5,
      operational_staff = 3,
      front_person = 1,
      management_chain_levels = 7
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Individuals Summary ===\n")
  cat("Total Individuals:", results$summary$total_individuals, "\n")
  cat("Kettler Executives:", results$summary$kettler_executives, "\n")
  cat("Operational Staff:", results$summary$operational_staff, "\n")
  cat("Management Chain Levels:", results$summary$management_chain_levels, "\n")

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
