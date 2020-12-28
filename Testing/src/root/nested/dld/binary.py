import random

hexadecimal_lookup = {
    "0000": 0,
    "0001": 1,
    "0010": 2,
    "0011": 3,
    "0100": 4,
    "0101": 5,
    "0110": 6,
    "0111": 7,
    "1000": 8,
    "1001": 9,
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F"
}
print("")
binary1 = list(hexadecimal_lookup.keys())[:]
binary2 = binary1[:]
random.shuffle(binary1)
random.shuffle(binary2)
for b in binary1:
    print(b)
    print(hexadecimal_lookup[b])
for b in binary1:
    print(b)
    print(hexadecimal_lookup[b])
