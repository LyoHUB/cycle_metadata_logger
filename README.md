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

## How to improve this system:

1. Make changes and upload to the repo on GitHub
1. Once changes are working, add a Release on GitHub (create a tag for the new version, while you're at it)
1. Give GitHub Actions a minute or two to run
1. Look at the release to find the executable
1. Download the executable and place in `Z:\\data\cycle_metadata_logger\dist`

## Improvements to be made:

- Have the script copy/rename process data files, so that .csv file with process data and .yaml file with metadata have the same name.
- Include a search capability to identify historical runs with particular sets of metadata
- Make separate text boxes for each formulation component & concentration, as shown in `metadata_template.yaml`