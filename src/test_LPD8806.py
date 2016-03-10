# LPD8806 Python driver.
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
import LPD8806


class TestStrand(unittest.TestCase):
    def test_init(self):
        m = mock.mock_open()
        with mock.patch.object(builtins, 'open', m):
            dut = LPD8806.Strand()
            m.assert_called_once_with('/dev/spidev0.0', "wb")
            self.assertEqual(dut.dev, '/dev/spidev0.0')
            self.assertEqual(dut.leds, 160)
            self.assertEqual(dut.buffer[-1], bytearray([0, 0, 0]))

if __name__ == '__main__':
    unittest.main()
