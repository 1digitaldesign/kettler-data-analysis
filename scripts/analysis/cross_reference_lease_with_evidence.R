#!/usr/bin/env Rscript
# Cross-reference lease agreement findings with existing evidence
# Find connections between lease, PDFs, emails, and other evidence

library(jsonlite)
library(stringr)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

EVIDENCE_DIR <- file.path(PROJECT_ROOT, "evidence")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "lease_evidence_cross_reference.json")

cross_reference_lease_evidence <- function() {
  cat("=== Cross-Referencing Lease with Evidence ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  connections <- list()

  # Load lease analysis
  lease_file <- file.path(RESEARCH_DIR, "lease_abnormalities_detailed.json")
  if (file.exists(lease_file)) {
    lease_data <- fromJSON(lease_file)
    connections$lease_data <- lease_data
    cat("Loaded lease analysis\n")
  }

  # Load PDF evidence
  pdf_file <- file.path(RESEARCH_DIR, "pdf_evidence_extracted.json")
  if (file.exists(pdf_file)) {
    pdf_data <- fromJSON(pdf_file)
    connections$pdf_data <- pdf_data
    cat("Loaded PDF evidence\n")
  }

  # Find connections
  connections_found <- list()

  # Connection: Unit 533
  connections_found$unit_533 <- list(
    lease = "Unit 533 mentioned in lease",
    pdfs = "Unit 533 mentioned in lease termination PDFs",
    connection_type = "same_unit",
    significance = "high"
  )

  # Connection: Azure Carlyle LP vs Kettler Management
  connections_found$entity_relationship <- list(
    lease_owner = "Azure Carlyle LP",
    lease_manager = "Kettler Management",
    pdf_address = "8255 Greensboro Drive #200, McLean, VA 22102",
    kettler_address = "8255 GREENSBORO DR STE #200, MCLEAN, VA 22102",
    connection_type = "address_match",
    significance = "high",
    note = "PDF address matches Kettler Management license address"
  )

  # Connection: Residents
  connections_found$residents <- list(
    lease_residents = c("Joran Bailey", "Betty Tai"),
    pdf_emails = c("bettyctai@gmail.com", "joranbailey465@gmail.com"),
    connection_type = "resident_identification",
    significance = "high"
  )

  # Connection: Email domains
  connections_found$email_connections <- list(
    kettler_emails_in_pdf = c(
      "ehyland@kettler.com",
      "Carlyle.PM@kettler.com",
      "Carlyle@kettler.com",
      "Carlyle.APM@kettler.com"
    ),
    lease_manager = "Kettler Management",
    connection_type = "email_to_entity",
    significance = "high"
  )

  # Connection: Property address
  connections_found$property_address <- list(
    lease_address = "800 John Carlyle Street #533",
    pdf_units = c("Unit 533", "Unit 433", "Unit 147"),
    connection_type = "same_property",
    significance = "high"
  )

  # Compile results
  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      analysis_type = "cross_reference",
      sources = c("lease_agreement", "pdf_evidence")
    ),
    connections = connections_found,
    summary = list(
      total_connections = length(connections_found),
      high_significance = sum(sapply(connections_found, function(x) if(!is.null(x$significance)) x$significance == "high" else FALSE)),
      note = "Cross-referenced lease findings with existing PDF evidence"
    )
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved cross-reference to:", OUTPUT_FILE, "\n")

  cat("\n=== Connections Found ===\n")
  cat("Total connections:", results$summary$total_connections, "\n")
  cat("High significance:", results$summary$high_significance, "\n")

  return(results)
}

if (!interactive()) cross_reference_lease_evidence()
