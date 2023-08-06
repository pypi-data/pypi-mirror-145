# -*- coding: utf-8 -*-

import unittest

from uval.utils.label_naming import label_long_to_short, label_short_to_long

example_volume_id_1 = "BAGGAGE_20210901_064516_00000"
example_volume_id_2 = "BAGGAGE_20190719_203712_28467"
example_label_id_1 = "%_label_1"
example_label_id_2 = "%_label_2"
example_invalid_label_id = "X_label_2"

example_long_label_name_1 = "BAGGAGE_20210901_064516_00000_label_1"
example_long_label_name_2 = "BAGGAGE_20190719_203712_28467_label_2"


class TestNamingMethods(unittest.TestCase):
    def test_label_short_to_long(self):
        msg = "The long label name does not match!"
        self.assertEqual(label_short_to_long(example_volume_id_1, example_label_id_1), example_long_label_name_1, msg)
        self.assertEqual(label_short_to_long(example_volume_id_2, example_label_id_2), example_long_label_name_2, msg)

    def test_label_long_to_short(self):
        msg = "The short label name does not match!"
        msg_char = "Short id must contain '%' character!"

        short_id_1 = label_long_to_short(example_volume_id_1, example_long_label_name_1)
        self.assertEqual(short_id_1, example_label_id_1, msg)
        self.assertTrue("%" in short_id_1, msg_char)

        short_id_2 = label_long_to_short(example_volume_id_2, example_long_label_name_2)
        self.assertEqual(short_id_2, example_label_id_2, msg)
        self.assertTrue("%" in short_id_1, msg_char)

    def test_label_short_to_long_throws_exception(self):
        self.assertRaises(ValueError, label_short_to_long, example_volume_id_1, example_invalid_label_id)

    def test_label_long_to_short_throws_exception(self):
        self.assertRaises(ValueError, label_long_to_short, example_volume_id_2, example_long_label_name_1)


if __name__ == "__main__":
    unittest.main()
