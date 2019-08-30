import examples
import string
import pprint
import operator
from itertools import zip_longest, takewhile
from collections import deque


def count_chars(row):
    result = {}
    for element in row:
        if element not in result.keys():
            result.update({element: row.count(element)})
    result.update({"_all": len(row)})
    return result


def calculate_propablities(row):
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
    candidates = []
    for candidate in place_candidats.keys():
        if (
            candidate is not ("\d" or "\w" or "\W")
            and place_candidats[candidate] >= 0.99
        ):
            return candidate
        if candidate not in ["\d", "\w", "\W"] and place_candidats[candidate] >= 0.30:
            candidates.append(candidate)

    if candidates:
        return candidates
    else:
        for candidate in place_candidats.keys():
            if place_candidats[candidate] >= 0.9:
                return candidate

    return "\."



def find_repetions(regex_list):
    for element in enumerate(regex_list):
        count=1
        for one_try in takewhile(lambda x: x==element[1],regex_list[(element[0]+1):]):
            count=count+1
        yield count








def find_lengths_spotted_in(data):
    found_length_values = {}
    for line in data.splitlines():
        if len(line) not in found_length_values.keys():
            found_length_values.update({len(line): 1})
        else:
            found_length_values[len(line)] += 1
    return found_length_values


def choose_most_common_length_of_data(counted_spots):
    return max(counted_spots.items(), key=operator.itemgetter(1))[0]


def split_data_in_clean_and_garbage(dataset, most_common_length):
    final_data = []
    garbage = []
    for element in dataset.splitlines():
        if len(element) == most_common_length:
            final_data.append(element)
        else:
            garbage.append(element)
    return final_data, garbage


def transpose_string_matrix(list_of_strings):
    chars = []
    for row in list_of_strings:
        chars.append(list(row))
    return list(zip_longest(*chars))


def main():
    with open("datasets/exp2.datasets", "r") as opened_file:
        datas = opened_file.read()
    cleaned, garbage = split_data_in_clean_and_garbage(
        datas, choose_most_common_length_of_data(find_lengths_spotted_in(datas))
    )
    pprint.pprint("Data excluded from analisys:{}".format(garbage))

    main_array = transpose_string_matrix(cleaned)
    list_of_propably_types = [
        calculate_propablities(count_chars(row)) for row in main_array
    ]
    pprint.pprint(list_of_propably_types)
    regex_list=[decide_of_char(place) for place in list_of_propably_types]
    pprint.pprint(regex_list)
    for element in find_repetions(regex_list):
        print(element)


if __name__ == "__main__":
    main()
