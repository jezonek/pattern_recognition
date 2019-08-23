import examples
import string
import pprint
from itertools import zip_longest



def calculate_propablity_of_type(row):
    result={}
    all_elements=len(row)
    for digit in string.digits:
        result.update({"{}".format(digit):row.count("{}".format(digit))/all_elements})
    for letter in string.ascii_letters:
        result.update({"{}".format(letter): row.count("{}".format(letter)) / all_elements})
    for extra_char in string.punctuation:
        result.update({"{}".format(extra_char): row.count("{}".format(extra_char)) / all_elements})
    return result

chars=[]
for row in examples.exp1:
    chars.append(list(row))

main_array=list(zip_longest(*chars))
pprint.pprint(main_array)
list_of_propably_types=[calculate_propablity_of_type(row) for row in main_array]
pprint.pprint(list_of_propably_types)

