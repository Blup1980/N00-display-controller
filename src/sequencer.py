# N00-display-controller.
# Copyright (C) 2016  Blup1980
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from datetime import datetime
import icalendar


class Sequencer:

    def __init__(self, path):
        """
        :param path: The full path of the csv file
        :return:
        """
        assert isinstance(path, str), 'Path given is not a string'

        self.path = path
        self.cal = False

    def get_msg(self):
        """
        Get the current message to display
        :return: string of the msg to display
        """
        assert isinstance(self.path, str), 'self.path is not a string'
        msg = ''
        try:
            f = open(self.path, mode='rb')
            data = f.read()
            f.close()
        except:
            raise OSError
        else:
            self.cal = icalendar.Calendar.from_ical(data)
            for e in self.cal.walk('VEVENT'):
                if e.decoded('DTSTART') <= datetime.now() < e.decoded('DTEND'):
                    msg = e.decoded('SUMMARY')
        return msg
