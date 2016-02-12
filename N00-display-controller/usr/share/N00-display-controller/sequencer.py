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
from time import time
import requests


class Sequencer:

    def __init__(self, url, interval_min):
        """
        :param url: The full url of the csv file
        :param interval_min: the interval time to recheck for file changes in minutes
        :return:
        """
        if ~isinstance(url, str):
            raise TypeError

        if interval_min <= 0:
            raise ValueError

        self.URL = url
        self.interval = interval_min * 60
        self.last_check_time = 0
        self.sequence = []

    def get_msg(self):
        """
        Get the current message to display
        :return: string of the msg to display
        """

        if self.last_check_time + self.interval <= time():
            self._refresh()

    def _refresh(self):
        r = requests.get(self.URL)
        #TODO do the parsing

