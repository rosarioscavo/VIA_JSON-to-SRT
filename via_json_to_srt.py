import argparse
import json
import math
import os
import sys
import time
import pandas as pd
import numpy as np


# it returns the via json file or None if it's in the correct format
def get_via_json(filename):
    with open(filename) as json_file:
        file = json.load(json_file)

        # check whatever it's a via json file
        if not "fname" in file['file']['1']:
            return None
        else:
            return file

        # try:
        #     var = file['file']['1']['fname']
        #     return file
        # except KeyError:
        #     return None


# it returns the video's name that has been annotated
def get_video_name(json_file):
    filename = json_file['file']['1']['fname']
    return filename.split(".", 1)[0]


# it creates a dataframe with all the annotations' information for each interval
def intervals_dataframe_creation(json_file):
    intervals = json_file['metadata'].values()
    df = pd.DataFrame(columns=['caption', 'timestamp_start', 'timestamp_end'])

    for interval_info in intervals:
        # if it's a region
        if len(interval_info['xy']) > 0:
            continue

        caption = interval_info['av']['1']
        timestamp_start = interval_info['z'][0]
        timestamp_end = interval_info['z'][1]

        new_row = {'caption': caption, 'timestamp_start': timestamp_start,
                   'timestamp_end': timestamp_end}

        df = df.append(new_row, ignore_index=True)

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
    f = open(output + file_name + ".srt", "w")

    # the VIA format isn't ordered by the start time of the intervals
    dataframe = dataframe.sort_values('timestamp_start')
    dataframe.index = np.arange(0, len(dataframe))

    for index, annotation in dataframe.iterrows():
        timestamp_start = timestamp_converter(annotation['timestamp_start'])
        timestamp_end = timestamp_converter(annotation['timestamp_end'])

        stamp = srt_formatter(index, timestamp_start, timestamp_end, annotation['caption'])
        f.write(stamp)

    f.close()


# steps to convert .json to .srt
def algorithm(filename, output):
    f = get_via_json(filename)
    if f is not None:
        if output is None:
            output = os.path.dirname(filename) + os.path.sep
        video_name = get_video_name(f)
        df = intervals_dataframe_creation(f)
        srt_creation(video_name, output, df)


# main program
def files_iteration(folder, output):
    directory = os.path.dirname(folder)
    empty = True

    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".json"):
                empty = False
                algorithm(filepath, output)

    if empty:
        print("The folder passed doesn't contain any .json files")


# main
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="path to a .json file")
    parser.add_argument("-fo", "--folder", help="path to a folder. It'll load only .json files")
    parser.add_argument("-o", "--output",
                        help="output folder for .srt file(s). If not specified, the .srt file(s) will be saved on the "
                             "same location of .json file(s)")
    args = parser.parse_args()

    if args.output:
        if not os.path.isdir(args.output):
            print("The output folder isn't a folder")
            sys.exit(1)
        else:
            output = args.output
    else:
        output = None

    if args.file:
        if os.path.isfile(args.file):
            algorithm(args.file, output)
            sys.exit(0)
        else:
            print("The path passed isn't a file")
            sys.exit(1)
    else:
        if args.folder:
            if os.path.isdir(args.folder):
                files_iteration(args.folder, output)
            else:
                print("The path passed isn't a folder")
                sys.exit(1)
        else:
            print("It is necessary to specify a file or a folder")
            sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
