import argparse
import json
import math
import os
import sys
import time
import pandas as pd


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


# it creates a dataframe with all the annotations' information for each interval present in intervals
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


# it converts the time (timestamp) expressed in ss.ms (45.234) to hh:mm:ss,ms (00:00:45,234)
def timestamp_converter(timestamp):
    decimal, integer = math.modf(timestamp)
    decimal *= 1000
    decimal = int(decimal)

    return time.strftime('%H:%M:%S', time.gmtime(integer)) + ",%i" % decimal


# it formats the annotation information into the srt format
def srt_formatter(num_caption, timestamp_start, timestamp_end, caption):
    stamp = "%i\n" \
            "%s --> %s\n" \
            "%s\n\n" % (num_caption, timestamp_start, timestamp_end, caption)

    return stamp


# it creates a srt file with name file_name
def srt_creation(file_name, output, dataframe):
    f = open(output + os.path.sep + file_name + ".srt", "w")

    # the VIA format isn't ordered by the srart time of the intervals
    dataframe = dataframe.sort_values('timestamp_start')

    for index, annotation in dataframe.iterrows():
        timestamp_start = timestamp_converter(annotation['timestamp_start'])
        timestamp_end = timestamp_converter(annotation['timestamp_end'])

        stamp = srt_formatter(annotation['num_caption'], timestamp_start, timestamp_end, annotation['caption'])
        f.write(stamp)

    f.close()


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
    srt_creation("Video (4)", output, df)
