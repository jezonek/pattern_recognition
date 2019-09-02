import unittest
import re
from pattern_recognition import first_selection, second_selection, transpose_string_matrix, calculate_propabilities, \
    count_chars, decide_of_char, create_regex


class TestDatesRegexGenerattion(unittest.TestCase):
    def test_if_regex_matches_every_valid_data(self):
        with open("../datasets/de_ibans.datasets") as opened_file:
            dataset = opened_file.read()
        cleaned, garbage = first_selection(dataset)
        main_array = transpose_string_matrix(cleaned)
        list_of_propably_types = [
            calculate_propabilities(count_chars(row)) for row in main_array
        ]
        regex_list = [decide_of_char(place) for place in list_of_propably_types]
        final_regex = create_regex(regex_list)
        second_cleaned, full_garbage = second_selection(final_regex, cleaned, garbage)
        for data in second_cleaned:
            self.assertRegex(data, final_regex)
