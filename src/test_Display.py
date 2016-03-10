from unittest import TestCase
import unittest.mock as mock
import N00_display


class TestDisplayClass(TestCase):
    @mock.patch('N00_display.Strand')
    def test_init(self, mock_strand):
        N00_display.Display()
        mock_strand.assert_called_with(leds=38+41+41, dev='/dev/spidev0.0')

    def test_parse(self):
        result = N00_display.Display._parse('N12')
        self.assertEqual(result[0], 'N')
        self.assertEqual(result[1], '1')
        self.assertEqual(result[2], '2')

        self.assertRaises(ValueError, N00_display.Display._parse, 'N111')
        self.assertRaises(TypeError, N00_display.Display._parse, 10)

    @mock.patch('N00_display.Strand')
    def test_show(self, mock_strand):
        dut = N00_display.Display()
        dut.show('N88')
        expected = [N00_display.Pixel(1)]*(38+41+41)
        mock_strand.return_value.show.assert_called_with(expected)

        dut.show('   ')
        expected = [N00_display.Pixel(0)]*(38+41+41)
        mock_strand.return_value.show.assert_called_with(expected)

        dut.show(' 88')
        expected = [N00_display.Pixel(0)]*38 + [N00_display.Pixel(1)]*(41+41)
        mock_strand.return_value.show.assert_called_with(expected)

        dut.show('N 8')
        expected = [N00_display.Pixel(1)]*38 + [N00_display.Pixel(0)]*41 + [N00_display.Pixel(1)]*41
        mock_strand.return_value.show.assert_called_with(expected)

        dut.show('N8 ')
        expected = [N00_display.Pixel(1)]*38 + [N00_display.Pixel(1)]*41 + [N00_display.Pixel(0)]*41
        mock_strand.return_value.show.assert_called_with(expected)


class TestAlphanumDisplay(TestCase):

    def test_pixelLength(self):
        dut = N00_display.LetterDisplay('N')
        l = dut.get_pixel_list()
        self.assertEqual(len(l), 13+13+12)

        dut = N00_display.LetterDisplay(' ')
        l = dut.get_pixel_list()
        self.assertEqual(len(l), 13+13+12)

        for i in range(0, 9):
            dut = N00_display.DigitDisplay(str(i))
            l = dut.get_pixel_list()
            self.assertEqual(len(l), 41, "for the digit: " + str(i))

        dut = N00_display.DigitDisplay(' ')
        l = dut.get_pixel_list()
        self.assertEqual(len(l), 41, "for no digit:")

    def test_pixelColor(self):
        dut = N00_display.DigitDisplay('3')
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
