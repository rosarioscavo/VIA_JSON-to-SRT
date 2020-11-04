import argparse
import json
import os
import sys

import pandas
import numpy as np


def convert_json_file():
    print("convert_json_file")


def read_json_file(path):
    with open(path) as json_file:
        data = json.load(json_file)


# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="path to the .json file")
    parser.add_argument("-fo", "--folder", help="path to a folder")
    parser.add_argument("-o", "--output", help="output folder for .srt file(s)")
    args = parser.parse_args()

    file_path = "/home/rosarioscavo/Documents/dataset/Acquisizioni Lab ENIGMA Scavo/HoloLens/QC/temp3.json"

    if args.file:
        file_path = args.file

    print(file_path)
