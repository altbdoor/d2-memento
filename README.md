# d2-memento

Curated by [/u/TheLastJoaquin](https://www.reddit.com/user/TheLastJoaquin), check out the [source spreadsheet](https://docs.google.com/spreadsheets/d/1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14) source spreadsheet!

Much thanks to all data contributors!

## Development

### Quick install

1. Requirements:
    - Python 3.x
    - Git Bash for Windows (or just Git on Unix)
1. Setup the Python virtual environment. ([?](https://docs.python.org/3/library/venv.html))
1. Run `pip install -r ./script/requirements.txt`
1. Run `cd script; bash ./do-all.sh`
1. Run Jekyll

### In detail

There are four main scripts that do all the work:

- `import-csv.py`
    - Exports the spreadsheet into XLSX, and converts the data into CSV
- `parse-csv.py`
    - Parses the CSV into a JSON
- `fetch-img.py`
    - Attempts to download the images into the local machine
- `put-jekyll.py`
    - Copies over a compiled JSON and the images into the Jekyll folders

### Images backup

Images are TAR-ed and uploaded to Backblaze.

https://f000.backblazeb2.com/file/d2-memento/images.tar
