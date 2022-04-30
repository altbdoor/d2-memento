#!/bin/bash

mkdir -p images

while IFS=, read -r filename url; do
    trimmed_url=$(echo "${url}" | sed -e 's/\ *$//g')
    curl -sL -o "images/${filename}.jpg" "${trimmed_url}"

    if file "images/${filename}.jpg" | grep 'PNG image data'; then
        mv "images/${filename}.jpg" "images/${filename}.png"
    fi

    echo "downloaded ${filename}"
done < output/files.csv
