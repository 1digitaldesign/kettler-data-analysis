#!/usr/bin/env Rscript
# Search all Kettler employees for real estate licenses in DC, MD, VA, NY, NJ, CT
# Also search for Caitlin Skidmore's connections

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "all_kettler_employees_license_search.json")

# All Kettler employees identified
kettler_employees <- list(
  robert_kettler = list(name = "Robert C. Kettler", name_variations = c("Robert Kettler", "Robert C Kettler", "Bob Kettler")),
  cindy_fisher = list(name = "Cindy Fisher", name_variations = c("Cynthia Fisher", "Cindy Fisher")),
  luke_davis = list(name = "Luke Davis", name_variations = c("Luke Davis", "L. Davis")),
  pat_cassada = list(name = "Pat Cassada", name_variations = c("Pat Cassada", "Patrick Cassada", "P. Cassada")),
  sean_curtin = list(name = "Sean Curtin", name_variations = c("Sean Curtin", "S. Curtin")),
  amy_groff = list(name = "Amy Groff", name_variations = c("Amy Groff", "A. Groff")),
  robert_grealy = list(name = "Robert Grealy", name_variations = c("Robert Grealy", "Bob Grealy", "R. Grealy")),
  edward_hyland = list(name = "Edward Hyland", name_variations = c("Edward Hyland", "Ed Hyland", "E. Hyland")),
  djene_moyer = list(name = "Djene Moyer", name_variations = c("Djene Moyer", "D. Moyer")),
  henry_ramos = list(name = "Henry Ramos", name_variations = c("Henry Ramos", "H. Ramos")),
  caitlin_skidmore = list(name = "Caitlin Skidmore", name_variations = c("Caitlin Skidmore", "Caitlin M Skidmore", "Caitlin Marie Skidmore", "CAITLIN MARIE SKIDMORE")),
  kristina_thoummarath = list(name = "Kristina Thoummarath", name_variations = c("Kristina Thoummarath", "K. Thoummarath")),
  christina_chang = list(name = "Christina Chang", name_variations = c("Christina Chang", "C. Chang")),
  todd_bowen = list(name = "Todd Bowen", name_variations = c("Todd Bowen", "T. Bowen")),
  jeffrey_williams = list(name = "Jeffrey Williams", name_variations = c("Jeffrey Williams", "Jeff Williams", "J. Williams"))
)

# States to search
states_to_search <- list(
  dc = list(code = "DC", name = "District of Columbia", dpor_url = "https://www.dcopla.com/"),
  md = list(code = "MD", name = "Maryland", dpor_url = "https://www.dllr.state.md.us/license/"),
  va = list(code = "VA", name = "Virginia", dpor_url = "https://www.dpor.virginia.gov/LicenseLookup"),
  ny = list(code = "NY", name = "New York", dpor_url = "https://www.dos.ny.gov/licensing/"),
  nj = list(code = "NJ", name = "New Jersey", dpor_url = "https://www.njconsumeraffairs.gov/"),
  ct = list(code = "CT", name = "Connecticut", dpor_url = "https://www.ct.gov/dcp/")
)

search_all_employees <- function() {
  cat("=== Searching All Kettler Employees for Licenses ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      total_employees = length(kettler_employees),
      states_searched = names(states_to_search),
      status = "framework_ready_for_browser_automation"
    ),
    employees = list(),
    states = states_to_search,
    search_strategy = list(
      method = "Browser automation via Playwright MCP",
      note = "Each employee will be searched in each state's DPOR database",
      license_types = c("Real Estate Broker", "Real Estate Salesperson", "Property Management License", "State Bar Admission")
    )
  )

  # Create search framework for each employee
  for (emp_id in names(kettler_employees)) {
    emp <- kettler_employees[[emp_id]]
    results$employees[[emp_id]] <- list(
      name = emp$name,
      name_variations = emp$name_variations,
      searches = list()
    )

    # Create search entries for each state
    for (state_id in names(states_to_search)) {
      state <- states_to_search[[state_id]]
      results$employees[[emp_id]]$searches[[state_id]] <- list(
        state = state$name,
        state_code = state$code,
        search_url = state$dpor_url,
        status = "pending_browser_automation",
        licenses_found = list(),
        note = paste("Search for", emp$name, "in", state$name)
      )
    }
  }

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved search framework to:", OUTPUT_FILE, "\n")

  cat("\n=== Search Framework Created ===\n")
  cat("Total employees:", length(kettler_employees), "\n")
  cat("Total states:", length(states_to_search), "\n")
  cat("Total searches needed:", length(kettler_employees) * length(states_to_search), "\n")
  cat("\nReady for browser automation execution\n")

  return(results)
}

if (!interactive()) search_all_employees()
