#!/usr/bin/env Rscript
# Maryland DLLR License Search with Manual CAPTCHA Support
# This script provides a framework for searching Maryland licenses
# User must manually complete CAPTCHA in browser, then script continues

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research", "license_searches", "maryland")
dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)

# Employees to search
EMPLOYEES <- list(
  list(name = "Edward Hyland", last_name = "Hyland", first_name = "Edward", priority = "HIGH"),
  list(name = "Robert Kettler", last_name = "Kettler", first_name = "Robert", priority = "HIGH"),
  list(name = "Caitlin Skidmore", last_name = "Skidmore", first_name = "Caitlin", priority = "HIGH"),
  list(name = "Cindy Fisher", last_name = "Fisher", first_name = "Cindy", priority = "MEDIUM"),
  list(name = "Luke Davis", last_name = "Davis", first_name = "Luke", priority = "MEDIUM"),
  list(name = "Pat Cassada", last_name = "Cassada", first_name = "Pat", priority = "MEDIUM"),
  list(name = "Sean Curtin", last_name = "Curtin", first_name = "Sean", priority = "MEDIUM"),
  list(name = "Amy Groff", last_name = "Groff", first_name = "Amy", priority = "MEDIUM"),
  list(name = "Robert Grealy", last_name = "Grealy", first_name = "Robert", priority = "MEDIUM"),
  list(name = "Djene Moyer", last_name = "Moyer", first_name = "Djene", priority = "MEDIUM"),
  list(name = "Henry Ramos", last_name = "Ramos", first_name = "Henry", priority = "MEDIUM"),
  list(name = "Kristina Thoummarath", last_name = "Thoummarath", first_name = "Kristina", priority = "MEDIUM"),
  list(name = "Christina Chang", last_name = "Chang", first_name = "Christina", priority = "MEDIUM"),
  list(name = "Todd Bowen", last_name = "Bowen", first_name = "Todd", priority = "MEDIUM"),
  list(name = "Jeffrey Williams", last_name = "Williams", first_name = "Jeffrey", priority = "MEDIUM")
)

# Search URL
MARYLAND_URL <- "https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name"

# Create search framework
create_search_framework <- function() {
  framework <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      state = "Maryland",
      url = MARYLAND_URL,
      method = "Manual CAPTCHA + Browser Automation",
      total_employees = length(EMPLOYEES),
      note = "User must manually complete CAPTCHA for each search. Script waits for button to become enabled."
    ),
    searches = list()
  )

  for (i in seq_along(EMPLOYEES)) {
    emp <- EMPLOYEES[[i]]
    framework$searches[[paste0("employee_", i)]] <- list(
      name = emp$name,
      last_name = emp$last_name,
      first_name = emp$first_name,
      priority = emp$priority,
      status = "pending",
      captcha_completed = FALSE,
      search_executed = FALSE,
      results_found = "pending"
    )
  }

  return(framework)
}

# Save framework
framework <- create_search_framework()
framework_file <- file.path(RESEARCH_DIR, "maryland_search_framework.json")
write_json(framework, framework_file, pretty = TRUE, auto_unbox = TRUE)

cat("=== Maryland License Search Framework Created ===\n")
cat("Date:", Sys.Date(), "\n")
cat("Total Employees:", length(EMPLOYEES), "\n")
cat("Framework saved to:", framework_file, "\n\n")
cat("INSTRUCTIONS:\n")
cat("1. Use Playwright MCP to navigate to:", MARYLAND_URL, "\n")
cat("2. For each employee:\n")
cat("   a. Fill in Last Name field\n")
cat("   b. Manually complete reCAPTCHA\n")
cat("   c. Wait for Search button to become enabled\n")
cat("   d. Click Search button\n")
cat("   e. Extract results\n")
cat("3. Update framework JSON with results\n\n")
cat("HIGH PRIORITY (Complete First):\n")
for (emp in EMPLOYEES) {
  if (emp$priority == "HIGH") {
    cat("  -", emp$name, "\n")
  }
}
