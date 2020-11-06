import argparse
import json
import math
import os
import time
import pandas as pd
import numpy as np


# it returns the video's name that has been annotated
def get_video_name(filename):
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except ValueError:
        print("Perhaps the file is not a JSON file")
    else:
        filename = data['file']['1']['fname']
        return filename.split(".", 1)[0]


# return the intervals' info after reading a json file from the filename path
def get_intervals(filename):
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
    video_name = get_video_name(filename)
    print(video_name)
    intervals = get_intervals(filename)
    df = intervals_dataframe_creation(intervals)
    srt_creation(video_name, output, df)


# main program
def via_json_to_srt(filename, output):
    if os.path.isfile(filename):
        if output is None:
            output = os.path.dirname(filename) + os.path.sep
        algorithm(filename, output)
    else:
        directory = os.path.dirname(filename)
        for filename in os.scandir(directory):
            output_path = output
            if filename.path.endswith(".json") and filename.is_file():
                if output is None:
                    output_path = os.path.dirname(filename) + os.path.sep
                algorithm(filename, output_path)


# main
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="Path to a .json file or directory")
    parser.add_argument("-fo", "--folder", help="Path to a folder. It'll load only .json files")
    parser.add_argument("-o", "--output",
                        help="Output folder for .srt file(s). If not specified, the .srt file(s) will be saved on the "
                             "same location of .json file(s)")
    args = parser.parse_args()

    filename = "/home/rosarioscavo/Documents/dataset/Acquisizioni Lab ENIGMA Scavo/HoloLens/QC/"
    output = "/home/rosarioscavo/Documents/dataset/Acquisizioni Lab ENIGMA Scavo/HoloLens/QC/temp/"

    # if args.file:
    #     filename = args.file
    # else:
    #     if args.folder:
    #         filename = args.file
    #     else:
    #         print("It is necessary to specify a file or a folder")
    #         sys.exit(1)
    #
    # if args.output:
    #     output = args.output
    # else:
    #     print("It is necessary to specify the output folder")
    #     sys.exit(1)
    output= None
    via_json_to_srt(filename, output)


if __name__ == '__main__':
    main()
