import string
import pprint
import operator
import re
from itertools import zip_longest, takewhile
from collections import defaultdict


def count_chars(row):
    """The function counts the occurrence of each character in a given place
    :param row: Place in origin string
    :type list
    :return: Dictionary in the form of {char:the sum of the occurrences of the char}
    :rtype dict
    """
    result=defaultdict()
    result= {element: row.count(element) for element in row if element not in result.keys()}
    result.update({"_all": len(row)})
    return result


def calculate_propabilities(row):
    """The function calculates the probability of characters occurrence for a given column and which
    group (digit, letter, punctuation) appears most frequently on a given place
    :param row: The occurrence of characters
    :type dict
    :return: dict: Calculated propabilities
    :rtype: dict
    """

    output = {}
    for element in row.keys():
        if element is not "_all":
            output.update({element: row[element] / row["_all"]})
            if element in string.digits:
                if "\d" in output.keys():
                    output["\d"] = output["\d"] + (row[element] / row["_all"])
                else:
                    output["\d"] = row[element] / row["_all"]
            if element in string.ascii_letters:
                if "\w" in output.keys():
                    output["\w"] = output["\w"] + (row[element] / row["_all"])
                else:
                    output["\w"] = row[element] / row["_all"]
            if element in string.punctuation:
                if "\W" in output.keys():
                    output["\W"] = output["\W"] + (row[element] / row["_all"])
                else:
                    output["\W"] = row[element] / row["_all"]
    return output


def decide_of_char(place_candidats):
    """The function decides whether there is a specific character, a pair of characters or a group on a given position.
    :param place_candidats: Propabilities of the occurrence of an object
    :type dict
    :rtype: str
    """
    candidates = []
    for candidate in place_candidats.keys():
        if (
            candidate is not ("\d" or "\w" or "\W")
            and place_candidats[candidate] >= 0.98
        ):
            return candidate

    if candidates:
        return candidates
    else:
        for candidate in place_candidats.keys():
            if place_candidats[candidate] >= 0.9:
                return candidate

    return "\."


def find_repetitions(regex_list):
    """For each character in the list, the generator calculates successive occurrences
    :param regex_list: List of consecutive objects in estimated regex
    :type list
    :return: Subsequent occurrences of a character
    :rtype: int
    """
    for element in enumerate(regex_list):
        count = 0
        for one_try in takewhile(
            lambda x: x == element[1], regex_list[(element[0] + 1) :]
        ):
            count = count + 1
        yield count


def create_regex(regex_list):
    """For a given list, it combines successive occurrences into one
    :param regex_list: List containing recurring occurrences
    :return:Final regex
    :rtype: str
    """
    content = []
    repetitions = list(zip_longest(regex_list, find_repetitions(regex_list)))
    waiter = 0
    for element in repetitions:
        if waiter > 0:
            waiter = waiter - 1
            continue
        if element[1] > 0:
            content.append(element[0])
            content.append("{" + str(element[1] + 1) + "}")
            waiter = element[1]
        else:
            content.append(element[0])
    return """^{}$""".format("".join(content))


def find_lengths_spotted_in(data):
    """Finds out how long the strings in a dataset are.
    :param data: whole dataset
    :type str
    :return: Dictionary in form {Length of string: Number of occurrences}
    :rtype: dict
    """
    found_length_values = {}
    for line in data.splitlines():
        if len(line) not in found_length_values.keys():
            found_length_values.update({len(line): 1})
        else:
            found_length_values[len(line)] += 1
    return found_length_values


def choose_most_common_length_of_data(counted_spots):
    """Chooses which lenght of string is most common
    :param counted_spots: Dictionary of occurrence of length data
    :return: Most common length of string
    :rtype: str
    """
    return max(counted_spots.items(), key=operator.itemgetter(1))[0]


def split_data_in_clean_and_garbage(dataset, most_common_length):
    """Using the most common length filters out mismatched data

    :param dataset: All data
    :type str
    """
    final_data = []
    garbage = []
    for element in dataset.splitlines():
        if len(element) == most_common_length:
            final_data.append(element)
        else:
            garbage.append(element)
    return final_data, garbage


def transpose_string_matrix(list_of_strings):
    """Transpose matrix of all chars
    :param list_of_strings: List of given data
    :return:
    """
    chars = []
    for row in list_of_strings:
        chars.append(list(row))
    return list(zip_longest(*chars))


def first_selection(dataset):
    """For given dataset generates regex and makes first selection, based on string length
    :param dataset: Dataset, in which each record is in a new line
    :return: Regex
    :rtype: str
    :return: Pre-cleaned data
    :rtype: list
    :return: Initially rejected data
    :rtype: list
    """
    cleaned, garbage = split_data_in_clean_and_garbage(
        dataset, choose_most_common_length_of_data(find_lengths_spotted_in(dataset))
    )
    pprint.pprint("Data excluded from analisys (first selection):{}".format(garbage))

    return cleaned, garbage


def second_selection(final_regex, cleaned, garbage):
    """Using the generated regex, it complements the set of rejected data with those that do not meet the requirements
    :param final_regex: Generated regex
    :type str
    :param cleaned: Cleaned dataset
    :type list
    :param garbage: Rejected dataset
    :type list
    :return: New cleaned dataset
    :rtype: list
    :return: New rejected dataset
    :rtype: list
    """
    regex = re.compile(final_regex)
    new_cleaned = []
    for data in cleaned:
        if regex.match(data) is None:
            garbage.append(data)
        else:
            new_cleaned.append(data)
    pprint.pprint("Data excluded from analisys (second selection):{}".format(garbage))
    return new_cleaned, garbage


def main(input_data_filename):
    with open(input_data_filename, "r") as opened_file:
        dataset = opened_file.read()
    cleaned, garbage = first_selection(dataset)
    main_array = transpose_string_matrix(cleaned)
    list_of_propably_types = [
        calculate_propabilities(count_chars(row)) for row in main_array
    ]
    regex_list = [decide_of_char(place) for place in list_of_propably_types]
    final_regex = create_regex(regex_list)
    print('''Regex: r"{}"'''.format(final_regex))
    second_cleaned, full_garbage = second_selection(final_regex, cleaned, garbage)


if __name__ == "__main__":
    main(input_data_filename="datasets/de_ibans.datasets")
