#!/usr/bin/env python

import csv
import json
import os
import re
import sys
import requests


DATUM_TYPE = dict[str, str]


def main():
    credit_headers = ["credit_gambit", "credit_trials", "credit_nightfall"]
    all_headers = [
        "season",
        "group",
        "weapon",
        "gambit",
        "spacer1",
        "trials",
        "spacer2",
        "nightfall",
        *credit_headers,
    ]
    activity_headers = [header.replace("credit_", "") for header in credit_headers]

    os.chdir(sys.path[0])
    data: list[DATUM_TYPE] = []

    with open("output/input.csv", "r") as fp:
        reader = csv.DictReader(fp, fieldnames=all_headers)
        for row in reader:
            if not row.get("season").lower().strip().startswith("season of"):
                continue

            datum: DATUM_TYPE = {
                "season": row.get("season", "").strip(),
                "group": row.get("group", "").strip(),
                "weapon": row.get("weapon", "").strip(),
                "gambit": row.get("gambit", "").strip(),
                "trials": row.get("trials", "").strip(),
                "nightfall": row.get("nightfall", "").strip(),
                "slug": "",
                "credit_gambit": row.get("credit_gambit", "").strip(),
                "credit_trials": row.get("credit_trials", "").strip(),
                "credit_nightfall": row.get("credit_nightfall", "").strip(),
            }

            for header in activity_headers:
                if not datum[header].startswith("http"):
                    datum[header] = ""

            # temp patch for future credits
            for header in credit_headers:
                if "add these later" in datum[header]:
                    datum[header] = ""
                elif "This person offered" in datum[header]:
                    datum[header] = ""

            datum["slug"] = re.sub(r"[^a-z0-9]", "", datum["weapon"].lower())
            data.append(datum)

    for datum in data:
        for act in activity_headers:
            image_url = datum[act]
            print(f'(i) processing {datum["weapon"]}, {act}, {image_url}')

            if "imgur.com/a/" in image_url:
                image_url = "/".join([*image_url.split("/"), "layout", "blog"])

                with requests.get(image_url) as res:
                    imgur_links = re.findall(
                        r'"https:\/\/i\.imgur\.com\/.+?"', res.text
                    )

                    if len(imgur_links) > 0:
                        image_url = imgur_links[0].replace('"', "")
                    else:
                        print(f"(!) unable to find image for {image_url}")

            elif imgur_id := re.match(r"^https:\/\/imgur\.com\/(\w+)$", image_url):
                image_url = f"https://i.imgur.com/{imgur_id.group(1)}.jpg"

            elif "drive.google.com" in image_url:
                drive_id = image_url.split("/")[5]
                image_url = f"https://docs.google.com/uc?export=download&id={drive_id}"

            datum[act] = image_url

    with open("output/csv-parsed.json", "w") as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    main()
