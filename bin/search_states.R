#!/usr/bin/env Rscript
# Multi-State DPOR Search Wrapper
# Orchestrates searches across all 50 states

# Load path utilities
source(file.path(dirname(normalizePath(commandArgs()[4])), "load_paths.R"))

# Source search scripts
source_script("search/search_dpor_comprehensive.R")
source_script("search/search_virginia_dpor.R")

# Load state registry
registry <- read.csv(STATE_REGISTRY_FILE, stringsAsFactors = FALSE)

# Define firms to search
FIRMS <- c(
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

# Search all firms across all states
search_all_firms_multi_state <- function() {
  log_message("=== Starting multi-state firm search ===")

  all_results <- list()

  for (firm in FIRMS) {
    log_message(paste("\n--- Searching for firm:", firm, "---"))

    # Use Virginia-specific search for Virginia
    va_results <- search_firm_virginia(firm)
    if (nrow(va_results) > 0) {
      all_results[[length(all_results) + 1]] <- va_results
      log_message(paste("Found", nrow(va_results), "results in Virginia"))
    }

    # Search other states using generic framework
    other_states <- registry %>% filter(state_code != "VA")

    if (nrow(other_states) > 0) {
      for (i in 1:nrow(other_states)) {
      state_info <- other_states[i, ]
      log_message(paste("Searching", state_info$state_code, "for", firm))

      results <- search_state_dpor(state_info, firm, "firm")

      if (nrow(results) > 0) {
        all_results[[length(all_results) + 1]] <- results
        log_message(paste("Found", nrow(results), "results in", state_info$state_code))
      }

      # Rate limiting
      Sys.sleep(RATE_LIMIT_DELAY)
      }
    }

    # Save individual firm results
    if (length(all_results) > 0) {
      firm_all <- bind_rows(all_results)
      firm_filename <- paste0("firm_", gsub("[^A-Za-z0-9]", "_", firm), "_all_states.csv")
      save_results(firm_all, firm_filename)
      all_results <- list()  # Reset for next firm
    }
  }

  log_message("=== Multi-state firm search complete ===")
}

# Search for Caitlin Skidmore across all states
search_skidmore_multi_state <- function() {
  log_message("=== Starting multi-state Skidmore search ===")

  all_results <- list()

  # Use Virginia-specific search for Virginia
  va_results <- search_skidmore_virginia()
  if (nrow(va_results) > 0) {
    all_results[[length(all_results) + 1]] <- va_results
    log_message(paste("Found", nrow(va_results), "results in Virginia"))
  }

  # Search other states
  other_states <- registry %>% filter(state_code != "VA")
  name_variations <- generate_skidmore_variations()

  if (nrow(other_states) > 0) {
    for (i in 1:nrow(other_states)) {
    state_info <- other_states[i, ]

    for (variation in name_variations) {
      log_message(paste("Searching", state_info$state_code, "for", variation))

      results <- search_state_dpor(state_info, variation, "individual")

      if (nrow(results) > 0) {
        all_results[[length(all_results) + 1]] <- results
        log_message(paste("Found", nrow(results), "results in", state_info$state_code))
      }

      # Rate limiting
      Sys.sleep(RATE_LIMIT_DELAY)
      }
    }
  }

  # Combine and save all Skidmore results
  if (length(all_results) > 0) {
    combined_results <- bind_rows(all_results)
    save_results(combined_results, "dpor_skidmore_all_states.csv")
    log_message(paste("Total Skidmore results:", nrow(combined_results)))
  }

  log_message("=== Multi-state Skidmore search complete ===")
}

# Main execution
main_multi_state <- function() {
  log_message("Starting multi-state DPOR search")
  log_message(paste("Searching", length(FIRMS), "firms across", nrow(registry), "states"))

  # Search all firms
  search_all_firms_multi_state()

  # Search for Skidmore
  search_skidmore_multi_state()

  log_message("=== All searches complete ===")
}

# Run if executed as script
if (!interactive()) {
  main_multi_state()
}
