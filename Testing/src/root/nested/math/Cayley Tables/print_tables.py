from ast import literal_eval as make_tuple

symbols = ["+", "-", "|", "/"]

def print_tables(tables):
    for table in tables:
        for row in table:
            for spot in row:
                print(symbols[spot], end=" ")
            print()
        print()

tables_f = open("Tables.txt")
tables_c_f = open("Tables_C.txt")

comm_tables = [set() for i in range(5)]
non_comm_tables = [set() for j in range(5)]
indices = []
index = 1
for line in tables_c_f:
    if line[0] == "(":
        t_table = make_tuple(line)
        comm_tables[index].add(t_table)
    else:
        index = int(line.split(",")[0])
        indices.append((index, int(line.split(",")[1])))

for ind in indices:
    print(ind)
    print_tables(comm_tables[ind[0]])
    print()

print()
print()

indices = []
index = -1
for line in tables_f:
    if line[0] == "(":
        t_table = make_tuple(line)
        non_comm_tables[index].add(t_table)
    else:
        index = int(line.split(",")[0])
        indices.append((index, int(line.split(",")[1])))

for ind in indices:
    print()
    non_comm_tables[ind[0]] -= comm_tables[ind[0]]
    print_tables(non_comm_tables[ind[0]])
    print()