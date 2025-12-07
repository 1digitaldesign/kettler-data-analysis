#!/usr/bin/env Rscript
# R API Server
# REST API for R analysis services

library(plumber)
library(jsonlite)

# Configuration
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

# Source analysis functions
source(file.path(PROJECT_ROOT, "analyze_skidmore_connections.R"))
source(file.path(PROJECT_ROOT, "scripts", "analysis", "analyze_all_evidence.R"))

# Create plumber API
api <- plumber::plumber$new()

# Health check
api$handle("GET", "/health", function() {
  list(status = "healthy", service = "r-analysis")
})

# Analyze connections
api$handle("POST", "/api/v1/analyze/connections", function(req) {
  tryCatch({
    skidmore_data <- load_skidmore_data()
    dpor_results <- load_dpor_results()
    connections <- find_skidmore_connections(dpor_results, skidmore_data)

    list(
      status = "success",
      connections_count = nrow(connections),
      connections = connections
    )
  }, error = function(e) {
    list(status = "error", error = e$message)
  })
})

# Analyze evidence
api$handle("POST", "/api/v1/analyze/evidence", function(req) {
  tryCatch({
    evidence <- load_all_evidence()
    entities <- extract_all_entities(evidence)

    list(
      status = "success",
      entities = entities
    )
  }, error = function(e) {
    list(status = "error", error = e$message)
  })
})

# Run analysis
api$run(host = "0.0.0.0", port = 8001)
