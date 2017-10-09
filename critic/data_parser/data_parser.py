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

###############
# Imports
###############

# For visualization
import cv2 as cv
import numpy as np
# For midi operations
import mido
from mido import MidiFile

###############


class MidiReader:
    """This uses mido to read through midis in a list."""
    midi_paths = []
    midi_data = []
    midi_parser = mido.Parser()

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
                data = open(midi_fp, "rb").read()

                # Get
                self.midi_parser.feed(data)
                total_messages = self.midi_parser.pending()
                print("\t--> " + str(total_messages) + " total MIDI messages")
                print("\t--> Reading messages...")

                width = int(np.math.sqrt(total_messages))
                width = width
                height = width

                out_img = np.ndarray((width, height, 3), np.int8)
                out_img.fill(0)

                msg = self.midi_parser.get_message()
                x = 0
                y = 0
                while msg is not None and x < width and y < height:
                    msg_d = msg.dict()
                    # print(msg)
                    chan = msg_d.get("channel", 0)
                    note = msg_d.get("note", 0)
                    vel = msg_d.get("velocity", 0)
                    out_img[x][y][0] = np.int8(chan)
                    out_img[x][y][1] = np.int8(note)
                    out_img[x][y][2] = np.int8(vel)
                    x += 1
                    if x >= width:
                        x = 0
                        y += 1
                    msg = self.midi_parser.get_message()

               # img_min = out_img.min(axis=(0,1), keepdims=True)
               # img_max = out_img.max(axis=(0,1), keepdims=True)
               # out_img = (out_img - img_min)/(img_max-img_min)
                cv.imwrite("C:/out" + str(i) + ".tiff", out_img, [int(cv.IMWRITE_PNG_COMPRESSION), 9])

                valid_midi_count += 1

                print("Done reading MIDI file [" + str(i) + "]")

        return valid_midi_count


if __name__ == "__main__":
    reader = MidiReader()
    reader.add_midi_to_file_list("../../data/midis/tf_in_d_minor.mid")
     # reader.add_midi_to_file_list("../../data/midis/bach7.mid")
    reader.read_midis()

# out_img = cv.imwrite("out_image.png")

