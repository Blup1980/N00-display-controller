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

from LPD8806 import Strand


class Display:

    def __init__(self):
        """
        :return:
        """
        self.strand = Strand(leds=38+41+41)

    def show(self, string):
        """
        :param string:
        :return:
        """
        parsed = self._parse(string)
        l = LetterDisplay(parsed[0])
        d0 = DigitDisplay(parsed[1])
        d1 = DigitDisplay(parsed[3])

        pixel_list = []
        pixel_list.extend(l.get_pixel_list())
        pixel_list.extend(d0.get_pixel_list())
        pixel_list.extend(d1.get_pixel_list())

        self.strand.show(pixel_list)

    @staticmethod
    def _parse(input_str):
        """
        Parse the input string into letters
        :param input_str:
        :return tuple:
        """
        if ~isinstance(input_str, str):
            raise TypeError

        if len(input_str) != 3:
            raise ValueError
        n, d1, d2 = input_str
        return n, d1, d2


class ChrDisplay:

    def __init__(self):
        """
        :return:
        """
        self.pixel_list = []

    def set_color(self, r, g, b):
        """
        The the color of the chr
        :param r:
        :param g:
        :param b:
        :return:
        """
        if r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b < 0:
            raise ValueError

        for x in self.pixel_list:
            if x.enabled:
                x.r = r
                x.g = g
                x.b = b

    def get_pixel_list(self):
        """
        :return:
        """
        return self.pixel_list


class LetterDisplay(ChrDisplay):

    def __init__(self, char):
        """
        :param char:
        :return:
        """
        super().__init__()
        if char == 'N':
            self.pixel_list = [Pixel(True) for _ in range(13+12+13)]
        else:
            self.pixel_list = [Pixel(False) for _ in range(13+12+13)]


class DigitDisplay(ChrDisplay):

    def __init__(self, digit):
        """
        :param digit:
        :return:
        """
        super().__init__()
        if digit == '0':
            self.pixel_list = [Pixel(True) for _ in range(13+5+13+5)]
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
        elif digit == '1':
            self.pixel_list = [Pixel(False) for _ in range(13+5)]
            self.pixel_list.extend([Pixel(True) for _ in range(13)])
            self.pixel_list.extend([Pixel(False) for _ in range(5+5)])
        elif digit == '2':
            self.pixel_list = [Pixel(True) for _ in range(1)]
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1+6+5+1)])
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(7+5+5)])
        elif digit == '3':
            self.pixel_list = [Pixel(True) for _ in range(1)]
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1)])
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1+5+13+5+5)])
        elif digit == '4':
            self.pixel_list = [Pixel(True) for _ in range(6+1)]
            self.pixel_list.extend([Pixel(False) for _ in range(6+5)])
            self.pixel_list.extend([Pixel(True) for _ in range(13)])
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(5)])
        elif digit == '5':
            self.pixel_list = [Pixel(True) for _ in range(6+1)]
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1+5+7)])
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1+5+5)])
        elif digit == '6':
            self.pixel_list = [Pixel(True) for _ in range(13+5+1+6)]
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1+5+5)])
        elif digit == '7':
            self.pixel_list = [Pixel(True) for _ in range(1)]
            self.pixel_list.extend([Pixel(False) for _ in range(5+1+6+5)])
            self.pixel_list.extend([Pixel(True) for _ in range(13+5)])
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
        elif digit == '8':
            self.pixel_list = [Pixel(True) for _ in range(13+5+13+5+5)]
        elif digit == '9':
            self.pixel_list = [Pixel(True) for _ in range(1+5+1)]
            self.pixel_list.extend([Pixel(False) for _ in range(5)])
            self.pixel_list.extend([Pixel(True) for _ in range(1+5+13+5+5)])
        else:
            self.pixel_list = [Pixel(False) for _ in range(13+5+13+5+5)]


class Pixel:

    def __init__(self, enabled):
        """
        :param enabled:
        :return:
        """
        self.enabled = enabled
        self.r = 0
        self.g = 0
        self.b = 0
