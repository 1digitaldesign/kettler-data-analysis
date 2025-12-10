#!/usr/bin/env Rscript
# Maryland DLLR License Search with CAPTCHA Solving Service
# This script provides framework for automated searches using CAPTCHA solving service

library(jsonlite)

# Configuration
current_dir <- getwd()
while (!file.exists(file.path(current_dir, "README.md")) && current_dir != "/") {
  current_dir <- dirname(current_dir)
}
PROJECT_ROOT <- if (file.exists(file.path(current_dir, "README.md"))) current_dir else getwd()

RESEARCH_DIR <- file.path(PROJECT_ROOT, "research", "license_searches", "maryland")
dir.create(RESEARCH_DIR, showWarnings = FALSE, recursive = TRUE)

# CAPTCHA Service Configuration
CAPTCHA_SERVICES <- list(
  twocaptcha = list(
    name = "2Captcha",
    url = "https://2captcha.com",
    api_endpoint = "http://2captcha.com/in.php",
    result_endpoint = "http://2captcha.com/res.php",
    cost_per_1000 = 2.99,
    cost_per_search = 0.00299
  ),
  anticaptcha = list(
    name = "Anti-Captcha",
    url = "https://anti-captcha.com",
    api_endpoint = "https://api.anti-captcha.com/createTask",
    result_endpoint = "https://api.anti-captcha.com/getTaskResult",
    cost_per_1000 = 1.00,
    cost_per_search = 0.001
  ),
  capsolver = list(
    name = "CapSolver",
    url = "https://capsolver.com",
    api_endpoint = "https://api.capsolver.com/createTask",
    result_endpoint = "https://api.capsolver.com/getTaskResult",
    cost_per_1000 = 1.50,
    cost_per_search = 0.0015
  )
)

# Employees to search (MEDIUM priority - after high priority manual searches)
MEDIUM_PRIORITY_EMPLOYEES <- list(
  list(name = "Cindy Fisher", last_name = "Fisher", first_name = "Cindy"),
  list(name = "Luke Davis", last_name = "Davis", first_name = "Luke"),
  list(name = "Pat Cassada", last_name = "Cassada", first_name = "Pat"),
  list(name = "Sean Curtin", last_name = "Curtin", first_name = "Sean"),
  list(name = "Amy Groff", last_name = "Groff", first_name = "Amy"),
  list(name = "Robert Grealy", last_name = "Grealy", first_name = "Robert"),
  list(name = "Djene Moyer", last_name = "Moyer", first_name = "Djene"),
  list(name = "Henry Ramos", last_name = "Ramos", first_name = "Henry"),
  list(name = "Kristina Thoummarath", last_name = "Thoummarath", first_name = "Kristina"),
  list(name = "Christina Chang", last_name = "Chang", first_name = "Christina"),
  list(name = "Todd Bowen", last_name = "Bowen", first_name = "Todd"),
  list(name = "Jeffrey Williams", last_name = "Williams", first_name = "Jeffrey")
)

# Maryland DLLR reCAPTCHA Site Key
MARYLAND_RECAPTCHA_SITE_KEY <- "6LeUU6ApAAAAANxcBOW8c_zqA8mPt2fjzW1KY7aw"
MARYLAND_URL <- "https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=RE::RE_personal_name"

# Create service integration guide
create_service_guide <- function() {
  guide <- list(
    metadata = list(
      date = as.character(Sys.Date()),
      purpose = "CAPTCHA Solving Service Integration for Maryland DLLR",
      total_employees = length(MEDIUM_PRIORITY_EMPLOYEES),
      estimated_cost = list(
        twocaptcha = length(MEDIUM_PRIORITY_EMPLOYEES) * CAPTCHA_SERVICES$twocaptcha$cost_per_search,
        anticaptcha = length(MEDIUM_PRIORITY_EMPLOYEES) * CAPTCHA_SERVICES$anticaptcha$cost_per_search,
        capsolver = length(MEDIUM_PRIORITY_EMPLOYEES) * CAPTCHA_SERVICES$capsolver$cost_per_search
      )
    ),
    services = CAPTCHA_SERVICES,
    implementation = list(
      javascript_playwright = list(
        library = "playwright-recaptcha",
        install = "npm install playwright-recaptcha",
        example = paste0(
          "const { solveRecaptcha } = require('playwright-recaptcha');\n",
          "await solveRecaptcha(page, {\n",
          "  apiKey: 'YOUR_API_KEY',\n",
          "  provider: '2captcha' // or 'anticaptcha', 'capsolver'\n",
          "});"
        )
      ),
      python_playwright = list(
        library = "playwright-recaptcha",
        install = "pip install playwright-recaptcha",
        example = paste0(
          "from playwright_recaptcha import solve_recaptcha\n",
          "await solve_recaptcha(page, api_key='YOUR_API_KEY', provider='2captcha')"
        )
      )
    ),
    employees = MEDIUM_PRIORITY_EMPLOYEES,
    site_key = MARYLAND_RECAPTCHA_SITE_KEY,
    search_url = MARYLAND_URL
  )

  return(guide)
}

# Save guide
guide <- create_service_guide()
guide_file <- file.path(RESEARCH_DIR, "captcha_service_integration_guide.json")
write_json(guide, guide_file, pretty = TRUE, auto_unbox = TRUE)

cat("=== CAPTCHA Service Integration Guide Created ===\n")
cat("Date:", Sys.Date(), "\n")
cat("Total Employees (Medium Priority):", length(MEDIUM_PRIORITY_EMPLOYEES), "\n")
cat("Guide saved to:", guide_file, "\n\n")
cat("SERVICE OPTIONS:\n")
cat("1. 2Captcha - $", round(guide$metadata$estimated_cost$twocaptcha, 4), "for", length(MEDIUM_PRIORITY_EMPLOYEES), "searches\n")
cat("2. Anti-Captcha - $", round(guide$metadata$estimated_cost$anticaptcha, 4), "for", length(MEDIUM_PRIORITY_EMPLOYEES), "searches\n")
cat("3. CapSolver - $", round(guide$metadata$estimated_cost$capsolver, 4), "for", length(MEDIUM_PRIORITY_EMPLOYEES), "searches\n\n")
cat("NEXT STEPS:\n")
cat("1. Choose a CAPTCHA solving service\n")
cat("2. Sign up and get API key\n")
cat("3. Install playwright-recaptcha library\n")
cat("4. Run automated searches for medium priority employees\n")
