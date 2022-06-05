# d2-memento

Curated by [/u/TheLastJoaquin](https://www.reddit.com/user/TheLastJoaquin), check out the [source spreadsheet](https://docs.google.com/spreadsheets/d/1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14) source spreadsheet!

Much thanks to all data contributors!

### Development

1. Requirements:
    - Python 3.x
    - Git Bash for Windows (or just Git on Unix)
    - Powershell v7
1. Fetching the CSV:
    1. Setup the Python virtual environment. ([?](https://docs.python.org/3/library/venv.html))
    1. Run `pip install -r ./script/requirements.txt`
    1. Run `./script/import-csv.py` to generate the data from XLSX to CSV.
1. Parsing the data:
    1. Run `./script/setup.ps1 $(which file)` to fetch the images.
        - ℹ `$(which file)` is needed for Powershell to check for the image type and validity.
1. (Optional) Optimizing the images:
    1. Get the latest [MozJPEG](https://github.com/mozilla/mozjpeg) release.
    1. Extract and get the path to `cjpeg-static.exe`.
    1. Run `./script/optimize.ps1 $path_to_cjpeg_exe`.
1. Moving the data to Jekyll:
    1. Run `./script/put-jekyll.ps1`.
    1. The weapons data will be inside `./_data/data.json`, and the images will be inside `./assets/images/`.
1. Run Jekyll
