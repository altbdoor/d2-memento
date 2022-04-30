#!/bin/bash

CURRENT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
cd "$CURRENT_DIR"

mkdir -p images

while IFS=, read -r filename url; do
    trimmed_url=$(echo "${url}" | sed -e 's/\ *$//g')
    curl -sL -o "images/${filename}.jpg" "${trimmed_url}"

    if file "images/${filename}.jpg" | grep 'PNG image data'; then
        mv "images/${filename}.jpg" "images/${filename}.png"
        ffmpeg -hide_banner -i "images/${filename}.png" "images/${filename}.jpg"
        rm "images/${filename}.png"
    fi

    echo "downloaded ${filename}"
done < output/files.csv
