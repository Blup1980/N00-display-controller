from unittest import TestCase
import N00_display as DUTModule


class TestAlphanumDisplay(TestCase):

    def test_pixelLength(self):
        dut = DUTModule.LetterDisplay('N')
        l = dut.get_pixel_list()
        self.assertEqual(len(l), 13+13+12)

        dut = DUTModule.LetterDisplay(' ')
        l = dut.get_pixel_list()
        self.assertEqual(len(l), 13+13+12)

        for i in range(0, 9):
            dut = DUTModule.DigitDisplay(str(i))
            l = dut.get_pixel_list()
            self.assertEqual(len(l), 41, "for the digit: " + str(i))

        dut = DUTModule.DigitDisplay(' ')
        l = dut.get_pixel_list()
        self.assertEqual(len(l), 41, "for no digit:")

    def test_pixelColor(self):
        dut = DUTModule.DigitDisplay('3')
        l = dut.get_pixel_list()
        for x in l:
            self.assertEqual(x.r, 0)
            self.assertEqual(x.g, 0)
            self.assertEqual(x.b, 0)

        dut.set_color(0, 2, 255)
        l = dut.get_pixel_list()
        for x in l:
            if x.enabled:
                self.assertEqual(x.r, 0)
                self.assertEqual(x.g, 2)
                self.assertEqual(x.b, 255)
            else:
                self.assertEqual(x.r, 0)
                self.assertEqual(x.g, 0)
                self.assertEqual(x.b, 0)

        self.assertRaises(ValueError, dut.set_color, 0, 0, 256)
        self.assertRaises(ValueError, dut.set_color, 0, 256, 0)
        self.assertRaises(ValueError, dut.set_color, 256, 0, 0)

        self.assertRaises(ValueError, dut.set_color, 0, 0, -1)
        self.assertRaises(ValueError, dut.set_color, 0, -1, 0)
        self.assertRaises(ValueError, dut.set_color, -1, 0, 0)
