#!/usr/bin/env Rscript
# Comprehensive search for all Kettler employees in DC, MD, VA, NY, NJ, CT
# Also search for Caitlin Skidmore connections

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research")
OUTPUT_FILE <- file.path(RESEARCH_DIR, "kettler_employees_all_states_license_search.json")

# Load existing individuals
load_existing_individuals <- function() {
  individuals_file <- file.path(RESEARCH_DIR, "all_individuals_identified.json")
  if (file.exists(individuals_file)) {
    return(fromJSON(individuals_file))
  }
  return(NULL)
}

# All Kettler employees to search
kettler_employees <- list(
  list(name = "Robert C. Kettler", role = "CEO", variations = c("Robert Kettler", "Robert C Kettler", "Bob Kettler")),
  list(name = "Cindy Fisher", role = "President", variations = c("Cynthia Fisher", "Cindy Fisher")),
  list(name = "Luke Davis", role = "CIO", variations = c("Luke Davis", "L. Davis")),
  list(name = "Pat Cassada", role = "CFO", variations = c("Pat Cassada", "Patrick Cassada", "P. Cassada")),
  list(name = "Sean Curtin", role = "General Counsel", variations = c("Sean Curtin", "S. Curtin"), needs_bar_check = TRUE),
  list(name = "Amy Groff", role = "VP Operations", variations = c("Amy Groff", "A. Groff")),
  list(name = "Robert Grealy", role = "SVP Operations", variations = c("Robert Grealy", "Bob Grealy", "R. Grealy")),
  list(name = "Edward Hyland", role = "Senior Regional Manager", variations = c("Edward Hyland", "Ed Hyland", "E. Hyland"), already_confirmed_unlicensed = TRUE),
  list(name = "Djene Moyer", role = "Community Manager", variations = c("Djene Moyer", "D. Moyer")),
  list(name = "Henry Ramos", role = "Property Manager", variations = c("Henry Ramos", "H. Ramos")),
  list(name = "Caitlin Skidmore", role = "Principal Broker", variations = c("Caitlin Skidmore", "Caitlin M Skidmore", "Caitlin Marie Skidmore", "CAITLIN MARIE SKIDMORE"), is_front_person = TRUE),
  list(name = "Kristina Thoummarath", role = "Chief of Staff", variations = c("Kristina Thoummarath", "K. Thoummarath")),
  list(name = "Christina Chang", role = "Head of Asset Management", variations = c("Christina Chang", "C. Chang")),
  list(name = "Todd Bowen", role = "SVP Strategic Services", variations = c("Todd Bowen", "T. Bowen")),
  list(name = "Jeffrey Williams", role = "VP Human Resources", variations = c("Jeffrey Williams", "Jeff Williams", "J. Williams"))
)

# States to search with URLs
states <- list(
  dc = list(code = "DC", name = "District of Columbia",
            dpor_url = "https://www.dcopla.com/",
            real_estate_url = "https://www.dcopla.com/realestate/"),
  md = list(code = "MD", name = "Maryland",
            dpor_url = "https://www.dllr.state.md.us/license/",
            real_estate_url = "https://www.dllr.state.md.us/license/realestate/"),
  va = list(code = "VA", name = "Virginia",
            dpor_url = "https://www.dpor.virginia.gov/LicenseLookup",
            real_estate_url = "https://www.dpor.virginia.gov/LicenseLookup"),
  ny = list(code = "NY", name = "New York",
            dpor_url = "https://www.dos.ny.gov/licensing/",
            real_estate_url = "https://www.dos.ny.gov/licensing/realestate/"),
  nj = list(code = "NJ", name = "New Jersey",
            dpor_url = "https://www.njconsumeraffairs.gov/",
            real_estate_url = "https://www.njconsumeraffairs.gov/rec/Pages/default.aspx"),
  ct = list(code = "CT", name = "Connecticut",
            dpor_url = "https://www.ct.gov/dcp/",
            real_estate_url = "https://www.ct.gov/dcp/cwp/view.asp?a=1629&q=274388")
)

create_search_framework <- function() {
  cat("=== Creating License Search Framework for All Kettler Employees ===\n")
  cat("Date:", Sys.Date(), "\n\n")

  # Load existing data
  existing <- load_existing_individuals()

  results <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      total_employees = length(kettler_employees),
      states_searched = names(states),
      search_type = "comprehensive_license_verification",
      status = "framework_ready"
    ),
    employees = list(),
    states = states,
    search_plan = list(
      total_searches_needed = length(kettler_employees) * length(states),
      license_types = c("Real Estate Broker", "Real Estate Salesperson", "Property Management License", "State Bar Admission"),
      note = "Each employee will be searched in each state's licensing database"
    )
  )

  # Create search entries for each employee
  for (i in seq_along(kettler_employees)) {
    emp <- kettler_employees[[i]]
    emp_id <- tolower(gsub(" ", "_", emp$name))

    results$employees[[emp_id]] <- list(
      name = emp$name,
      role = emp$role,
      name_variations = emp$variations,
      needs_bar_check = ifelse(is.null(emp$needs_bar_check), FALSE, emp$needs_bar_check),
      is_front_person = ifelse(is.null(emp$is_front_person), FALSE, emp$is_front_person),
      already_confirmed_unlicensed = ifelse(is.null(emp$already_confirmed_unlicensed), FALSE, emp$already_confirmed_unlicensed),
      searches = list()
    )

    # Create search entries for each state
    for (state_id in names(states)) {
      state <- states[[state_id]]

      # Determine status
      emp_status <- ifelse(is.null(emp$already_confirmed_unlicensed), FALSE, emp$already_confirmed_unlicensed)
      search_status <- if (emp_status && state_id == "va") {
        "already_confirmed_unlicensed"
      } else {
        "pending"
      }

      results$employees[[emp_id]]$searches[[state_id]] <- list(
        state = state$name,
        state_code = state$code,
        search_url = state$real_estate_url,
        status = search_status,
        licenses_found = list(),
        violations = list(),
        note = paste("Search for", emp$name, "in", state$name)
      )
    }
  }

  # Add Caitlin Skidmore connections search
  results$caitlin_skidmore_connections <- list(
    note = "Search for individuals connected to Caitlin Skidmore",
    search_targets = c(
      "Firms where Skidmore is principal broker",
      "Individuals at same addresses",
      "License applications co-signed by Skidmore",
      "Business partners of Skidmore"
    ),
    states_to_search = names(states),
    status = "pending"
  )

  dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)
  write_json(results, OUTPUT_FILE, pretty = TRUE, auto_unbox = TRUE)
  cat("Saved search framework to:", OUTPUT_FILE, "\n")

  cat("\n=== Framework Summary ===\n")
  cat("Total employees:", length(kettler_employees), "\n")
  cat("Total states:", length(states), "\n")
  cat("Total searches:", length(kettler_employees) * length(states), "\n")
  cat("Bar association checks needed:", sum(sapply(kettler_employees, function(e) !is.null(e$needs_bar_check) && e$needs_bar_check)), "\n")
  cat("\nReady for browser automation\n")

  return(results)
}

if (!interactive()) create_search_framework()
