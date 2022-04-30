#!/bin/bash

# thanks /u/TheLastJoaquin
# https://docs.google.com/spreadsheets/d/1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14/edit#gid=0

sheet='1Msr7Vdqfa6MlMXYSlERAnbTwEr4Fd7rVe2uvxaPjo14'
mkdir -p output
curl -sL -o 'output/input.csv' "https://docs.google.com/spreadsheets/d/${sheet}/export?format=csv&gid=0"
