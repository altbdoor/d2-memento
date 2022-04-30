#!/usr/bin/env python

import csv
import json
import os
import re
import urllib.request

if not os.path.exists('output'):
    os.mkdir('output')

data = []

with open('output/input.csv') as fp:
    csv_reader = csv.reader(fp)
    next(csv_reader)

    for row in csv_reader:
        stripped_row = [i.strip() for i in row]

        row_data = {
            "group": stripped_row[0],
            "weapon": stripped_row[1],
            "slug": re.sub(r'[^A-z0-9]', '', stripped_row[1]).lower(),
            "gambit": stripped_row[2],
            "trials": stripped_row[4],
            "nightfall": stripped_row[6],
        }

        if row_data['group'] == '':
            row_data['group'] = data[-1]['group']

        if row_data['gambit'] and row_data['trials'] and row_data['nightfall']:
            data.append(row_data)
        else:
            break

with open('output/data.json', 'w') as fp:
    json.dump(data, fp, indent=4)


with open('output/files.csv', 'w', newline='') as fp:
    csv_writer = csv.writer(fp)
    activities = ('gambit', 'trials', 'nightfall', )

    for datum in data:
        for act in activities:
            final_img: str = datum[act]

            if 'imgur.com/a/' in final_img:
                with urllib.request.urlopen(final_img) as res:
                    res_body = res.read().decode('utf-8')
                    link_match = re.search(r'"(https://i.imgur.com/.+?)"', res_body)

                    if link_match:
                        final_img = link_match.group(1)
                    else:
                        raise Exception('unable to deduce imgur image')
            elif 'drive.google.com' in final_img:
                drive_id = final_img.split('/')[5]
                final_img = f'https://docs.google.com/uc?export=download&id={drive_id}'

            filename = f"{datum['slug']}-{act}"
            csv_writer.writerow([filename, final_img])
