#!/usr/bin/env Rscript
# Comprehensive DPOR License Search Script
# Searches DPOR websites across all 50 states for firm and individual license information

library(httr)
library(rvest)
library(dplyr)
library(jsonlite)
library(stringr)
library(data.table)

# Configuration
DATA_DIR <- "data/raw"
LOG_FILE <- "dpor_search_log.txt"
RATE_LIMIT_DELAY <- 2  # seconds between requests

# Initialize log file
if (!file.exists(LOG_FILE)) {
  file.create(LOG_FILE)
}

# Logging function
log_message <- function(message) {
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  log_entry <- paste0("[", timestamp, "] ", message, "\n")
  cat(log_entry)
  cat(log_entry, file = LOG_FILE, append = TRUE)
}

# Load state registry
load_state_registry <- function() {
  registry_file <- "state_dpor_registry.csv"
  if (!file.exists(registry_file)) {
    stop(paste("Cannot find state_dpor_registry.csv in current directory:", getwd()))
  }
  registry <- read.csv(registry_file, stringsAsFactors = FALSE)
  return(registry)
}

# Standardize firm name variations
standardize_firm_name <- function(name) {
  # Remove common suffixes
  name <- name %>%
    str_remove_all("\\s+(Inc|LLC|Corporation|Corp|Company|Co|Ltd|Limited)$") %>%
    str_trim()

  # Remove punctuation
  name <- str_replace_all(name, "[[:punct:]]", " ")

  # Normalize whitespace
  name <- str_replace_all(name, "\\s+", " ") %>%
    str_trim()

  return(name)
}

# Generate name variations for search
generate_name_variations <- function(name) {
  base_name <- standardize_firm_name(name)
  variations <- c(
    name,  # Original
    base_name,  # Standardized
    paste0(base_name, " Inc"),
    paste0(base_name, " LLC"),
    paste0(base_name, " Corporation"),
    paste0(base_name, " Company")
  )
  return(unique(variations))
}

# Generate Skidmore name variations
generate_skidmore_variations <- function() {
  return(c(
    "Caitlin Skidmore",
    "Caitlin Marie Skidmore",
    "SKIDMORE, CAITLIN MARIE",
    "SKIDMORE, CAITLIN",
    "Skidmore, Caitlin",
    "Skidmore, Caitlin Marie"
  ))
}

# Generic form-based search function
search_form_based <- function(url, search_params, state_code) {
  tryCatch({
    log_message(paste("Attempting form-based search for", state_code))

    # Attempt POST request
    response <- POST(
      url,
      body = search_params,
      encode = "form",
      add_headers(
        "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
      ),
      timeout(30)
    )

    if (status_code(response) == 200) {
      return(content(response, "text"))
    } else {
      log_message(paste("HTTP error", status_code(response), "for", state_code))
      return(NULL)
    }
  }, error = function(e) {
    log_message(paste("Error in form-based search for", state_code, ":", e$message))
    return(NULL)
  })
}

# Generic query-based search function
search_query_based <- function(base_url, search_params, state_code) {
  tryCatch({
    log_message(paste("Attempting query-based search for", state_code))

    # Build query string
    query_string <- paste(names(search_params), search_params, sep = "=", collapse = "&")
    full_url <- paste0(base_url, "?", query_string)

    response <- GET(
      full_url,
      add_headers(
        "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
      ),
      timeout(30)
    )

    if (status_code(response) == 200) {
      return(content(response, "text"))
    } else {
      log_message(paste("HTTP error", status_code(response), "for", state_code))
      return(NULL)
    }
  }, error = function(e) {
    log_message(paste("Error in query-based search for", state_code, ":", e$message))
    return(NULL)
  })
}

# Parse HTML results (generic parser - state-specific parsers will override)
parse_dpor_result <- function(html_content, state_code, search_term) {
  tryCatch({
    if (is.null(html_content) || html_content == "") {
      return(data.frame())
    }

    html <- read_html(html_content)

    # Generic parsing - extract tables and lists
    # State-specific implementations should override this
    results <- data.frame(
      state = character(),
      search_term = character(),
      license_number = character(),
      name = character(),
      address = character(),
      license_type = character(),
      expiration_date = character(),
      status = character(),
      stringsAsFactors = FALSE
    )

    # Try to find tables
    tables <- html %>% html_nodes("table")
    if (length(tables) > 0) {
      # Attempt to parse first table
      try({
        table_data <- tables[[1]] %>% html_table(fill = TRUE)
        if (nrow(table_data) > 0) {
          log_message(paste("Found", nrow(table_data), "results in table for", state_code))
        }
      }, silent = TRUE)
    }

    return(results)
  }, error = function(e) {
    log_message(paste("Error parsing results for", state_code, ":", e$message))
    return(data.frame())
  })
}

# Search single state for firm
search_state_dpor <- function(state_info, firm_name, search_type = "firm") {
  state_code <- state_info$state_code
  url <- state_info$license_lookup_url
  search_type_site <- state_info$search_type

  log_message(paste("Searching", state_code, "for", firm_name))

  # Generate search parameters based on site type
  if (search_type_site == "query_based") {
    search_params <- list(
      name = firm_name,
      lic_name = firm_name
    )
    html_content <- search_query_based(url, search_params, state_code)
  } else {
    # Form-based search
    search_params <- list(
      name = firm_name,
      searchTerm = firm_name,
      companyName = firm_name
    )
    html_content <- search_form_based(url, search_params, state_code)
  }

  # Parse results
  if (!is.null(html_content)) {
    results <- parse_dpor_result(html_content, state_code, firm_name)
    if (nrow(results) > 0) {
      results$state <- state_code
      results$search_term <- firm_name
      results$search_type <- search_type
    }
    return(results)
  }

  return(data.frame())
}

# Search firm across all states
search_firm_all_states <- function(firm_name, registry = NULL) {
  if (is.null(registry)) {
    registry <- load_state_registry()
  }

  all_results <- list()
  name_variations <- generate_name_variations(firm_name)

  log_message(paste("Searching all states for firm:", firm_name))
  log_message(paste("Using", length(name_variations), "name variations"))

  if (nrow(registry) == 0) {
    log_message("Warning: Registry is empty, cannot search")
    return(data.frame())
  }

  for (i in 1:nrow(registry)) {
    state_info <- registry[i, ]

    # Try each name variation
    for (variation in name_variations) {
      results <- search_state_dpor(state_info, variation, "firm")

      if (nrow(results) > 0) {
        all_results[[length(all_results) + 1]] <- results
        log_message(paste("Found", nrow(results), "results for", variation, "in", state_info$state_code))
      }

      # Rate limiting
      Sys.sleep(RATE_LIMIT_DELAY)
    }
  }

  if (length(all_results) > 0) {
    combined_results <- bind_rows(all_results)
    return(combined_results)
  }

  return(data.frame())
}

# Search for Caitlin Skidmore across all states
search_skidmore_all_states <- function(registry = NULL) {
  if (is.null(registry)) {
    registry <- load_state_registry()
  }

  all_results <- list()
  name_variations <- generate_skidmore_variations()

  log_message("Searching all states for Caitlin Skidmore")
  log_message(paste("Using", length(name_variations), "name variations"))

  if (nrow(registry) == 0) {
    log_message("Warning: Registry is empty, cannot search")
    return(data.frame())
  }

  for (i in 1:nrow(registry)) {
    state_info <- registry[i, ]

    # Try each name variation
    for (variation in name_variations) {
      results <- search_state_dpor(state_info, variation, "individual")

      if (nrow(results) > 0) {
        all_results[[length(all_results) + 1]] <- results
        log_message(paste("Found", nrow(results), "results for", variation, "in", state_info$state_code))
      }

      # Rate limiting
      Sys.sleep(RATE_LIMIT_DELAY)
    }
  }

  if (length(all_results) > 0) {
    combined_results <- bind_rows(all_results)
    return(combined_results)
  }

  return(data.frame())
}

# Save results to file
save_results <- function(results, filename) {
  if (nrow(results) > 0) {
    filepath <- file.path(DATA_DIR, filename)
    write.csv(results, filepath, row.names = FALSE)
    log_message(paste("Saved", nrow(results), "results to", filepath))
    return(TRUE)
  } else {
    log_message(paste("No results to save for", filename))
    return(FALSE)
  }
}

# Main execution function
main <- function() {
  log_message("Starting comprehensive DPOR search")

  # Load state registry
  registry <- load_state_registry()
  log_message(paste("Loaded", nrow(registry), "states from registry"))

  # Define firms to search
  firms <- c(
    "Bell Partners Inc",
    "Bozzuto Management Company",
    "Cortland Management LLC",
    "Gables Residential Services Inc",
    "Gateway Management Company LLC",
    "McCormack Baron Management Inc",
    "Burlington Capital Properties LLC",
    "Bainbridge Mid Atlantic Management LLC",
    "Capreit Residential Management LLC",
    "Edgewood Management Corporation"
  )

  # Search all firms
  log_message("=== Searching for firms ===")
  all_firm_results <- list()

  for (firm in firms) {
    log_message(paste("\n--- Searching for:", firm, "---"))
    firm_results <- search_firm_all_states(firm, registry)

    if (nrow(firm_results) > 0) {
      all_firm_results[[length(all_firm_results) + 1]] <- firm_results
      save_results(firm_results, paste0("firm_", gsub("[^A-Za-z0-9]", "_", firm), "_results.csv"))
    }
  }

  # Combine and save all firm results
  if (length(all_firm_results) > 0) {
    combined_firm_results <- bind_rows(all_firm_results)
    save_results(combined_firm_results, "dpor_all_firms_results.csv")
  }

  # Search for Caitlin Skidmore
  log_message("\n=== Searching for Caitlin Skidmore ===")
  skidmore_results <- search_skidmore_all_states(registry)

  if (nrow(skidmore_results) > 0) {
    save_results(skidmore_results, "dpor_skidmore_results.csv")
  }

  log_message("\n=== Search complete ===")
}

# Run if executed as script
if (!interactive()) {
  main()
}
