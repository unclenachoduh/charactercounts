# Character Counts

A quick script for counting the characters in the translateable text of Mozilla .po files.

By: Uncle Nacho, duh.

## Running the script

From `root`:

`python3 counts.py <source_folder>`

`<source_folder>` should be a directory with at least one .po-formatted file. 

The script will output characters counts for each file individually and for all files together in the `results` folder. 

The script also outputs the raw and human-readable versions of the translateable text in the `search_text` and `readable_text` folders respectively.