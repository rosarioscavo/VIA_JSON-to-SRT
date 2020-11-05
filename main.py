import argparse
import json
import math
import os
import sys
import time

import pandas as pd
import numpy as np


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


def intervals_dataframe_creation(intervals):
    num_caption = 1
    df = pd.DataFrame(columns=['num_caption', 'caption', 'timestamp_start', 'timestamp_end'])

    for interval_info in intervals:
        caption = interval_info['av']['1']
        timestamp_start = interval_info['z'][0]
        timestamp_end = interval_info['z'][1]

        new_row = {'num_caption': num_caption, 'caption': caption, 'timestamp_start': timestamp_start,
                   'timestamp_end': timestamp_end}

        df = df.append(new_row, ignore_index=True)
        num_caption += 1
    return df


# it converts the time expressed in ss.ms (45.234) to hh:mm:ss,ms (00:00:45,234)
def timestamp_converter(timestamp):
    decimal, integer = math.modf(timestamp)
    decimal*=1000
    decimal=int(decimal)
    return time.strftime('%H:%M:%S', time.gmtime(integer)) + ",%i" % decimal


# def srt_creation(file_name, dataframe):
#     # f = open(file_name+".srt", "w")
#     # f.write()
#     # f.close()
#     annotation = dataframe.loc[0]
#     print("%i \n"
#           "%5.3f" % (annotation['num_caption'], annotation['timestamp_start']))
#     print()


# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="Path to the .json file")
    parser.add_argument("-fo", "--folder", help="Path to a folder. It'll load only .json files")
    parser.add_argument("-o", "--output", help="Output folder for .srt file(s)")
    args = parser.parse_args()

    filename = "/home/rosarioscavo/Documents/dataset/Acquisizioni Lab ENIGMA Scavo/HoloLens/QC/temp3.json"
    output = "/home/rosarioscavo/Documents/dataset/Acquisizioni Lab ENIGMA Scavo/HoloLens/QC"

    if args.file:
        filename = args.file
    if args.output:
        output = args.output

    intervals = read_intervals(filename)
    df = intervals_dataframe_creation(intervals)
    annotation = df.loc[0]
    timestamp_converter(annotation['timestamp_start'])
    # srt_creation("video(4)", df)
