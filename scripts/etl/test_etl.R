#!/usr/bin/env Rscript
# Test ETL Pipeline
# Simple test to verify ETL system is working

cat("========================================\n")
cat("Testing ETL Pipeline\n")
cat("========================================\n\n")

PROJECT_ROOT <- getwd()
if (basename(PROJECT_ROOT) != "kettler-data-analysis") {
  PROJECT_ROOT <- dirname(dirname(PROJECT_ROOT))
}

# Test 1: Check Python availability
cat("Test 1: Checking Python availability...\n")
python_cmd <- if (system("which python3 > /dev/null 2>&1", ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
  "python3"
} else {
  "python"
}

if (system(paste("which", python_cmd), ignore.stdout = TRUE, ignore.stderr = TRUE) == 0) {
  cat("  ✓ Python found:", python_cmd, "\n")
} else {
  cat("  ✗ Python not found\n")
  stop("Python is required for ETL pipeline")
}

# Test 2: Check Python dependencies
cat("\nTest 2: Checking Python dependencies...\n")
test_import <- function(package) {
  result <- system(
    paste(python_cmd, "-c", shQuote(paste0("import ", package))),
    ignore.stdout = TRUE,
    ignore.stderr = TRUE
  )
  return(result == 0)
}

deps <- list(
  "sentence_transformers" = "sentence-transformers",
  "faiss" = "faiss-cpu",
  "pandas" = "pandas",
  "numpy" = "numpy"
)

all_ok <- TRUE
for (module in names(deps)) {
  if (test_import(module)) {
    cat("  ✓", deps[[module]], "\n")
  } else {
    cat("  ✗", deps[[module]], "(missing)\n")
    all_ok <- FALSE
  }
}

if (!all_ok) {
  cat("\nSome dependencies are missing. Install with:\n")
  cat("  pip install -r requirements.txt\n\n")
}

# Test 3: Check ETL scripts exist
cat("\nTest 3: Checking ETL scripts...\n")
etl_dir <- file.path(PROJECT_ROOT, "scripts", "etl")
scripts <- c(
  "vector_embeddings.py",
  "etl_pipeline.py"
)

for (script in scripts) {
  script_path <- file.path(etl_dir, script)
  if (file.exists(script_path)) {
    cat("  ✓", script, "\n")
  } else {
    cat("  ✗", script, "(not found)\n")
    all_ok <- FALSE
  }
}

# Test 4: Check vector store directory
cat("\nTest 4: Checking vector store directory...\n")
vector_dir <- file.path(PROJECT_ROOT, "data", "vectors")
if (dir.exists(vector_dir)) {
  cat("  ✓ Vector store directory exists\n")
} else {
  cat("  ⚠ Vector store directory does not exist (will be created)\n")
  dir.create(vector_dir, showWarnings = FALSE, recursive = TRUE)
  cat("  ✓ Created vector store directory\n")
}

# Test 5: Try importing Python modules (if dependencies available)
if (all_ok) {
  cat("\nTest 5: Testing Python module import...\n")
  test_script <- paste0("
import sys
sys.path.insert(0, '", etl_dir, "')
try:
    from vector_embeddings import VectorEmbeddingSystem
    print('  ✓ VectorEmbeddingSystem imported successfully')
except Exception as e:
    print('  ✗ Import error:', str(e))
    sys.exit(1)
")

  result <- system(
    paste(python_cmd, "-c", shQuote(test_script)),
    intern = TRUE
  )

  if (length(result) > 0) {
    cat(paste(result, collapse = "\n"), "\n")
  }
}

cat("\n========================================\n")
if (all_ok) {
  cat("✓ All tests passed!\n")
  cat("\nYou can now run the ETL pipeline:\n")
  cat("  python3 scripts/etl/etl_pipeline.py\n")
  cat("  or\n")
  cat("  Rscript scripts/etl/init_vector_store.R\n")
} else {
  cat("⚠ Some tests failed. Please install missing dependencies.\n")
}
cat("========================================\n")
