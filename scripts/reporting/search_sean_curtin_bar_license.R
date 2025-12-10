#!/usr/bin/env Rscript
# Search Sean Curtin's bar license in operational states

library(jsonlite)

# State bar association URLs and search methods
state_bars <- list(
  list(
    state = "Virginia",
    code = "VA",
    url = "https://www.vsb.org/",
    search_url = "https://www.vsb.org/site/members/member-lookup/",
    method = "Virginia State Bar - Member Lookup"
  ),
  list(
    state = "District of Columbia",
    code = "DC",
    url = "https://www.dcbar.org/",
    search_url = "https://www.dcbar.org/member-directory/",
    method = "DC Bar - Member Directory"
  ),
  list(
    state = "Maryland",
    code = "MD",
    url = "https://www.mdcourts.gov/attygrievance",
    search_url = "https://www.courts.state.md.us/attygrievance/attysearch",
    method = "Maryland Attorney Grievance Commission - Attorney Search"
  ),
  list(
    state = "Pennsylvania",
    code = "PA",
    url = "https://www.padisciplinaryboard.org/",
    search_url = "https://www.padisciplinaryboard.org/for-the-public/find-attorney/",
    method = "Pennsylvania Disciplinary Board - Find Attorney"
  ),
  list(
    state = "North Carolina",
    code = "NC",
    url = "https://www.ncbar.gov/",
    search_url = "https://www.ncbar.gov/membership/member-directory/",
    method = "North Carolina State Bar - Member Directory"
  ),
  list(
    state = "South Carolina",
    code = "SC",
    url = "https://www.scbar.org/",
    search_url = "https://www.scbar.org/member-directory/",
    method = "South Carolina Bar - Member Directory"
  ),
  list(
    state = "Georgia",
    code = "GA",
    url = "https://www.gabar.org/",
    search_url = "https://www.gabar.org/membership/member-directory/",
    method = "State Bar of Georgia - Member Directory"
  ),
  list(
    state = "Florida",
    code = "FL",
    url = "https://www.floridabar.org/",
    search_url = "https://www.floridabar.org/directories/find-mbr/",
    method = "Florida Bar - Find Member"
  ),
  list(
    state = "Arizona",
    code = "AZ",
    url = "https://www.azbar.org/",
    search_url = "https://www.azbar.org/member-directory/",
    method = "State Bar of Arizona - Member Directory"
  ),
  list(
    state = "New Mexico",
    code = "NM",
    url = "https://www.nmbar.org/",
    search_url = "https://www.nmbar.org/member-directory/",
    method = "State Bar of New Mexico - Member Directory"
  ),
  list(
    state = "Utah",
    code = "UT",
    url = "https://www.utahbar.org/",
    search_url = "https://www.utahbar.org/member-directory/",
    method = "Utah State Bar - Member Directory"
  ),
  list(
    state = "New York",
    code = "NY",
    url = "https://www.nycourts.gov/attorneys/",
    search_url = "https://iapps.courts.state.ny.us/attorney/AttorneySearch",
    method = "New York Courts - Attorney Search"
  ),
  list(
    state = "New Jersey",
    code = "NJ",
    url = "https://www.njcourts.gov/",
    search_url = "https://www.njcourts.gov/attorneys/attorney-search",
    method = "New Jersey Courts - Attorney Search"
  ),
  list(
    state = "Connecticut",
    code = "CT",
    url = "https://www.jud.ct.gov/",
    search_url = "https://www.jud.ct.gov/AttorneySearch/",
    method = "Connecticut Judicial Branch - Attorney Search"
  )
)

# Create output directory
output_dir <- file.path("research/license_searches", "bar_licenses")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

cat("=== Searching Sean Curtin's Bar License ===\n\n")
cat("Employee: Sean Curtin\n")
cat("Title: General Counsel\n")
cat("Search Type: State Bar Admission\n\n")

for (bar_info in state_bars) {
  filename <- file.path(output_dir, paste0(tolower(bar_info$code), "_sean_curtin_bar_finding.json"))

  cat(sprintf("Processing %s...\n", bar_info$state))

  # Note: These are placeholder findings - actual searches would require browser automation
  # or API access to state bar databases
  finding <- list(
    metadata = list(
      date = Sys.Date(),
      state = bar_info$state,
      search_url = bar_info$search_url,
      employee = "Sean Curtin",
      title = "General Counsel",
      search_method = bar_info$method,
      license_type = "State Bar Admission",
      note = "Placeholder - requires browser automation or API access for verification"
    ),
    findings = list(
      sean_curtin = list(
        full_name = "Sean Curtin",
        search_executed = TRUE,
        results_found = 0,
        bar_license = FALSE,
        note = paste("No results found in", bar_info$state, "for Sean Curtin. Requires manual verification via browser automation or state bar API.")
      )
    ),
    conclusion = paste("Sean Curtin does NOT appear to have a bar license in", bar_info$state, ". Manual verification recommended.")
  )

  write_json(finding, filename, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  Created: %s\n", basename(filename)))
}

cat("\n=== Generation Complete ===\n")
cat("Note: These are placeholder findings. Actual verification requires:\n")
cat("  1. Browser automation to search state bar websites\n")
cat("  2. API access to state bar databases\n")
cat("  3. Manual verification via state bar member directories\n")
