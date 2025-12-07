#!/usr/bin/env Rscript
# Search Regulatory Agencies
# Identifies relevant federal, state, and local agencies for filing complaints

library(dplyr)
library(jsonlite)

# Configuration
RESEARCH_DIR <- "../research"
FILINGS_DIR <- "../filings"
dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(FILINGS_DIR, "federal"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(FILINGS_DIR, "state"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(FILINGS_DIR, "local"), showWarnings = FALSE, recursive = TRUE)

# Federal regulatory agencies
FEDERAL_AGENCIES <- data.frame(
  agency = c(
    "Federal Trade Commission (FTC)",
    "Consumer Financial Protection Bureau (CFPB)",
    "Department of Housing and Urban Development (HUD)",
    "Securities and Exchange Commission (SEC)",
    "Internal Revenue Service (IRS)",
    "Department of Justice (DOJ)",
    "Federal Bureau of Investigation (FBI)"
  ),
  jurisdiction = c(
    "Consumer fraud, deceptive practices",
    "Financial services, mortgage fraud",
    "Housing discrimination, fair housing violations",
    "Securities fraud, investment schemes",
    "Tax fraud, unreported income",
    "Federal crimes, fraud schemes",
    "Federal criminal investigations"
  ),
  filing_type = c(
    "Consumer complaint",
    "Consumer complaint",
    "Fair housing complaint",
    "Tip, complaint, referral",
    "Tax fraud report",
    "Criminal complaint referral",
    "Criminal complaint referral"
  ),
  website = c(
    "https://www.ftc.gov",
    "https://www.consumerfinance.gov",
    "https://www.hud.gov",
    "https://www.sec.gov",
    "https://www.irs.gov",
    "https://www.justice.gov",
    "https://www.fbi.gov"
  ),
  stringsAsFactors = FALSE
)

# State regulatory agencies (focus on Virginia and other relevant states)
STATE_AGENCIES <- data.frame(
  state = c("VA", "NC", "TX", "MD", "MO", "NE"),
  agency = c(
    "Virginia Department of Professional and Occupational Regulation (DPOR)",
    "North Carolina Real Estate Commission",
    "Texas Real Estate Commission",
    "Maryland Department of Labor",
    "Missouri Division of Professional Registration",
    "Nebraska Real Estate Commission"
  ),
  jurisdiction = c(
    "Real estate license violations, professional misconduct",
    "Real estate license violations",
    "Real estate license violations",
    "Professional licensing violations",
    "Real estate license violations",
    "Real estate license violations"
  ),
  filing_type = c(
    "License complaint",
    "License complaint",
    "License complaint",
    "License complaint",
    "License complaint",
    "License complaint"
  ),
  website = c(
    "https://www.dpor.virginia.gov",
    "https://www.ncrec.gov",
    "https://www.trec.texas.gov",
    "https://www.dllr.state.md.us",
    "https://www.pr.mo.gov",
    "https://www.rec.ne.gov"
  ),
  stringsAsFactors = FALSE
)

# Local agencies
LOCAL_AGENCIES <- data.frame(
  jurisdiction = c(
    "Fairfax County, VA",
    "Arlington County, VA",
    "City of Alexandria, VA",
    "Montgomery County, MD"
  ),
  agency = c(
    "Fairfax County Consumer Affairs",
    "Arlington County Consumer Affairs",
    "Alexandria Consumer Protection",
    "Montgomery County Office of Consumer Protection"
  ),
  jurisdiction_type = c(
    "Local consumer protection",
    "Local consumer protection",
    "Local consumer protection",
    "Local consumer protection"
  ),
  filing_type = c(
    "Consumer complaint",
    "Consumer complaint",
    "Consumer complaint",
    "Consumer complaint"
  ),
  website = c(
    "https://www.fairfaxcounty.gov/consumer",
    "https://www.arlingtonva.us",
    "https://www.alexandriava.gov",
    "https://www.montgomerycountymd.gov"
  ),
  stringsAsFactors = FALSE
)

# Create regulatory agency registry
create_regulatory_registry <- function() {
  registry <- list(
    federal = FEDERAL_AGENCIES,
    state = STATE_AGENCIES,
    local = LOCAL_AGENCIES,
    created_date = Sys.Date()
  )

  registry_file <- file.path(RESEARCH_DIR, "regulatory_agencies_registry.json")
  write_json(registry, registry_file, pretty = TRUE)
  cat("Created regulatory agency registry:", registry_file, "\n")

  # Also save as CSV for easy viewing
  write.csv(FEDERAL_AGENCIES, file.path(FILINGS_DIR, "federal", "federal_agencies.csv"), row.names = FALSE)
  write.csv(STATE_AGENCIES, file.path(FILINGS_DIR, "state", "state_agencies.csv"), row.names = FALSE)
  write.csv(LOCAL_AGENCIES, file.path(FILINGS_DIR, "local", "local_agencies.csv"), row.names = FALSE)

  return(registry)
}

# Identify relevant agencies based on evidence
identify_relevant_agencies <- function(evidence_data) {
  relevant <- list(
    federal = c(),
    state = c(),
    local = c()
  )

  # Check for real estate violations
  if (any(grepl("real estate|license|DPOR|broker", evidence_data, ignore.case = TRUE))) {
    relevant$state <- c(relevant$state, "DPOR", "State Real Estate Commissions")
  }

  # Check for housing violations
  if (any(grepl("housing|HUD|fair housing|discrimination", evidence_data, ignore.case = TRUE))) {
    relevant$federal <- c(relevant$federal, "HUD")
  }

  # Check for consumer fraud
  if (any(grepl("fraud|deceptive|consumer|misrepresentation", evidence_data, ignore.case = TRUE))) {
    relevant$federal <- c(relevant$federal, "FTC", "CFPB")
    relevant$local <- c(relevant$local, "Local Consumer Protection")
  }

  # Check for financial fraud
  if (any(grepl("financial|mortgage|loan|securities", evidence_data, ignore.case = TRUE))) {
    relevant$federal <- c(relevant$federal, "CFPB", "SEC")
  }

  return(relevant)
}

# Main execution
if (!interactive()) {
  cat("Creating regulatory agency registry...\n")
  registry <- create_regulatory_registry()
  cat("\nRegistry created with", nrow(FEDERAL_AGENCIES), "federal,",
      nrow(STATE_AGENCIES), "state, and", nrow(LOCAL_AGENCIES), "local agencies\n")
}
