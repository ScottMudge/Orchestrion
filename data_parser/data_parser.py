# Orchestrion -- Artist-Critic A.I.
#    Copyright (C) 2018  Scott Mudge
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
import midi

SF_NOTE = 0.015625
DEFAULT_TEMPO = 120

###########################################################
# Static Methods
###########################################################


def round_up_to_even(f):
    """Rounds supplied value to nearest even number."""
    return math.ceil(f / 2.) * 2


def tempo_to_ticks(tempo):
    """Converts tempo to midi ticks."""
    return math.floor(60 * 1000000 / tempo)


def ticks_to_seconds(resolution,tempo,ticks):
    """Converts ticks to seconds."""
    return float(((tempo/resolution)/1000000) * ticks)


def get_midi_metadata(midi_file):
    """Returns total number of tracks, events, track names, and total time of midi file"""

    track_cnt = 0
    msg_cnt = 0
    note_ons = 0
    note_offs = 0
    track_names = []
    for Track in midi_file:
        track_cnt += 1
        has_track_name = False
        for AbstractEvent in Track:
            if AbstractEvent.name != 'End of Track':
                msg_cnt += 1
            if AbstractEvent.name == 'Track Name':
                track_names.append(AbstractEvent.text)
                has_track_name = True
            if AbstractEvent.name == 'Note On':
                if AbstractEvent.velocity == 0:
                    note_offs += 1
                else:
                    note_ons += 1

            if AbstractEvent.name == 'Note Off':
                note_offs += 1
        if has_track_name is not True:
            track_names.append('[No Name]')

    return track_cnt, msg_cnt, track_names, note_ons, note_offs

def get_midi_tracks_with_notes(midi_file):
    """This returns the indexes of tracks which contain notes."""

    tracks_with_notes = []

    for i, Track in enumerate(midi_file):
        for AbstractEvent in Track:
            if AbstractEvent.name == 'Note On' or AbstractEvent.name == 'Note Off':
                tracks_with_notes.append(int(i))
                break

    return tracks_with_notes


def get_total_midi_time(midi_file):
    """Returns total midi time of the midi_file."""

    max_time = 0
    tempo = tempo_to_ticks(DEFAULT_TEMPO)

    for Track in midi_file:
        time = 0
        for AbstractEvent in Track:
            ticks = AbstractEvent.tick
            if AbstractEvent.name == 'Set Tempo':
                tempo = tempo_to_ticks(AbstractEvent.bpm)
            time += ticks_to_seconds(midi_file.resolution, tempo, ticks)
        if time > max_time:
            max_time = time
    return max_time

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
        for midi_count, midi_fp in enumerate(self.midi_paths):
            print("Reading MIDI file [" + str(midi_count) + "] (" + midi_fp + ")...")

            #midi_file = MidiFile(midi_fp)

            midi_file = midi.read_midifile(midi_fp)
            midi_file.make_ticks_rel()

            print("\t--> Loaded!")
            track_count = 0
            event_count = 0
            note_ons = 0
            note_offs = 0
            track_names = []
            track_count, event_count, track_names, note_ons, note_offs = get_midi_metadata(midi_file)
            if track_count < 1:
                print("No valid tracks found!")
            else:
                print("\t--> " + str(track_count) + " total tracks:")
                for i in range(0,track_count):
                   print('\t\t > Track {}: {}'.format(i, track_names[i]))

                # Read data

                total_time = get_total_midi_time(midi_file)
                total_px = round_up_to_even(total_time / SF_NOTE)
                px_per_sec = total_px / total_time

                m, s = divmod(total_time, 60)
                print("\t--> Total MIDI Events: \t" + str(event_count))
                print("\t\t > Note Ons: " + str(note_ons) + " | Note Offs: " + str(note_offs))
                print("\t--> Total Time: \t\t%02d:%02d" % (m, s))
                print("\t--> Total Pixels: \t\t" + str(total_px))

                width = round_up_to_even(np.math.sqrt(total_px))
                width = width
                height = width

                print("\t--> Image Dimensions: \t%d x %d" % (width, height))

                img_buf = np.ndarray((width * height, 4,), np.uint16)
                img_buf.fill(0)

                print("\t--> Reading messages...")

                x = 0
                y = 0

                tempo = tempo_to_ticks(DEFAULT_TEMPO)
                time = 0

                tracks_with_notes = get_midi_tracks_with_notes(midi_file)

                for j, Track in enumerate(midi_file):

                    time = 0

                    for AbstractEvent in Track:

                        ticks = AbstractEvent.tick

                        if AbstractEvent.name == 'Set Tempo':
                            tempo = tempo_to_ticks(AbstractEvent.bpm)

                        time += ticks_to_seconds(midi_file.resolution, tempo, ticks)

                        if j not in tracks_with_notes:
                            continue

                        pixel = math.floor(time * px_per_sec)

                        if AbstractEvent.name == 'Note On':
                            if AbstractEvent.velocity == 0:
                                img_buf[pixel][2] = 2 ** 16 - 1
                            else:
                                img_buf[pixel][1] = 2**16-1

                        elif AbstractEvent.name == 'Note Off':
                            img_buf[pixel][2] = 2**16-1

                        img_buf[pixel][3] = 2**16-1

               # img_min = out_img.min(axis=(0,1), keepdims=True)
               # img_max = out_img.max(axis=(0,1), keepdims=True)
               # out_img = (out_img - img_min)/(img_max-img_min)

               # out_img = np.ndarray((width, height, 3), np.int8)
               # for rows in out_img:

                out_img = np.reshape(img_buf, (width, height, 4,), 'C')
                cv.imwrite("C:\\out" + str(midi_count) + ".png", out_img)
                cv.imshow("Result", out_img)
                cv.waitKey(0)

                valid_midi_count += 1

                print("Done reading MIDI file [" + str(midi_count) + "]\n\n----------------------------------------\n")

        return valid_midi_count


if __name__ == "__main__":
    reader = MidiReader()
    reader.add_midi_to_file_list("../../data/midis/tf_in_d_minor.mid")
    reader.add_midi_to_file_list("../../data/midis/dream_sk.mid")
    reader.add_midi_to_file_list("../../data/midis/bach7.mid")
    reader.read_midis()

# out_img = cv.imwrite("out_image.png")

