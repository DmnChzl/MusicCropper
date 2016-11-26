# -*- coding: utf-8 -*-
'''
Copyright (C) 2016 Damien Chazoule

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys

from pydub import AudioSegment

LOG = True
START = 0
END = 0

def extension_version(ext, file):
    if ext.lower() not in [".wav",".mp3",".ogg",".flv",".mp4",".wma",".aac"]:
        return None

    if ext.lower() == ".wav":
        return AudioSegment.from_wav(file)
    elif ext.lower() == ".mp3":
        return AudioSegment.from_mp3(file)
    elif ext.lower() == ".ogg":
        return AudioSegment.from_ogg(file)
    elif ext.lower() == ".flv":
        return AudioSegment.from_flv(file)
    else:
        return AudioSegment.from_file(file, ext[1:])

def crop_audio(file):
    filename, ext = os.path.splitext(file)
    song = extension_version(ext, file)
    if song is None:
        print("Error : Extension '{}' not supported".format(ext))
        sys.exit(1)

    if LOG:
        try:
            os.remove("log.txt")
        except OSError:
            pass

        with open("log.txt", "a") as text:
            text.write("Cropping the '{}' file : \n".format(filename + ext))

    if START != 0:
        song = song[START:]
        if LOG:
            with open("log.txt", "a") as text:
                text.write("Deletion of the first {} second(s) ; \n".format(str(START / 1000)))

    if END != 0:
        song = song[:END]
        if LOG:
            with open("log.txt", "a") as text:
                text.write("Deletion of the last {} second(s) ; \n".format(str(END / -1000)))

    if START != 0 or END != 0:
        new_filename = filename + " (cropped)" + ext
        song.export(new_filename, format=ext[1:])
        if LOG:
            with open("log.txt", "a") as text:
                text.write("Recording in '{}'.".format(new_filename))

def identify_arg(arg):
    global LOG
    global START
    global END

    values = arg.split("=")
    if len(values) == 1:
        if values[0] in ["-l", "--log"]:
            LOG = True
        else:
            print("Unknown option : '{}'".format(values[0]))
            sys.exit(1)
    elif len(values) == 2:
        if values[0] in ["-s", "--start"]:
            START = int(values[1]) * 1000
        elif values[0] in ["-e", "--end"]:
            END = int(values[1]) * -1000
        else:
            print("Unknown option : '{}'".format(values[0]))
            sys.exit(1)
    else:
        print("Unknown option : '{}'".format(values[0]))
        sys.exit(1)

def use_assistant():
    global LOG
    global START
    global END

    START = int(input("How many seconds would you want to remove at the beginning of the song : "))
    START *= 1000
    END = int(input("How many seconds would you want to remove at the ending of the song : "))
    END *= -1000

    val = input("Would you display logs (Y/n) ? ")
    if val.lower() in ["n", "no"]:
        LOG = False

def show_help():
    print('''Usage : music_cropper.py [file.[wav|mp3|ogg|flv|mp4|wma|aac]] [option] ...
Options available :
-l : create .txt with logs of the process (also --log)
-e : precise how many seconds to remove at the ending of the song, use it like this : '-e=[value]' (also --end)
-s : precise how many seconds to remove at the beginning of the song, use it like this : '-s=[value]' (also --start)
-h : print this help message (also --help)
''')

if __name__ == "__main__":
    args = list(sys.argv)
    args.remove("music_cropper.py")
    if len(args) >= 1:
        if "-h" in args:
            show_help()
            sys.exit(1)
        elif "--help" in args:
            show_help()
            sys.exit(1)
        else:
            path = args[0]
            if len(args) > 1:
                for x in range(1, len(args)):
                    identify_arg(args[x])
            else:
                use_assistant()
    else:
        print('''Usage : Usage : music_cropper.py [file.[wav|mp3|ogg|flv|mp4|wma|aac]]''')
        sys.exit(1)

    if os.path.isfile(path):
        crop_audio(path)
    else:
        print("Error : Path {} not found".format(path))
