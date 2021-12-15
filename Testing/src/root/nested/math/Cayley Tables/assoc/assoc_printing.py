import sys
from ast import literal_eval

sign_symbols = ["x","y","z","w","v","u"]
unknown3_symbols = ["a","b","c","d","e","f"]
unknown2_symbols = ["l","p","q","r","s","t"]

for line in sys.stdin:
    splitted = line.rstrip().split("): ")
    print(splitted[0]+")")
    print(splitted[1])
    statements = literal_eval(splitted[0]+")")
    cases = literal_eval(splitted[1])
    for statement in statements:
        print("".join(sign_symbols[i] for i in statement), end=", ")
    print()
    for case in cases:
        for unknown, sign in case.items():
            if isinstance(unknown, int):
                index = -unknown-1
                print(unknown3_symbols[index], end="=")
            else:
                index = -int(unknown)-1
                print(unknown2_symbols[index], end="=")
            print(sign_symbols[sign], end=", ")
        print()
