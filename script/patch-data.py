#!/usr/bin/env python

import json
import os


with open('output/data.json', 'r') as fp:
    data = json.load(fp)

patched_data = []
activities = ('gambit', 'trials', 'nightfall', )
image_files = os.listdir('images')

for datum in data:
    clone_datum = {
        "group": datum['group'],
        "weapon": datum['weapon'],
        "slug": datum['slug'],
        "gambit": '',
        "trials": '',
        "nightfall": '',
    }

    for act in activities:
        image_name = f'{datum["slug"]}-{act}'
        for filename in image_files:
            if filename.startswith(image_name):
                clone_datum[act] = filename
                break

    patched_data.append(clone_datum)

with open('output/data.json', 'w') as fp:
    json.dump(patched_data, fp, indent=4)
