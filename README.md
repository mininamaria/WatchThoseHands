# WatchThoseHands
This repo contains all the code I use in my coursework, investigating whether listeners attend to speakers' gestures or not

NB: In `.txt` files, do not enter any redundant spaces, please.

## Repository overview

### WTH Analysis

`WatchThoseHandsAnalysis` is basically a complete R project that is designed for preprocessing and analyzing all the data. All the other files are helpful add-ons that were for whatever reason created separately and written in Python.

- `.../data_prepped/`: here you can find CSV files with joined tables. The most useful yet are:
  - `all_aoi_fixations_metadata.csv` that, beside IDs, contains AOI name, fixation duration, wearer and view;
  - `gesture_summary.csv` and `summary_aoi_gesture_view`;
  - `respondents.csv`, a bit truncated version of metadata, as it contains only the information that can be used in statistical analysis.
- `.../data_raw/` does not contain all the data, it is loaded here just for demonstration purposes (maybe later I'll add the rest).
