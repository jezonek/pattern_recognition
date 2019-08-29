import examples
import string
import pprint
import operator
from itertools import zip_longest


def count_chars(row):
    result = {}
    #TODO dla kazdego znaku w kolumnie:
    # okreslic typ by nie liczyc niepotrzebnych prawdopodobienstw
    # sprawdzic czy byl on juz brany do liczenia  : jezeli tak to dodac 1 do danego elementu jezeli nie to dodac element z wartoscia 1
    for element in row:
        if element not in result.keys():
            result.update({element:row.count(element)})
    result.update({"_all":len(row)})
    # for char in result:
    #     result[char]=result[char]/all_elements
    # for digit in string.digits:
    #     result.update(
    #         {"{}".format(digit): row.count("{}".format(digit)) / all_elements}
    #     )
    # for letter in string.ascii_letters:
    #     result.update(
    #         {"{}".format(letter): row.count("{}".format(letter)) / all_elements}
    #     )
    # for extra_char in string.punctuation:
    #     result.update(
    #         {"{}".format(extra_char): row.count("{}".format(extra_char)) / all_elements}
    #     )
    return result

def calculate_propablities(row):
    output={}
    print(row.keys())
    for element in row.keys():
        if element is not "_all":
            output.update({element:row[element]/row["_all"]})

    return output


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
    for row in cleaned:
        chars.append(list(row))
    return list(zip_longest(*chars))



if __name__ == "__main__":
    with open("datasets/de_ibans.datasets", "r") as opened_file:
        datas = opened_file.read()
    cleaned, garbage = split_data_in_clean_and_garbage(
        datas, choose_most_common_length_of_data(find_lengths_spotted_in(datas))
    )
    pprint.pprint("Data excluded from analisys:{}".format(garbage))



    main_array = transpose_string_matrix(cleaned)
    # pprint.pprint(main_array)
    list_of_propably_types = [calculate_propablities(count_chars(row)) for row in main_array]
    pprint.pprint(list_of_propably_types)
