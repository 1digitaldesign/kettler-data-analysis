#!/usr/bin/env Rscript
# Dataframe Helper Functions
# Common validation and access patterns for dataframes

# Check if dataframe is valid and has rows
is_valid_df <- function(df) {
  !is.null(df) && is.data.frame(df) && nrow(df) > 0
}

# Check if dataframe has required columns
has_columns <- function(df, cols) {
  if (!is_valid_df(df)) return(FALSE)
  all(cols %in% names(df))
}

# Safe column access with default value
safe_get <- function(df, col, default = NA) {
  if (has_columns(df, col) && nrow(df) > 0) {
    df[[col]][1]
  } else {
    default
  }
}

# Safe dataframe filter - returns empty dataframe if invalid
safe_filter <- function(df, ...) {
  if (!is_valid_df(df)) {
    return(data.frame())
  }
  tryCatch({
    dplyr::filter(df, ...)
  }, error = function(e) {
    data.frame()
  })
}

# Safe group_by and summarise
safe_group_summarise <- function(df, group_cols, ...) {
  if (!has_columns(df, group_cols)) {
    return(data.frame())
  }
  tryCatch({
    df %>%
      dplyr::group_by(!!!rlang::syms(group_cols)) %>%
      dplyr::summarise(...)
  }, error = function(e) {
    data.frame()
  })
}
