from itertools import permutations
from tabulate import tabulate


def kmap(table_values):
    kmap_values = [[0, 0, " ", 0, 0], [0, 0, " ", 0, 0], [0, 0, " ", 0, 0], [0, 0, " ", 0, 0]]
    for l in range(0, 2):
        for i in range(0, len(table_values[l])):
            j = 0 if i < 4 else 1
            if i == 2 or i == 6:
                kmap_values[i % 4][j + l * 3] = table_values[l][i + 1]
            elif i == 3 or i == 7:
                kmap_values[i % 4][j + l * 3] = table_values[l][i - 1]
            else:
                kmap_values[i % 4][j + l * 3] = table_values[l][i]

    return kmap_values


perms = list(permutations(["00", "01", "10", "11"]))
truth_table_format = [2, None, 1, 3, 0, None, 0, 0, 0]
truth_tables = []

for perm in perms:
    truth_table = [[], []]
    for i in range(0, 2):
        for index in truth_table_format:
            if index is None:
                truth_table[i].append("X")
            else:
                truth_table[i].append(perm[index][i])
    truth_tables.append(truth_table)

# for i in range(0, len(truth_tables)):
#     print(i)
#     print(tabulate(kmap(truth_tables[i])))

print(perms[4])
print(tabulate(kmap(truth_tables[4])))
