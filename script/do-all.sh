#!/bin/bash

set -o errexit

CURRENT_DIR=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
cd "$CURRENT_DIR"

python import-csv.py
python parse-csv.py
python fetch-img.py
python put-jekyll.py
