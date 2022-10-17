#!/bin/bash

set -o errexit

python import-csv.py
python parse-csv.py
python fetch-img.py
python put-jekyll.py
