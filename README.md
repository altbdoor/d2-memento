# d2-memento

Data curated by [/u/TheLastJoaquin](https://www.reddit.com/user/TheLastJoaquin), much thanks to the [Reddit post](https://www.reddit.com/r/DestinyTheGame/comments/twzs6e/a_few_days_ago_i_started_cataloguing_the_memento/) and data contributors!

For the original source data, please visit https://docs.google.com/spreadsheets/d/1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14/edit#gid=0

### Development

1. Requirements:
    - Git Bash for Windows (or just Git on Unix)
    - Powershell v7
1. Fetching the data:
    1. Run `./script/setup.ps1 $(which file)` to generate the data, and fetch the images.
        - ℹ `$(which file)` is needed for Powershell to check for the image type and validity.
1. (Optional) Optimizing the images:
    1. Get the latest [MozJPEG](https://github.com/mozilla/mozjpeg) release.
    1. Extract and get the path to `cjpeg-static.exe`.
    1. Run `./script/optimize.ps1 $path_to_cjpeg_exe`.
1. Moving the data to Jekyll:
    1. Run `./script/put-jekyll.ps1`.
    1. The weapons data will be inside `./_data/data.json`, and the images will be inside `./assets/images/`.
1. Run Jekyll
