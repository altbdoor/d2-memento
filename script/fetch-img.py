#!/usr/bin/env python

import json
import multiprocessing as mp
import os
import shutil
import sys
import requests
import filetype


DATUM_TYPE = dict[str, str]


def get_images(image_url: str, image_filename: str):
    if os.path.exists(f"{image_filename}.png"):
        print(f"(i) {image_filename}.png already downloaded")
        return
    elif os.path.exists(f"{image_filename}.jpg"):
        print(f"(i) {image_filename}.jpg already downloaded")
        return

    print(f"(i) downloading {image_url} as {image_filename}")
    with requests.get(image_url, stream=True) as res:
        with open(image_filename, "wb") as fp:
            shutil.copyfileobj(res.raw, fp)

    kind = filetype.guess(image_filename)
    if kind.mime == "image/png":
        os.rename(image_filename, f"{image_filename}.png")
    elif kind.mime == "image/jpeg":
        os.rename(image_filename, f"{image_filename}.jpg")


def main():
    os.chdir(sys.path[0])

    if not os.path.exists("images"):
        os.mkdir("images")

    with open("output/data.json", "r") as fp:
        data: list[DATUM_TYPE] = json.load(fp)

    activities = ["gambit", "trials", "nightfall"]
    process_count = min(4, mp.cpu_count() // 2)
    pool = mp.Pool(process_count)
    print(f"(i) using {process_count} processes in pool")

    for datum in data:
        for act in activities:
            image_url = datum[act]
            image_filename = f'images/{datum["slug"]}-{act}'
            pool.apply_async(get_images, args=(image_url, image_filename))

    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
