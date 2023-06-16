# cycle_metadata_logger
Python & Tkinter GUI for recording metadata that goes alongside lyophilization runs.

## What you do:

1. Execute `main.py`
1. Fill out all the run information
1. Click "Finish"

## What you get:

A YAML file with the cycle metadata.
YAML file names are as follows:

`YYYY-MM-DD-HH_LYO_UU.yaml`
Breakdown:
- `YYYY-MM-DD-HH` is a timestamp, including hours in case multiple are run in a day
- `LYO` will be `LS`, `MFD`, or `REVO`, indicating which machine
- `UU` will be user initials

## Improvements to be made:

- Have the script copy/rename process data files, so that .csv file with process data and .yaml file with metadata have the same name.
- Include a search capability to identify historical runs with particular sets of metadata