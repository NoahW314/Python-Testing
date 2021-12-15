from collections import deque
from timeit import default_timer as time
from math import lcm

# f = open("Root Tables.txt", 'w')
f = None

# spot is (row, column)
def next_spot(spot, m, sym):
    if spot[1] == m-1:
        if spot[0] == m-1:
            return -1, -1
        elif sym:
            return spot[0]+1, spot[0]+1
        else:
            return spot[0]+1, 0
    elif spot == (-2, -2):
        return 0, 0
    else:
        return spot[0], spot[1]+1

def prev_spot(spot, m, sym):
    if spot[1] == 0:
        if spot[0] == 0:
            return -2, -2
        else:
            return spot[0]-1, m-1
    elif spot == (-1, -1):
        return m-1, m-1
    elif sym and spot[1] == spot[0]:
        return spot[0]-1, m-1
    else:
        return spot[0], spot[1]-1


def allowed_signs(m, table, spot, sym, u_row):
    signs = set(range(m))
    # unique row check
    if u_row:
        row_signs = {table[spot[0]][i] for i in range(m)}
        signs -= row_signs
        # unique column check
        if sym:
            col_signs = {table[i][spot[1]] for i in range(m)}
            signs -= col_signs
    return signs

def generate_tables(m, tables, spot, sym=True, u_row=True):
    if spot == (-1,-1):
        return tables
    filled_tables = []
    for table in tables:
        signs = allowed_signs(m, table, spot, sym, u_row)
        for s in signs:
            table[spot[0]][spot[1]] = s
            if sym:
                table[spot[1]][spot[0]] = s
            filled_tables.append([row.copy() for row in table])
    return generate_tables(m, filled_tables, next_spot(spot, m, sym), sym, u_row)

def lazy_gen_test_tables_rec(m, table, spot, sym=True, u_row=True):
    if spot == (-1,-1):
        test(m, table)
    signs = allowed_signs(m, table, spot, sym, u_row)
    for s in signs:
        table[spot[0]][spot[1]] = s
        if sym:
            table[spot[1]][spot[0]] = s
        lazy_gen_test_tables_rec(m, table, next_spot(spot, m, sym), sym, u_row)
        table[spot[0]][spot[1]] = -1
        if sym:
            table[spot[1]][spot[0]] = -1


def lazy_gen_test_tables(m, sym=True, u_row=True, is_form=False):
    curr_spot = (0, 0)
    start_table = [[-1] * m for j in range(m)]
    if is_form:
        curr_spot = (1, 1)
        # By definition, forms are commutative, so the table is symmetric
        sym = True
        # Similarly, forms are Latin, that is, each row contains each sign once
        u_row = True
        for i in range(m):
            start_table[0][i] = i
            start_table[i][0] = i
    stack = deque([[start_table, allowed_signs(m, start_table, curr_spot, sym, u_row), curr_spot]])
    curr_table = [row.copy() for row in start_table]
    signs = set()
    done = False
    while not done:
        while len(signs) == 0:
            if len(stack) == 0:
                return
            curr = stack.pop()
            curr_table = curr[0]
            signs = curr[1]
            curr_spot = curr[2]
        curr_sign = signs.pop()
        next_table = [row.copy() for row in curr_table]
        next_table[curr_spot[0]][curr_spot[1]] = curr_sign
        if sym:
            next_table[curr_spot[1]][curr_spot[0]] = curr_sign
        curr_spot = next_spot(curr_spot, m, sym)
        if curr_spot == (-1, -1):
            test(m, next_table)
            if len(stack) == 0:
                done = True
        else:
            if len(signs) != 0:
                stack.append([curr_table, signs, prev_spot(curr_spot, m, sym)])
            curr_table = next_table
            signs = allowed_signs(m, curr_table, curr_spot, sym, u_row)

total_tested = 0
non_associative_forms = 0
non_diag_roots = 0
def test(m, table):
    global total_tested, non_diag_roots, non_associative_forms
    total_tested += 1
    # if assoc_check(m, table):
    #     non_associative_forms += 1
    #     if not is_associative(m, table):
    #         print_table(table, False)
    #         assert False
    if is_associative(m, table):
        non_associative_forms += 1
    # if roots_exist(m, table):
    #     non_diag_roots += 1
    #     if is_associative(m, table):
    #         non_associative_forms += 1
    #         f.write("Associative!\n")
    #         print("Associative!")
    #     print_table(table, False, f)
    # loop_size_check(m, table)
    # if print_roots_exist(m, table):
    #     non_diag_roots += 1
    if total_tested%1_000_000 == 0:
        print(str(total_tested)+" in "+str(int((time()-start_time)/60))+" minutes")


symbols = ["+","-","|","/","\\","_"]
def print_table(table, pretty=True, file=None):
    if len(table) > len(symbols):
        pretty = False
    for i in range(len(table)):
        for j in range(len(table[i])):
            if pretty:
                print(symbols[table[i][j]], end=" ")
            else:
                if file is not None:
                    file.write(str(table[i][j])+" ")
                print(table[i][j],end=" ")
        if file is not None:
            file.write("\n")
        print()
    if file is not None:
        file.write("\n")
    print()

def make_tables_hashable(tables):
    return {tuple(tuple(table[i]) for i in range(len(table))) for table in tables}


def is_associative(m, table):
    # check that (a*b)*c=a*(b*c) for all a,b,c
    for a in range(m):
        for b in range(m):
            for c in range(m):
                side1 = table[table[a][b]][c]
                side2 = table[a][table[b][c]]
                if side1 != side2:
                    return False
    return True


def assoc_check(m, table):
    for a in range(m):
        for n in range(m):
            side1 = table[table[a][a]][n]
            side2 = table[table[a][n]][a]
            if side1 != side2:
                return False
    return True

def roots_exist(m, table):
    last_values = {s : s for s in range(m)}
    # TODO: This many loops could be really slow if intend to do more testing for higher m values
    # Doing an initial test up to m or 2*m or something like that might be good.
    # Then we can take a file containing all the ones that pass this test and test them with the full test
    # It is also likely that this function contributes very little to the overall time of checking the tables,
    # so this may not be needed
    for i in range(2, lcm(*[j for j in range(m+1)])+1):
        next_values = {s: table[last_values[s]][s] for s in range(m)}
        if len(set(next_values.values())) != m:
            return False
        last_values = next_values.copy()
    return True

loop_values = [0]*5
loop_value_distributions = {}
perm_distributions = {}
def print_roots_exist(m, table):
    values = [{s: s for s in range(m)}]
    for i in range(2, lcm(*[j for j in range(m+1)]) + 1):
        next_values = {s: table[values[-1][s]][s] for s in range(m)}
        if len(set(next_values.values())) != m:
            return False
        values.append(next_values)

    # for i in range(len(table)):
    #     for j in range(len(table[i])):
    #             print(table[i][j],end=" ")
    #     print(" ", end=" ")
    #     for j in range(m):
    #         print(values[j][i], end=" ")
    #     print()
    # print()
    #
    # num_4length_loops = 0
    # for i in range(m):
    #     loop_length = len({values[j][i] for j in range(m)})
    #     if loop_length == 4:
    #         num_4length_loops += 1
    # assert num_4length_loops == 0 or num_4length_loops == m



    return True

# we are looking at the distribution of loop sizes
def loop_size_check(m, table):
    # looking for two elements, x and z, such that [[x,z],z]=x, where x\not=z
    has_two_loop = False
    for x in range(m):
        for z in set(range(m))-{x}:
            if table[table[x][z]][z] == x:
                has_two_loop = True
                return
    if not has_two_loop:
        print_table(table, pretty=False)

    # values = [{s: s for s in range(m)}]
    # for i in range(2, m+1):
    #     next_values = {s: table[values[-1][s]][s] for s in range(m)}
    #     values.append(next_values)
    #
    # table_loop_values = []
    # for i in range(m):
    #     loop_length = len({values[j][i] for j in range(m)})
    #     table_loop_values.append(loop_length)
    #
    # distribution = [0]*(m+1)
    # for value in table_loop_values:
    #     distribution[value] += 1
    #
    # t_distr = tuple(distribution)
    # if t_distr in loop_value_distributions:
    #     loop_value_distributions[t_distr] += 1
    # else:
    #     loop_value_distributions[t_distr] = 1

def quasi_diagonal(m, table):
    offset = table[0][0]
    for i in range(m):
        if (i+offset)%m != table[i][i]:
            return False
    return True

def diagonal(m, table):
    for i in range(m):
        if i != table[i][i]:
            return False
    return True


def test_all(m):
    if m <= 0:
        return
    base_table = [[-1]*m for j in range(m)]
    unhashable_tables = generate_tables(m, [base_table], (0,0), is_commutative, True)
    tables = make_tables_hashable(unhashable_tables)

    print("Testing... ")
    # associative = set()
    # poss_assoc = set()
    # roots = set()
    # n_diag = set()
    for table in tables:
        assert is_associative(m, table) == assoc_check(m, table)
        # if is_associative(m, table):
        #     associative.add(table)
        # if assoc_check(m, table):
        #     poss_assoc.add(table)
        # if roots_exist(m, table):
        #     roots.add(table)
        #     if not_diagonal(m, table):
        #         n_diag.add(table)

    # both = associative & roots
    # a_n_diag = associative & n_diag
    # associative_non_poss = associative-poss_assoc
    # non_assoc_poss = poss_assoc-associative
    print("Tables: "+str(len(tables)))
    # print("Assoc: "+str(len(associative)))
    # print("Poss Assoc: "+str(len(poss_assoc)))
    # print("Assoc Non-Poss: "+str(len(associative_non_poss)))
    # print("Non-Assoc Poss: "+str(len(non_assoc_poss)))
    # print("Roots: "+str(len(roots)))
    # print("Both: "+str(len(both)))
    # print("No Diagonal: "+str(len(n_diag)))
    # print("A No Diag: "+str(len(a_n_diag)))
    # for table in associative:
    #     print_table(table)
    # for table in a_n_diag:
    #     print(table)
    print()


is_commutative = False
Latin = True

for x in range(1, 7):
    # if x%2 == 0:
    #     continue
    start_time = time()
    print(x)

    if f is not None:
        f.write(str(x)+"\n")
    total_tested = 0
    non_diag_roots = 0
    non_associative_forms = 0
    start_table = [[-1] * x for j in range(x)]
    lazy_gen_test_tables_rec(x, start_table, (0,0), is_commutative, Latin)
    # lazy_gen_test_tables(x, is_commutative, Latin)
    print("Tables: "+str(total_tested))
    print("Associativity: "+str(non_associative_forms))
    print("Roots: "+str(non_diag_roots))

    if f is not None:
        f.write("Tables: " + str(total_tested)+"\n")
        f.write("Roots and Associativity: " + str(non_associative_forms)+"\n")
        f.write("Roots: " + str(non_diag_roots)+"\n")
    end_time = time()
    print(end_time - start_time)
    print()

# for distr, freq in loop_value_distributions.items():
#     print(str(distr)+": "+str(freq))

if f is not None:
    f.close()
# start_time = time()
# for x in range(4, 5):
#     print(x)
#     test_all(x)
# end_time = time()
# print(end_time-start_time)
