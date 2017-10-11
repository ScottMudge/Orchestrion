# Orchestrion -- Artist-Critic A.I.
#    Copyright (C) 2017  Scott Mudge
#
#    mail@scottmudge.com
#    http://www.scottmudge.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


"""
@package data_parser

This package parses midi files of a certain directory, restructures it in a format that is amenable for training the
critic model.
"""

###########################################################
# Imports
###########################################################

# For visualization
import cv2 as cv
import numpy as np
import math
# For midi operations
from mido import MidiFile
from mido import tick2second
from mido.midifiles.midifiles import DEFAULT_TEMPO

SF_NOTE = 0.015625

###########################################################
# Static Methods
###########################################################


def msg_count(midi_file):
    """Returns the number of messages in the midi file supplied.

    Inclusive of end-track messages."""
    return sum(len(track) for track in midi_file.tracks)


def round_up_to_even(f):
    """Rounds supplied value to nearest even number."""
    return math.ceil(f / 2.) * 2

class MidiReader:
    """This uses mido to read through midis in a list."""
    midi_paths = []
    midi_data = []

    # Add test data
    def add_midi_to_file_list(self, filename):
        """Loads a file into the file list."""
        self.midi_paths.append(filename)

    def read_midis(self):
        """ This reads through the tracks in the midiPaths list and loads them into memory.

        @return Number of valid midis"""
        # Local vars
        valid_midi_count = 0

        # Enumerate through the midi files
        for i, midi_fp in enumerate(self.midi_paths):
            print("Reading MIDI file [" + str(i) + "] (" + midi_fp + ")...")
            midi_file = MidiFile(midi_fp)
            print("\t--> Loaded!")
            track_count = len(midi_file.tracks)
            if track_count < 1:
                print("No valid tracks found!")
            else:
                print("\t--> " + str(track_count) + " total tracks:")
                for i, track in enumerate(midi_file.tracks):
                   print('\t\t > Track {}: {}'.format(i, track.name))

                # Read data

                total_messages = msg_count(midi_file)
                total_time = midi_file.length
                total_px = round_up_to_even(total_time / SF_NOTE)
                px_per_sec = total_px / total_time

                m, s = divmod(total_time, 60)
                print("\t--> Total MIDI Msgs: \t" + str(total_messages))
                print("\t--> Total Time: \t\t%02d:%02d" % (m, s))
                print("\t--> Total Pixels: \t\t" + str(total_px))

                width = round_up_to_even(np.math.sqrt(total_px))
                width = width
                height = width

                print("\t--> Image Dimensions: \t%d x %d" % (width, height))

                img_buf = np.ndarray((width * height, 3,), np.uint8)
                img_buf.fill(0)


                print("\t--> Reading messages...")

                x = 0
                y = 0
                tempo = DEFAULT_TEMPO
                time = 0
                for msg in midi_file:
                    time += msg.time

                    pixel = math.floor(time * px_per_sec)

                    print(str(time))

                    if msg.type == 'set_tempo':
                        tempo = msg.tempo

                    img_buf[pixel][1] = 255
                    x += 1

               # img_min = out_img.min(axis=(0,1), keepdims=True)
               # img_max = out_img.max(axis=(0,1), keepdims=True)
               # out_img = (out_img - img_min)/(img_max-img_min)

               # out_img = np.ndarray((width, height, 3), np.int8)
               # for rows in out_img:

                out_img = np.reshape(img_buf, (width, height, 3,), 'C')
                cv.imshow("Result", out_img)
                cv.waitKey(0)

                valid_midi_count += 1

                print("Done reading MIDI file [" + str(i) + "]")

        return valid_midi_count


if __name__ == "__main__":
    reader = MidiReader()
    reader.add_midi_to_file_list("../../data/midis/tf_in_d_minor.mid")
     # reader.add_midi_to_file_list("../../data/midis/bach7.mid")
    reader.read_midis()

# out_img = cv.imwrite("out_image.png")

