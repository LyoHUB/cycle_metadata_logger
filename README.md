# cycle_metadata_logger
Python & Tkinter GUI for recording metadata that goes alongside lyophilization runs.
An initial draft was authored by Petr Kazarin and ChatGPT; expanded significantly and improved by Isaac S Wheeler.

## What you do:

1. Find `Z:\data\metadata_writer.exe - Shortcut`
1. Execute the shortcut
1. Fill out all the run information
1. Click "Finish"

## What you get:

A YAML file with the cycle metadata, placed in a folder with any chosen process data files.
The given file names are as follows:

`YYYY-MM-DD-HH_LYO_UU.yaml`
Breakdown:
- `YYYY-MM-DD-HH` is a timestamp, including hours in case multiple are run in a day
- `LYO` will be e.g. `LS`, `LC`, `MFD`, or `REVO`, indicating which machine was used
- `UU` will be user initials

If only one process file is included, it will be named as `YYYY-MM-DD-HH_LYO_UU.csv`;
multiple will be named `YYYY-MM-DD-HH_LYO_UU_1.csv`, `YYYY-MM-DD-HH_LYO_UU_2.csv`

## Default options
For the early life of this system, the choices of lyophilizer, formulation, project, and container size had defaults hardcoded into the program. The directory in which files would be saved was likewise hardcoded.
As of 0.2, however, if the executable finds a file called `persistent_options.yaml`, it will read in that file.
You can open that file and add or remove items from that list to add or remove items from the dropdown boxes, as suits your convenience.

## How to improve this system:

Assuming you are a future LyoHUB user: make changes and upload to this repo, 
then pull them down to the instance of this repo on `depot\lyohub\data\cycle_metadata_logger`.
Then, follow an appropriate set of instructions below.
Be warned that if you use a `git pull` to copy the files, this will likely override the `persistent_options.yaml` which is currently there. It would be prudent to make a copy of that file elsewhere, update, then put the desired version back in.


### Windows 7 install
1. Log onto a computer with Windows 7 (any of the ones in the lab could be used, but the FDM computer already has everything necessary installed)
1. Open PowerShell
1. In PowerShell: Navigate to the repo directory on the LyoHUB remote drive
1. In PowerShell: Update the repo to match GitHub, e.g. with `git pull`
1. In PowerShell: Run `pyinstaller metadata_writer.spec`
1. In a regular file explorer window, find the executable in `depot\lyohub\data\cycle_metadata_logger\dist`, and check its file permissions: "everyone" should be able to "read and execute" (this is not the default)

### Windows 10
1. Add a Release on GitHub (create a tag for the new version, while you're at it)
1. Give GitHub Actions a minute or two to run
1. Look at the release to find the executable
1. Download the executable and place where you want it

## Improvements to be made:

- Add a search capability to identify historical runs with particular sets of metadata, e.g. for a specific project or using a particular formulation.
