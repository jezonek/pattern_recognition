import examples
import string
import pprint
# def principal_period(s):
#     i = (s+s).find(s, 1, -1)
#     return None if i == -1 else s[:i]

table= {key:"d" for key in string.digits}
letters_table= {key:"w" for key in string.ascii_letters}
table.update(letters_table)
pprint.pprint(table)
trantab=str.maketrans(table)

for element in examples.exp2:
    print(element.translate(trantab))
