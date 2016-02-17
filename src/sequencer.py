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
import requests
import logging


class Sequencer:

    def __init__(self, url, interval_min):
        """
        :param url: The full url of the csv file
        :param interval_min: the interval time to recheck for file changes in minutes
        :return:
        """
        if not isinstance(url, str):
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

        now = datetime.today()
        if self.last_check_time + self.interval <= now.timestamp():
            logging.debug('Sequence need refresh from server')
            self._refresh()

        msg = ''
        for t in self.sequence:
            if t['start'] <= now < t['stop']:
                msg = t['msg']
        return msg

    def _refresh(self):
        # TODO manage the exception of no connexion or issues with the parsing
        r = requests.get(self.URL)
        if not r.ok:
            logging.warning('Cannot access the server. server returned error: %s', r.status_code)
            return
        lines = r.text.split('\n')
        parsed = [l.split(';') for l in lines]
        parsed = parsed[1:]
        seq = []
        for f in parsed:
            try:
                time_start = datetime.strptime(f[0], '%d.%m.%Y %H:%M')
                time_stop = datetime.strptime(f[1], '%d.%m.%Y %H:%M')
                msg = f[2]
                seq.append({'start': time_start, 'stop': time_stop, 'msg': msg})
            except ValueError:
                logging.warning('Problem parsing the result from the server')
                pass
        self.sequence = seq
