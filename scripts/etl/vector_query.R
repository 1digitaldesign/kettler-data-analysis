#!/usr/bin/env Rscript
# Vector Query Interface for R
# Provides R interface to Python vector embedding system

library(jsonlite)
library(reticulate)

# Configuration
PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

VECTOR_DIR <- file.path(PROJECT_ROOT, "data", "vectors")

# Initialize Python environment
init_python <- function() {
  if (!py_available()) {
    cat("Python not available. Attempting to use system Python...\n")
    use_python("python3", required = FALSE)
  }

  if (!py_available()) {
    stop("Python is required for vector embeddings. Please install Python 3.")
  }

  # Source Python modules
  etl_dir <- file.path(PROJECT_ROOT, "scripts", "etl")
  py_run_string(paste0("import sys; sys.path.insert(0, '", etl_dir, "')"))

  return(TRUE)
}

# Query similar content
query_similar <- function(query_text, top_k = 10) {
  if (!exists("vector_system", envir = .GlobalEnv)) {
    init_python()

    # Import Python modules
    py_run_string("
from vector_embeddings import VectorEmbeddingSystem
vector_system = VectorEmbeddingSystem()
")
  }

  # Query
  py_run_string(paste0("
results = vector_system.search_similar('", query_text, "', top_k=", top_k, ")
"))

  results <- py$results

  if (length(results) == 0) {
    return(data.frame())
  }

  # Convert to data frame
  df <- data.frame(
    content_id = sapply(results, function(x) x$content_id),
    similarity = sapply(results, function(x) x$similarity),
    distance = sapply(results, function(x) x$distance),
    source = sapply(results, function(x) x$source),
    text_preview = sapply(results, function(x) substr(x$text, 1, 200)),
    stringsAsFactors = FALSE
  )

  return(df)
}

# Run ETL pipeline
run_etl_pipeline <- function(force = FALSE) {
  init_python()

  py_run_string("
from etl_pipeline import ETLPipeline
pipeline = ETLPipeline()
results = pipeline.run_full_pipeline(force=", ifelse(force, "True", "False"), ")
")

  results <- py$results

  return(results)
}

# Get vector store statistics
get_vector_stats <- function() {
  if (!exists("vector_system", envir = .GlobalEnv)) {
    init_python()

    py_run_string("
from vector_embeddings import VectorEmbeddingSystem
vector_system = VectorEmbeddingSystem()
")
  }

  py_run_string("stats = vector_system.get_stats()")

  return(py$stats)
}

# Main function for interactive use
if (!interactive()) {
  args <- commandArgs(trailingOnly = TRUE)

  if (length(args) == 0) {
    cat("Usage: Rscript vector_query.R <command> [args]\n")
    cat("Commands:\n")
    cat("  query <text> [top_k]  - Query similar content\n")
    cat("  etl [force]           - Run ETL pipeline\n")
    cat("  stats                  - Get vector store statistics\n")
  } else if (args[1] == "query" && length(args) >= 2) {
    query_text <- paste(args[-1], collapse = " ")
    top_k <- if (length(args) >= 3) as.integer(args[3]) else 10
    results <- query_similar(query_text, top_k)
    print(results)
  } else if (args[1] == "etl") {
    force <- if (length(args) >= 2 && args[2] == "force") TRUE else FALSE
    results <- run_etl_pipeline(force)
    cat("ETL pipeline complete.\n")
  } else if (args[1] == "stats") {
    stats <- get_vector_stats()
    print(stats)
  }
}
