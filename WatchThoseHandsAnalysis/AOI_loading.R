library(tidyverse)

# Define data folder
data_dir <- "data_raw/"

gesture_dirs <- list.dirs(data_dir, recursive = FALSE)

# Function to load and tag fixations with gesture info
load_fixations <- function(folder_path) {
  folder_name <- basename(folder_path)
  file_path <- file.path(folder_path, "aoi_fixations.csv")
  
  if (!file.exists(file_path)) {
    warning(paste("Missing file:", file_path))
    return(NULL)
  }
  
  # Read file safely
  df <- tryCatch(read_csv(file_path, show_col_types = FALSE), 
                 error = function(e) {
                   warning(paste("Failed to read:", file_path, "|", e$message))
                   return(NULL)
                 })
  
  # Check if "fixation status" exists
 # if (is.null(df) || !"fixation status" %in% names(df)) {
 #   warning(paste("Skipping invalid or malformed file:", file_path))
 #   return(NULL)
 # }
  
  # Standardize type
  #df <- df |>
   # mutate(`fixation status` = as.character(`fixation status`))
  
  # Extract gesture metadata
  #aoi_id,aoi_name,section_id,recording_id,fixation_id,fixation_duration.ms
  print(colnames(df))
  df <- df |> 
    rename(
      aoi_id = 'aoi id',
      aoi_name = 'aoi name',
      section_id = 'section id',
      recording_id = 'recording id',
      fixation_id = 'fixation id',
      fixation_duration.ms = 'fixation duration [ms]'
    ) |>
    mutate(
      fixation_id = as.character(fixation_id),
      fixation_duration.ms = as.character(fixation_duration.ms)
    )
  df$folder <- folder_name
  
  return(df)
}

# Load all data
all_aoi_fixations <- map_df(gesture_dirs, load_fixations)
View(all_aoi_fixations)
write.csv(all_aoi_fixations, "data_prepped/all_aoi_fixations.csv")


# Load recording metadata
recording_info <- read_csv("data_prepped/recording_id_name_wearer.csv", show_col_types = FALSE) |>
  mutate(
    gesture_id = str_extract(name, "^\\d{2}"),
    view = str_extract(name, "view_\\d"),
  )

# Explicitly specify different column names in each data frame
merged_aoi_df <- left_join(
  all_aoi_fixations,
  recording_info,
  by = c("recording_id" = "recording_id")  # fixations$recording_id = recording_info$recording_id
)
# Clear existing values in gesture_id and replace with first two characters from folder
merged_aoi_df$gesture_id <- substr(merged_aoi_df$folder, 1, 2)
merged_aoi_df$view[is.na(merged_aoi_df$view)] <- "view_1"
print(colnames(merged_aoi_df))
print(summary(merged_aoi_df))
write.csv(merged_aoi_df, "data_prepped/all_aoi_fixations_metadata.csv")

library(dplyr)

# Convert fixation_duration.ms to numeric (coerce non-numeric to NA)
merged_aoi_df <- merged_aoi_df |>
  mutate(fixation_duration.ms = as.numeric(fixation_duration.ms))

# Now summarize (with NA handling)
summary_merged_aoi_df <- merged_aoi_df |>
  group_by(gesture_id, aoi_name, view) |>
  summarise(
    count = n(),
    mean_fixation_duration = mean(fixation_duration.ms, na.rm = TRUE),
    median_fixation_duration = median(fixation_duration.ms, na.rm = TRUE),
    sd_fixation_duration = sd(fixation_duration.ms, na.rm = TRUE),
    .groups = "drop"
  )

# View results
print(summary_merged_aoi_df)
write.csv(summary_merged_aoi_df, "data_prepped/summary_aoi_gesture_view.csv")

