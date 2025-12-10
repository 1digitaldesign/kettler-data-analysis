#!/usr/bin/env Rscript
# Generate Complaint Letters for Administrative Filings
#
# This script generates complaint letters for each state regulatory agency
# based on the consolidated findings.

library(jsonlite)
library(dplyr)
library(stringr)

# Set working directory to repo root
if (dir.exists("research")) {
  # Already in repo root
} else if (dir.exists("../research")) {
  setwd("..")
} else if (dir.exists("../../research")) {
  setwd("../..")
}

# Output directory
output_dir <- file.path("research", "license_searches", "complaint_letters")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Read consolidated findings
findings_file <- file.path("research", "license_searches", "consolidated", "all_findings.csv")
if (!file.exists(findings_file)) {
  stop("Consolidated findings file not found. Run consolidate_license_findings_simple.R first.")
}

findings <- read.csv(findings_file, stringsAsFactors = FALSE)

# State agency information
agencies <- list(
  "New Jersey" = list(
    name = "New Jersey Division of Consumer Affairs",
    address = "124 Halsey Street, Newark, NJ 07102",
    website = "https://www.njconsumeraffairs.gov/",
    email = "askconsumeraffairs@dca.lps.state.nj.us",
    phone = "(973) 504-6200"
  ),
  "New York" = list(
    name = "New York Department of State",
    address = "123 William Street, New York, NY 10038",
    website = "https://www.dos.ny.gov/",
    email = "licensing@dos.ny.gov",
    phone = "(518) 474-4429"
  ),
  "DC" = list(
    name = "DC Office of Consumer Protection and Licensing Administration",
    address = "1100 4th Street SW, Washington, DC 20024",
    website = "https://www.dcopla.com/",
    email = "dcopla@dc.gov",
    phone = "(202) 442-4400"
  ),
  "Virginia" = list(
    name = "Virginia Department of Professional and Occupational Regulation",
    address = "9960 Mayland Drive, Suite 400, Henrico, VA 23233",
    website = "https://www.dpor.virginia.gov/",
    email = "dporinfo@dpor.virginia.gov",
    phone = "(804) 367-8500"
  ),
  "Connecticut" = list(
    name = "Connecticut Department of Consumer Protection",
    address = "450 Columbus Boulevard, Suite 901, Hartford, CT 06103",
    website = "https://portal.ct.gov/DCP",
    email = "dcp.complaints@ct.gov",
    phone = "(860) 713-6100"
  ),
  "Maryland" = list(
    name = "Maryland Department of Labor, Licensing and Regulation (DLLR)",
    address = "500 North Calvert Street, Baltimore, MD 21202",
    website = "https://www.dllr.state.md.us/",
    email = "dllr@maryland.gov",
    phone = "(410) 230-6000"
  )
)

# Function to generate complaint letter
generate_complaint_letter <- function(state_name, state_findings, agency_info) {
  unlicensed_employees <- state_findings[state_findings$licensed == FALSE, ]
  licensed_employees <- state_findings[state_findings$licensed == TRUE, ]

  # Count violations
  total_violations <- nrow(unlicensed_employees)

  # Identify CEO and executive leadership
  ceo <- unlicensed_employees[grepl("Kettler", unlicensed_employees$employee, ignore.case = TRUE), ]
  executives <- unlicensed_employees[
    grepl("President|CEO|CFO|CIO|General Counsel|VP|SVP", unlicensed_employees$employee, ignore.case = TRUE),
  ]

  # Generate letter
  letter <- paste0(
    "COMPLAINT: Unlicensed Real Estate Operations\n",
    "Kettler Management - ", state_name, "\n\n",
    "Date: ", format(Sys.Date(), "%B %d, %Y"), "\n\n",
    "To: ", agency_info$name, "\n",
    agency_info$address, "\n",
    "Email: ", agency_info$email, "\n",
    "Phone: ", agency_info$phone, "\n\n",
    "RE: Complaint Regarding Unlicensed Real Estate Operations\n\n",
    "Dear ", agency_info$name, ",\n\n",
    "I am filing this complaint regarding systematic unlicensed real estate operations ",
    "by Kettler Management, a property management company operating in ", state_name, ".\n\n",
    "INVESTIGATION FINDINGS:\n\n",
    "This investigation has identified ", total_violations, " employees of Kettler Management ",
    "operating without required real estate licenses in ", state_name, ":\n\n"
  )

  # List unlicensed employees
  if (nrow(unlicensed_employees) > 0) {
    letter <- paste0(letter, "UNLICENSED EMPLOYEES:\n")
    for (i in 1:nrow(unlicensed_employees)) {
      emp <- unlicensed_employees[i, ]
      letter <- paste0(letter, sprintf("%d. %s - %s\n", i, emp$employee, emp$status))
    }
    letter <- paste0(letter, "\n")
  }

  # Highlight CEO violations
  if (nrow(ceo) > 0) {
    letter <- paste0(letter,
      "CRITICAL FINDING: The company owner and CEO (Robert Kettler) is operating ",
      "without a real estate license in ", state_name, ".\n\n"
    )
  }

  # Highlight executive leadership violations
  if (nrow(executives) > 0) {
    letter <- paste0(letter,
      "EXECUTIVE LEADERSHIP VIOLATIONS:\n",
      "The following executive leadership members are operating without licenses:\n"
    )
    for (i in 1:nrow(executives)) {
      emp <- executives[i, ]
      letter <- paste0(letter, sprintf("- %s\n", emp$employee))
    }
    letter <- paste0(letter, "\n")
  }

  # Front person scheme if applicable
  if (nrow(licensed_employees) > 0 && state_name != "DC") {
    letter <- paste0(letter,
      "FRONT PERSON SCHEME:\n",
      "This investigation has identified a front person scheme where only one employee ",
      "(Caitlin Skidmore) holds real estate licenses, and only in the District of Columbia. ",
      "All other employees, including the company owner and entire executive leadership team, ",
      "operate without required licenses in ", state_name, ".\n\n"
    )
  }

  # Requested action
  letter <- paste0(letter,
    "REQUESTED ACTION:\n\n",
    "I request that your agency:\n",
    "1. Investigate these unlicensed operations\n",
    "2. Verify the license status of all Kettler Management employees\n",
    "3. Take appropriate enforcement action against violators\n",
    "4. Ensure compliance with state licensing requirements\n\n",
    "EVIDENCE:\n\n",
    "Supporting evidence, including license search results and documentation, ",
    "is attached to this complaint.\n\n",
    "Thank you for your attention to this matter.\n\n",
    "Respectfully,\n",
    "[Your Name]\n",
    "[Your Contact Information]\n\n",
    "---\n",
    "Supporting Documentation:\n",
    "- License search results for ", total_violations, " employees\n",
    "- Consolidated findings report\n",
    "- Individual employee finding files\n"
  )

  return(letter)
}

# Generate complaint letters for each state
cat("Generating complaint letters...\n\n")

for (state_name in names(agencies)) {
  # Filter findings for this state
  state_findings <- findings[findings$state == state_name, ]

  cat(sprintf("Processing %s: %d findings\n", state_name, nrow(state_findings)))

  if (nrow(state_findings) > 0) {
    agency_info <- agencies[[state_name]]
    letter <- generate_complaint_letter(state_name, state_findings, agency_info)

    # Save letter
    filename <- paste0("complaint_", tolower(gsub(" ", "_", state_name)), ".txt")
    filepath <- file.path(output_dir, filename)
    writeLines(letter, filepath)

    cat(sprintf("Generated: %s\n", filepath))
    cat(sprintf("  - %d violations documented\n", nrow(state_findings[state_findings$licensed == FALSE, ])))
  } else {
    cat(sprintf("  Skipping %s: No findings\n", state_name))
  }
}

cat("\n=== Complaint Letters Generated ===\n")
cat(sprintf("Files saved to: %s\n", output_dir))
