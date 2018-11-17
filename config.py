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
#       Main application configuration.
#

from utils import settings
from utils.logger import get_logger as logging
import utils.utility as utility


class General(settings.Config):
    """General configuration parameters."""
    def __init__(self):
        super().__init__("general", utility.get_root_dir())
        self.log_to_disk = self.add_param("LogToDisk", True)
        self.version = self.add_param("Version", "0.1.0")
        self.author = self.add_param("Author", "Scott Mudge")
        self.copyright_year = self.add_param("CopyrightYear", "2018")
        self.save()


GeneralCfg = General()
