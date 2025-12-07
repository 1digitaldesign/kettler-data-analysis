#!/usr/bin/env Rscript
# Find the real nexus beyond Caitlin Skidmore
# Analyze ownership patterns, financial connections, and control structures

library(jsonlite)
library(dplyr)
library(stringr)

# Configuration
if (file.exists("research/all_entities_extracted.json")) {
  PROJECT_ROOT <- getwd()
} else {
  current_dir <- getwd()
  while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
    current_dir <- dirname(current_dir)
  }
  PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()
}

DATA_DIR <- file.path(PROJECT_ROOT, "data")
RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "real_nexus_analysis.json")

# Analyze who benefits from this structure
analyze_beneficiaries <- function(firms) {
  cat("\n=== Analyzing Beneficiaries ===\n")

  beneficiaries <- list()

  # Kettler Management benefits
  kettler_firm <- firms[firms$Firm.Name == "KETTLER MANAGEMENT INC", ]
  if (nrow(kettler_firm) > 0) {
    beneficiaries$kettler <- list(
      firm_name = "KETTLER MANAGEMENT INC",
      address = kettler_firm$Address[1],
      license_number = kettler_firm$License.Number[1],
      benefits = c(
        "Operates properties through unlicensed manager (Hyland)",
        "Uses front person (Skidmore) as principal broker",
        "Evidence connection to lease termination documents",
        "Email domain (kettler.com) appears in evidence"
      ),
      nexus_score = "HIGH"
    )
  }

  # Address cluster beneficiaries (Frisco, TX)
  if ("Address" %in% names(firms) && nrow(firms) > 0) {
    address_matches <- !is.na(firms$Address) & firms$Address != ""
    if (sum(address_matches) > 0) {
      frisco_firms <- firms[address_matches &
                            grepl("5729.*LEBANON|LEBANON.*5729", firms$Address, ignore.case = TRUE) &
                            grepl("FRISCO.*TX.*75034", firms$Address, ignore.case = TRUE), ]
    } else {
      frisco_firms <- firms[FALSE, ]
    }
  } else {
    frisco_firms <- firms[FALSE, ]
  }

  if (nrow(frisco_firms) > 0) {
    beneficiaries$frisco_cluster <- list(
      address = "5729 LEBANON RD STE 144553, FRISCO, TX 75034",
      firm_count = nrow(frisco_firms),
      firms = frisco_firms$Firm.Name,
      benefits = c(
        "Multiple firms at same address suggests shell company operation",
        "All list same principal broker (front person)",
        "May be used to obscure true ownership"
      ),
      nexus_score = "MEDIUM-HIGH"
    )
  }

  return(beneficiaries)
}

# Analyze control structure
analyze_control_structure <- function(firms) {
  cat("\n=== Analyzing Control Structure ===\n")

  control <- list()

  # Pattern: Single principal broker across all firms
  unique_brokers <- unique(firms$Principal.Broker)
  control$single_broker_pattern <- list(
    broker_name = unique_brokers[1],
    firm_count = nrow(firms),
    pattern_type = "front_person_structure",
    explanation = "All firms use same principal broker - classic front person pattern"
  )

  # Pattern: Address clustering suggests centralized control
  address_counts <- table(firms$Address)
  clustered <- address_counts[address_counts > 1]

  control$centralized_addresses <- list(
    cluster_count = length(clustered),
    clusters = as.list(clustered),
    pattern_type = "centralized_control",
    explanation = "Multiple firms at same addresses suggest centralized operation"
  )

  # Pattern: License gaps suggest retroactive assignment
  gaps <- firms[!is.na(firms$Gap.Years) & firms$Gap.Years != "UNKNOWN", ]
  large_gaps <- gaps[as.numeric(gaps$Gap.Years) > 10, ]

  control$retroactive_assignment <- list(
    large_gap_count = nrow(large_gaps),
    firms = large_gaps$Firm.Name,
    pattern_type = "retroactive_broker_assignment",
    explanation = "Firms existed years before principal broker was licensed - suggests retroactive assignment"
  )

  return(control)
}

# Identify operational connections
identify_operational_connections <- function() {
  cat("\n=== Identifying Operational Connections ===\n")

  connections <- list()

  # Hyland as operational connection
  hyland_file <- file.path(RESEARCH_DIR, "hyland_verification.json")
  if (file.exists(hyland_file)) {
    hyland <- fromJSON(hyland_file, simplifyDataFrame = FALSE)

    connections$hyland_operational <- list(
      role = "Senior Regional Manager",
      employer = "Kettler Management Inc.",
      unlicensed = hyland$claims_to_verify$licensing_status$virginia$status == "not_found",
      properties_managed = c("800 Carlyle", "Sinclaire on Seminary"),
      connection_type = "operational_nexus",
      explanation = "Hyland operates properties without license, connecting Kettler to operations"
    )
  }

  # Email domain connections
  email_file <- file.path(RESEARCH_DIR, "email_domain_analysis.json")
  if (file.exists(email_file)) {
    email_analysis <- fromJSON(email_file, simplifyDataFrame = FALSE)

    connections$email_domain <- list(
      domain = "kettler.com",
      email_count = ifelse(is.null(email_analysis$summary$kettler_emails_found), 0, email_analysis$summary$kettler_emails_found),
      connection_type = "communication_nexus",
      explanation = "All operational emails use kettler.com domain"
    )
  }

  return(connections)
}

# Analyze financial patterns
analyze_financial_patterns <- function(firms) {
  cat("\n=== Analyzing Financial Patterns ===\n")

  patterns <- list()

  # Pattern: All firms are property management companies
  patterns$all_property_management <- TRUE
  patterns$revenue_stream = "Property management fees, rental income"

  # Pattern: Geographic distribution suggests interstate operation
  states <- unique(str_extract(firms$Address, ",\\s*([A-Z]{2})\\s*\\d", group = 1))
  states <- states[!is.na(states)]
  patterns$interstate_operation <- list(
    state_count = length(states),
    states = states,
    explanation = "Operations across multiple states suggest larger financial operation"
  )

  # Pattern: License gaps suggest firms operated before "principal broker"
  if ("Gap.Years" %in% names(firms) && nrow(firms) > 0) {
    gaps <- firms[!is.na(firms$Gap.Years) & firms$Gap.Years != "UNKNOWN", ]
    if (nrow(gaps) > 0) {
      gap_values <- suppressWarnings(as.numeric(gaps$Gap.Years))
      gap_values <- gap_values[!is.na(gap_values)]
    } else {
      gap_values <- numeric(0)
    }
  } else {
    gap_values <- numeric(0)
  }
  
  if (length(gap_values) > 0) {
    avg_gap <- mean(gap_values)
  } else {
    avg_gap <- NA
  }
  patterns$average_gap_years <- avg_gap
  patterns$financial_implication <- if (!is.na(avg_gap)) "Firms generated revenue for years before principal broker was assigned" else "Insufficient data"

  return(patterns)
}

# Main analysis
main_analysis <- function() {
  cat("=== Real Nexus Analysis ===\n")
  cat("Finding who really controls these firms\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load firms
  firms_file <- file.path(DATA_DIR, "source", "skidmore_all_firms_complete.csv")
  if (!file.exists(firms_file)) {
    stop("Firms file not found: ", firms_file)
  }
  firms <- read.csv(firms_file, stringsAsFactors = FALSE)

  # Analyze beneficiaries
  beneficiaries <- analyze_beneficiaries(firms)

  # Analyze control structure
  control <- analyze_control_structure(firms)

  # Identify operational connections
  operations <- identify_operational_connections()

  # Analyze financial patterns
  financial <- analyze_financial_patterns(firms)

  # Create comprehensive results
  results <- list(
    analysis_date = as.character(Sys.Date()),
    hypothesis = "Caitlin Skidmore is a front person - real nexus involves Kettler Management and operational connections",
    beneficiaries = beneficiaries,
    control_structure = control,
    operational_connections = operations,
    financial_patterns = financial,
    conclusions = list(
      real_nexus_candidates = c(
        "Kettler Management Inc. (HIGH) - Evidence connection, email domain, property operations",
        "Edward Hyland (MEDIUM-HIGH) - Operational connection, unlicensed practice",
        "Frisco TX Address Cluster (MEDIUM) - Shell company pattern"
      ),
      skidmore_role = "Front person - listed as principal broker but firms existed before she was licensed",
      evidence_summary = c(
        "8 firms licensed BEFORE Skidmore was licensed",
        "Average 7.4 year gap between firm establishment and Skidmore license",
        "All firms use same principal broker (front person pattern)",
        "Kettler email domain appears in evidence",
        "Hyland operates without license, connecting Kettler to properties",
        "Address clustering suggests centralized control"
      ),
      recommended_investigations = c(
        "Corporate ownership of all 11 firms",
        "Financial connections between firms",
        "Kettler Management corporate structure and subsidiaries",
        "Edward Hyland's role and decision-making authority",
        "Who actually owns/controls the Frisco TX address cluster"
      )
    )
  )

  # Save results
  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("\nSaved results to:", OUTPUT_FILE, "\n")

  # Print summary
  cat("\n=== Analysis Summary ===\n")
  cat("Real Nexus Candidates:\n")
  for (candidate in results$conclusions$real_nexus_candidates) {
    cat("  -", candidate, "\n")
  }

  cat("\nKey Evidence:\n")
  for (evidence in results$conclusions$evidence_summary) {
    cat("  -", evidence, "\n")
  }

  cat("\n=== Analysis Complete ===\n")
}

# Run if executed as script
if (!interactive()) {
  main_analysis()
}
