#!/usr/bin/env python

import csv
import os
import random
import re
import sys
from urllib.request import urlopen, Request


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


def get_url_request(url: str) -> Request:
    return Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/79.0.3945.{random.randint(0, 9999)} Safari/537.{random.randint(0, 99)}"
            )
        },
    )


os.chdir(sys.path[0])
data: list[dict[str, str]] = []

with open("output/input.csv", "r") as fp:
    reader = csv.DictReader(fp, fieldnames=all_headers)
    for row in reader:
        if not row.get("season").lower().strip().startswith("season of"):
            continue

        datum: dict[str, str] = {
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

# https://www.geeksforgeeks.org/parallel-processing-in-python/
# for datum in data:
#     for act in activity_headers:
#         image_url = datum[act]

#         if "imgur.com/a/" in image_url:
#             image_url = "/".join([*image_url.split("/"), "layout", "blog"])
#             with urlopen(get_url_request(image_url)) as res:
#                 html_str: str = res.read().decode("utf8")
#                 imgur_links = re.findall(r'"https:\/\/i\.imgur\.com\/.+?"', html_str)

#             if len(imgur_links) > 0:
#                 image_url = imgur_links[0].replace('"', "")
#             else:
#                 print(f"unable to find image for {image_url}")

#         elif imgur_id := re.match(r"^https:\/\/imgur\.com\/(\w+)$", image_url):
#             image_url = f"https://i.imgur.com/{imgur_id.group(1)}.jpg"

#         elif "drive.google.com" in image_url:
#             drive_id = image_url.split("/")[5]
#             image_url = f"https://docs.google.com/uc?export=download&id={drive_id}"

#         datum[act] = image_url

if not os.path.isdir("images"):
    os.mkdir("images")

for datum in data:
    for act in activity_headers:
        image_url = datum[act]
        image_filename = f"{datum['slug']}-{act}"
        print(datum)
