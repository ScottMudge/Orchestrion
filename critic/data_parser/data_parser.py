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
midiPaths = []
midis = []

# Add test data
midiPaths.append("../../data/midis/tf_in_d_minor.mid")

for i, midi_fp in enumerate(midiPaths):
    print("Reading MIDI file [" + str(i) + "]...")
    midis.append(MidiFile(midi_fp))
    print("\t--> Loaded!")
    track_count = len(midis[i].tracks)
    if track_count < 1:
        print("No valid tracks found!")
        break
    else:
        print("\t--> " + str(track_count) + " total tracks:")
        for i, track in enumerate(midis[i].tracks):
            print('\t\t > Track {}: {}'.format(i, track.name))


# out_img = cv.imwrite("out_image.png")

