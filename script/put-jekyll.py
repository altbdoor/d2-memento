#!/usr/bin/env python


import os
import shutil
import sys


def main():
    os.chdir(sys.path[0])
    shutil.copy2("output/data.json", "../_data/")

    for image in os.listdir("../assets/images"):
        image_path = os.path.join("../assets/images", image)
        os.remove(image_path)

    for image in os.listdir("images"):
        image_path = os.path.join("images", image)
        shutil.copy2(image_path, "../assets/images")


if __name__ == "__main__":
    main()
