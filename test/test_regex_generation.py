import unittest
import re
from pattern_recognition import first_selection, second_selection

class TestDatesRegexGenerattion(unittest.TestCase):
    files= ["dates"]

    def test_if_regex_matches_every_valid_data(self):
        with open("../datasets/de_ibans.datasets") as opened_file:
            dataset=opened_file.read()
        generated_regex, cleaned, garbage =first_selection(dataset)
        second_cleaned, full_garbage = second_selection(generated_regex, cleaned, garbage)
        for data in second_cleaned:
            self.assertRegex(data,generated_regex)

