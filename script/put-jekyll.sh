#!/bin/bash

CURRENT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
cd "$CURRENT_DIR"

cp output/data.json ../_data/
cp images/* ../assets/images/
