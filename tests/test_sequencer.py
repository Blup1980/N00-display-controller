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

import unittest
import unittest.mock as mock
import builtins
import sys
sys.path.insert(0, '../src')
import sequencer
import tempfile
import os
import icalendar
import datetime


class TestSequencer(unittest.TestCase):
    def test_init(self):
        dut = sequencer.Sequencer('/dev/null')
        self.assertEqual(dut.path, '/dev/null')

    def test_fileOpenOk(self):
        m = mock.mock_open()
        # noinspection PyUnresolvedReferences
        with mock.patch.object(builtins, 'open', m):
            dut = sequencer.Sequencer('/dev/null')
            dut.get_msg()
            m.assert_called_once_with('/dev/null', mode='rb')

    def test_fileOpenError(self):
        dut = sequencer.Sequencer('/impossiblePath/test.ics')
        self.assertRaises(OSError, dut.get_msg)

    def test_fileParsingWithin(self):
        cal = icalendar.Calendar()
        now = datetime.datetime.now()
        delta_t = datetime.timedelta(minutes=10)

        event = icalendar.Event()
        event.add('dtstart', now-delta_t)
        event.add('dtend', now+delta_t)
        event.add('summary', 'N00')
        cal.add_component(event)

        cal_content = cal.to_ical()

        fp = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
        fp.write(cal_content)
        fp.close()
        dut = sequencer.Sequencer(fp.name)
        msg = dut.get_msg()
        os.remove(fp.name)
        self.assertEqual(msg, b'N00')

    def test_fileParsingOutside(self):
        cal = icalendar.Calendar()
        now = datetime.datetime.now()
        delta_t = datetime.timedelta(minutes=10)

        event = icalendar.Event()
        event.add('dtstart', now+delta_t)
        event.add('dtend', now+delta_t+delta_t)
        event.add('summary', 'N00')
        cal.add_component(event)

        cal_content = cal.to_ical()

        fp = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
        fp.write(cal_content)
        fp.close()
        dut = sequencer.Sequencer(fp.name)
        msg = dut.get_msg()
        os.remove(fp.name)
        self.assertEqual(msg, '')

    def test_Recurrence(self):
            cal = icalendar.Calendar()
            now = datetime.datetime.now()
            delta_t = datetime.timedelta(minutes=10)

            event = icalendar.Event()
            event.add('dtstart', now + delta_t)
            event.add('summary', 'N00')
            event.add('rrule', {'INTERVAL': [3], 'FREQ': ['WEEKLY'], 'BYDAY': ['FR']})

            cal.add_component(event)

            cal_content = cal.to_ical()

            fp = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
            fp.write(cal_content)
            fp.close()
            dut = sequencer.Sequencer(fp.name)
            msg = dut.get_msg()
            os.remove(fp.name)
            self.assertEqual(msg, '')



if __name__ == '__main__':
    unittest.main()
