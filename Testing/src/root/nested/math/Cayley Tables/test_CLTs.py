from math import lcm


def roots_exist(m, table):
    last_values = {s : s for s in range(m)}
    for i in range(2, lcm(*[j for j in range(m+1)])+1):
        next_values = {s: table[last_values[s]][s] for s in range(m)}
        if len(set(next_values.values())) != m:
            return False
        last_values = next_values.copy()
    return True

def print_roots_exist(m, table):
    values = [{s: s for s in range(m)}]
    for i in range(2, lcm(*[j for j in range(m+1)]) + 1):
        next_values = {s: table[values[-1][s]][s] for s in range(m)}
        if len(set(next_values.values())) != m:
            return False
        values.append(next_values)

    for i in range(len(table)):
        for j in range(len(table[i])):
                print(table[i][j],end=" ")
        print(" ", end=" ")
        for j in range(m):
            print(values[j][i], end=" ")
        print()
    print()

    num_4length_loops = 0
    for i in range(m):
        loop_length = len({values[j][i] for j in range(m)})
        if loop_length == 4:
            num_4length_loops += 1
    assert num_4length_loops == 0 or num_4length_loops == m

    return True

def print_table(table, file=None):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if file is not None:
                file.write(str(table[i][j]) + " ")
            print(table[i][j], end=" ")
        if file is not None:
            file.write("\n")
        print()
    if file is not None:
        file.write("\n")
    print()

repeators = 0
loop_values = [0]*7
loop_value_distributions = {}
perm_distributions = {}
def test(m, table):
    global repeators, loop_values, loop_value_distributions
    values = [{s: s for s in range(m)}]
    for i in range(2, 14):
        next_values = {s: table[values[-1][s]][s] for s in range(m)}
        if len(set(next_values.values())) != m:
            return False
        values.append(next_values)

    # num_4length_loops = 0
    # for i in range(m):
    #     loop_length = len({values[j][i] for j in range(m)})
    #     if loop_length == 4:
    #         num_4length_loops += 1

    # table_loop_values = []
    # for i in range(m):
    #     loop_length = len({values[j][i] for j in range(m)})
    #     loop_values[loop_length] += 1
    #     table_loop_values.append(loop_length)
    #
    # distribution = [0]*m
    # for value in table_loop_values:
    #     distribution[value] += 1
    # t_distr = tuple(distribution)
    # if t_distr in loop_value_distributions:
    #     loop_value_distributions[t_distr] += 1
    # else:
    #     loop_value_distributions[t_distr] = 1

    # perm = tuple(values[1][i] for i in range(m))
    # if perm in perm_distributions:
    #     perm_distributions[perm] += 1
    # else:
    #     perm_distributions[perm] = 1

    # repeat = True
    # for i in range(m):
    #     if i != values[-1][i]:
    #         repeat = False
    #         break
    # if repeat:
    #     repeators += 1

    return True

with open("Root Tables.txt") as f:
    first_line = f.readline().rstrip()
    print(first_line)
    x = int(first_line[-1])
    t = [[-1]*x for j in range(x)]
    row = 0
    table_num = 0
    for line in f:
        if line == "\n":
            assert test(x, t)
            row = 0
            table_num += 1
        else:
            t[row] = [int(c) for c in line.rstrip().split(" ")]
            row += 1

# print(repeators)
# print(table_num)
# print(loop_values)
# for distr, freq in loop_value_distributions.items():
#     print(str(distr)+": "+str(freq))
# distribution_distributions = {}
# for distr, freq in perm_distributions.items():
#     if freq in distribution_distributions:
#         distribution_distributions[freq] += 1
#     else:
#         distribution_distributions[freq] = 1
# for distr, freq in distribution_distributions.items():
#     print(str(distr)+": "+str(freq))
# print()
# for distr, freq in perm_distributions.items():
#     if freq != 3:
#         print(str(distr)+": "+str(freq))