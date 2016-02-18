#!/usr/bin/python3
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

import daemon
from N00_display import Display
from sequencer import Sequencer
import logging
import threading
import configparser


class App:

    def __init__(self):
        # daemon_context = daemon.DaemonContext()
        # daemon_context.open()
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                            filename='/var/log/N00-display-controller.log', level=logging.DEBUG)
        logging.info('Script started')
        self.config = configparser.ConfigParser()
        url = ''
        try:
            self.config.read('/etc/N00-display.conf')
            url = self.config['SERVER']['Url']

        except configparser.Error:
            logging.warning('Cannot use value in /etc/N00-display.conf')

        self.dis = Display()
        self.seq = Sequencer(url, 1)

    def run(self):
        t = threading.Timer(7.0, self.run)
        t.daemon = True
        t.start()
        logging.debug('Calling Display.show')
        self.dis.show(self.seq.get_msg())
        print('test')

App = App()

App.run()

while True:
    pass
