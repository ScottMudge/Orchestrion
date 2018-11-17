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
# File Description:
#       Main application entry point, also used for testing.
#

from utils import logger
from utils.logger import get_logger as logging
from utils import utility
from config import GeneralCfg

from data_parsing.midi_reader import MidiReader

if __name__ == '__main__':
    logger.initialize("Orchestrion", GeneralCfg.log_to_disk.value, utility.get_root_dir())
    log = logging("App")
    log.info(
        "Starting Orchestrion Application:\n"
        "\n"
        "Application Details:\n"
        "__________________________________________________\n\n"
        "\t> Version: {}\n"
        "\t> Author: {}\n"
        "\t> Copyright Year: {}\n"
        "__________________________________________________\n".format(
            GeneralCfg.version.value,
            GeneralCfg.author.value,
            GeneralCfg.copyright_year.value)
    )

    midi_root = utility.get_root_dir() + "/data/midis/"
    midi_reader = MidiReader(midi_root, "{}/data/generated".format(utility.get_root_dir()))
    midi_reader.add_midi_to_file_list("bach7.mid")
    midi_reader.add_midi_to_file_list("dream_sk.mid")
    midi_reader.add_midi_to_file_list("tf_in_d_minor.mid")
    midi_reader.read_midis(True)

    input("Press any key to quit...")

