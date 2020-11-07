# VIA project (json) to srt
It's a simple script created to make a .srt file starting from a VIA (VGG Image Annotator) .json file obtained by annotating a video.

Annotations on the interface of VIA aren't comfortably viewable, especially for many different labels. However, using a .srt file, you can see annotations as subtitles on a video player to control them more comfortably.



## Table of contents

- [General-info](#general-info)

- [Comparison](#comparison)

- [Setup](#setup)

- [Usage](#usage)

- [Developed by](#developed-by)

  

## General info
>VGG Image Annotator is a simple and standalone manual annotation software for image, audio and video. VIA runs in a web browser and does not require any installation or setup. The complete VIA software fits in a single self-contained HTML page of size less than 400 Kilobyte that runs as an offline application in most modern web browsers.

Source: [VGG Image Annotator](http://www.robots.ox.ac.uk/~vgg/software/via/)

VIA projects are saved by using .json files. In the .json file, all the intervals and the name of the corresponding label are stored, even the name of the video that has been annotated. 

The .srt file is created following the [standard format](https://en.wikipedia.org/wiki/SubRip#File_format), specifically:

1. The index starts by 0
2. The beginning timestamp and the ending timestamp of the interval, each in hh:mm:ss,ms
3. The label
4. A blank line

In the .json file also the regions are stored but, they are ignored during the conversion process.



## Comparison

This is the VIA web interface. Depending on the size of the monitor and the number of labels, it's quite impossible to see all the labels and reproducing the video, you have to scroll down and up in order to see which labels are annotated at that instant.  



<img src="https://drive.google.com/uc?export=view&id=1hZbIiyC1majH1OSnTpPRPSujrzqK6pLJ" style="zoom:50%;" />



This is the visualisation using a video player and the .srt file generated.

 <img src="https://drive.google.com/uc?export=view&id=1eTOLJcSbJ7QQ9hduwbD6ta9T_DiJjBBb" style="zoom:50%;" />





## Setup

N.B. If you haven't already installed the following packages, you need to do it.

- pandas

- numpy

  

1. Clone the repository

2. ```
   $ cd path_to_cloned_repo
   ```



## Usage

It's possible to use this command to see the arguments that can be used.

```
$ python via_json_to_srt.py --help
```

This is the help message:

```
-h, --help            		show this help message and exit
-f FILE, --file FILE  		path to a .json file
-fo FOLDER, --folder FOLDER path to a folder. It'll load only .json files
-o OUTPUT, --output OUTPUT  output folder for .srt file(s). If not specified, the .srt file(s) will be saved 							 on the same location of .json file(s)
```

Using the folder argument, the script will convert all the json files that are in the VIA's format in the directory and subdirectories.

If -f and -fo arguments are used at the same time, the script will ignore the -fo argument.



## Developed by

- [Rosario Scavo](https://github.com/PerseRos) 

