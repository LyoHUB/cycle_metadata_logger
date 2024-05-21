# cycle_metadata_logger
Python & Tkinter GUI for recording metadata that goes alongside lyophilization runs.

## What you do:

1. Find `Z:\data\metadata_writer.exe - Shortcut`
1. Execute the shortcut
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

First, make changes and upload to this repo, then pull them down to the instance of this repo on `depot\lyohub\data\cycle_metadata_logger`.

### Windows 7
1. Log onto a computer with Windows 7 (any of the ones in the lab will do, but the desk one already has everything installed)
1. Open PowerShell
1. Navigate to the repo directory on the LyoHUB remote drive
1. Run `pyinstaller metadata_writer.spec`
1. Find the executable in `depot\lyohub\data\cycle_metadata_logger\dist`, and check its file permissions: "everyone" should be able to "read and execute"

### Windows 10
1. Add a Release on GitHub (create a tag for the new version, while you're at it)
1. Give GitHub Actions a minute or two to run
1. Look at the release to find the executable
1. Download the executable and place where you want it


## Improvements to be made:

- Make the date and time a field to fill out, rather than set by the time you run it
- Add fill volume!
- At least include total solid concentration, if not something fancier

- Include a search capability to identify historical runs with particular sets of metadata
- Make separate text boxes for each formulation component & concentration, as shown in `metadata_template.yaml`

- Error if no process field is included

- Store history of user inputs to use in dropdown boxes?
    - Or: store longer list of default options in a separate text file, so that it's easy to add and modify