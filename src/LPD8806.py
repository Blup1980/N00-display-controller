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


class Strand:

    def __init__(self, leds=160, dev="/dev/spidev0.0"):
        """
        Variables:
            :type leds: object
            :param leds -- strand size
            :param dev -- spi device
        """
        self.dev = dev
        self.spi = open(self.dev, "wb")
        self.leds = leds
        self.gamma = bytearray(256)
        self.latchBytes = bytearray(int((leds + 31) / 32))
        self.buffer = []
        for x in range(self.leds):
            self.buffer.append([0, 0, 0])
        for led in range(self.leds):
            self.buffer[led] = bytearray(3)
        for i in range(256):
            # Color calculations from
            # http://learn.adafruit.com/light-painting-with-raspberry-pi
            self.gamma[i] = 0x80 | int(
                pow(float(i) / 255.0, 2.5) * 127.0 + 0.5
            )

    def show(self, pixel_list):
        """
        Fill the strand with the pixel values
        Variables:
            :param pixel_list -- List of Pixel class to display
        """
        for i in range(len(pixel_list)):
            self.buffer[i][0] = self.gamma[pixel_list[i].g]
            self.buffer[i][1] = self.gamma[pixel_list[i].r]
            self.buffer[i][2] = self.gamma[pixel_list[i].b]
        self._update()

    def _update(self):
        """
        Flush the buffer to the strand
        """
        for x in range(self.leds):
            self.spi.write(bytearray(self.buffer[x]))
            self.spi.flush()
        self.spi.write(self.latchBytes)
        self.spi.flush()
