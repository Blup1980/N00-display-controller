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
            :param leds -- strand size
            :param dev -- spi device
        """
        self.dev = dev
        self.spi = open(self.dev, "wb")
        self.leds = leds
        self.gamma = bytearray(256)
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

    def fill(self, r, g, b, start=0, end=0):
        """
        Fill the strand (or a subset) with a single color
        Variables:
            :param r -- Red value
            :param g -- Green value
            :param b -- Blue value
            :param start -- index of the first LED to consider
            :param end -- index of the last LED to consider
        """
        if start < 0:
            raise NameError("Start invalid:" + str(start))
        if end == 0:
            end = self.leds
        if end > self.leds:
            raise NameError("End invalid: " + str(end))
        for led in range(start, end):
            self.buffer[led][0] = self.gamma[g]
            self.buffer[led][1] = self.gamma[r]
            self.buffer[led][2] = self.gamma[b]

    def set(self, pixel, r, g, b):
        """
        Set a single LED a specific color
        Variables:
            :param pixel -- index of the pixel
            :param r -- Red value
            :param g -- Green value
            :param b -- Blue value
        """
        self.buffer[pixel][0] = self.gamma[g]
        self.buffer[pixel][1] = self.gamma[r]
        self.buffer[pixel][2] = self.gamma[b]

    def update(self):
        """
        Flush the buffer to the strand
        """
        for x in range(self.leds):
            self.spi.write(bytearray(self.buffer[x]))
            self.spi.flush()
        self.spi.write(bytearray(b'\x00'))
        self.spi.flush()
