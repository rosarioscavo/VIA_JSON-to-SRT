import argparse
import json
import os
import sys

import pandas as pd
import numpy as np


def intervals_dataframe_creation(intervals):
    num_caption = 1
    df = pd.DataFrame(columns=['num_caption', 'caption', 'timecodes_start', 'timecodes_end'])

    for interval_info in intervals:
        caption = interval_info['av']['1']
        timecodes_start = interval_info['z'][0]
        timecodes_end = interval_info['z'][1]

        new_row = {'num_caption': num_caption, 'caption': caption, 'timecodes_start': timecodes_start,
                   'timecodes_end': timecodes_end}

        df = df.append(new_row, ignore_index=True)
        num_caption += 1
    return df


# return the intervals' info after reading a json file from the filename path
def read_intervals(filename):
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except ValueError:
        print("Perhaps the file is not a JSON file")
    else:
        # the intervals are a dictionary
        return data['metadata'].values()


# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="Path to the .json file")
    parser.add_argument("-fo", "--folder", help="Path to a folder. It'll load only .json files")
    parser.add_argument("-o", "--output", help="Output folder for .srt file(s)")
    args = parser.parse_args()

    filename = "/home/rosarioscavo/Documents/dataset/Acquisizioni Lab ENIGMA Scavo/HoloLens/QC/temp3.json"

    if args.file:
        filename = args.file

    intervals = read_intervals(filename)
    df = intervals_dataframe_creation(intervals)
    print(df)
