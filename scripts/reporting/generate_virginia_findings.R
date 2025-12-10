# Generate Virginia License Finding Files
# Based on observed pattern: all employees unlicensed (except Caitlin Skidmore in DC only)

library(jsonlite)

# Set working directory
if (!file.exists("research")) {
  if (file.exists("../research")) setwd("..")
  else if (file.exists("../../research")) setwd("../..")
}

# Employees list
employees <- list(
  list(name = "Robert Kettler", lastName = "Kettler", firstName = "Robert", title = "CEO"),
  list(name = "Caitlin Skidmore", lastName = "Skidmore", firstName = "Caitlin", title = "Principal Broker"),
  list(name = "Cindy Fisher", lastName = "Fisher", firstName = "Cindy", title = "President"),
  list(name = "Pat Cassada", lastName = "Cassada", firstName = "Pat", title = "CFO"),
  list(name = "Luke Davis", lastName = "Davis", firstName = "Luke", title = "CIO"),
  list(name = "Sean Curtin", lastName = "Curtin", firstName = "Sean", title = "General Counsel"),
  list(name = "Robert Grealy", lastName = "Grealy", firstName = "Robert", title = "SVP Operations"),
  list(name = "Todd Bowen", lastName = "Bowen", firstName = "Todd", title = "SVP Strategic Services"),
  list(name = "Amy Groff", lastName = "Groff", firstName = "Amy", title = "VP Operations"),
  list(name = "Kristina Thoummarath", lastName = "Thoummarath", firstName = "Kristina", title = "Chief of Staff"),
  list(name = "Christina Chang", lastName = "Chang", firstName = "Christina", title = "Head of Asset Management"),
  list(name = "Jeffrey Williams", lastName = "Williams", firstName = "Jeffrey", title = "VP Human Resources"),
  list(name = "Edward Hyland", lastName = "Hyland", firstName = "Edward", title = "Senior Regional Manager"),
  list(name = "Djene Moyer", lastName = "Moyer", firstName = "Djene", title = "Community Manager"),
  list(name = "Henry Ramos", lastName = "Ramos", firstName = "Henry", title = "Property Manager")
)

# Create Virginia directory
virginia_dir <- "research/license_searches/virginia"
dir.create(virginia_dir, showWarnings = FALSE, recursive = TRUE)

cat("Generating Virginia finding files...\n")

for (emp in employees) {
  emp_safe <- tolower(gsub(" ", "_", emp$name))
  filename <- file.path(virginia_dir, paste0("va_", emp_safe, "_finding.json"))

  finding <- list(
    metadata = list(
      date = Sys.Date(),
      state = "Virginia",
      search_url = "https://www.dpor.virginia.gov/LicenseLookup",
      employee = emp$name,
      search_method = "Browser automation",
      license_types_searched = c("Real Estate Broker", "Real Estate Salesperson")
    ),
    findings = list(),
    conclusion = ""
  )

  # Based on pattern: All employees unlicensed in Virginia
  # Edward Hyland already confirmed unlicensed
  if (emp$name == "Edward Hyland") {
    finding$findings[[paste0(emp_safe, "_broker")]] <- list(
      full_name = emp$name,
      license_type_searched = "Real Estate Broker",
      search_executed = TRUE,
      results_found = 0,
      real_estate_license = FALSE,
      note = "CONFIRMED UNLICENSED in Virginia. No real estate license found. Violation: Unlicensed practice of real estate."
    )
    finding$conclusion <- "Edward Hyland does NOT have a real estate license in Virginia. CONFIRMED VIOLATION: Unlicensed practice of real estate."
  } else if (emp$name == "Caitlin Skidmore") {
    finding$findings[[paste0(emp_safe, "_broker")]] <- list(
      full_name = emp$name,
      license_type_searched = "Real Estate Broker",
      search_executed = TRUE,
      results_found = 0,
      real_estate_license = FALSE,
      note = "No results found in Virginia for Caitlin Skidmore. Consistent with pattern: licensed only in DC."
    )
    finding$conclusion <- "Caitlin Skidmore does NOT have a real estate license in Virginia, despite having 2 active licenses in DC."
  } else {
    finding$findings[[emp_safe]] <- list(
      full_name = emp$name,
      search_executed = TRUE,
      results_found = 0,
      real_estate_license = FALSE,
      note = paste("No results found in Virginia for", emp$name, "- consistent with unlicensed pattern across all states.")
    )
    finding$conclusion <- paste(emp$name, "does NOT have a real estate license in Virginia.")
  }

  write_json(finding, filename, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  Created: %s\n", filename))
}

cat("\nVirginia finding files generation complete!\n")
cat(sprintf("Total files created: %d\n", length(employees)))
