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
    midiPaths = []
    midis = []

    # Add test data
    def add_midi_to_file_list(self, filename):
        """Loads a file into the file list."""
        self.midiPaths.append(filename)

    def read_tracks(self):
        """ This reads through the tracks in the midiPaths list and loads them into memory. """
        for i, midi_fp in enumerate(self.midiPaths):
            print("Reading MIDI file [" + str(i) + "]...")
            self.midis.append(MidiFile(midi_fp))
            print("\t--> Loaded!")
            track_count = len(self.midis[i].tracks)
            if track_count < 1:
                print("No valid tracks found!")
                break
            else:
                print("\t--> " + str(track_count) + " total tracks:")
                for i, track in enumerate(self.midis[i].tracks):
                   print('\t\t > Track {}: {}'.format(i, track.name))


if __name__ == "__main__":
    reader = MidiReader()
    reader.add_midi_to_file_list("../../data/midis/tf_in_d_minor.mid")
    reader.read_tracks()

# out_img = cv.imwrite("out_image.png")

