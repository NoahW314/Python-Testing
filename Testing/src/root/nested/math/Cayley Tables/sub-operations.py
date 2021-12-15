
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

def print_table(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(table[i][j],end=" ")
        print()
    print()

total_impossible = 0 # not left distributive, associative
total_predicted = 0 # not left distributive, not associative
total_follow = 0 # left distributive, associative
total_break = 0 # left distributive, not associative
total_rdistr = 0 # all left distributive
total_assoc = 0 # all associative
total_tables = 0
def test(m, table):
    global total_tables, total_rdistr, total_break, total_assoc, total_follow, total_predicted, total_impossible
    total_tables += 1
    # Construct the right sub-operation table
    sub_table = []
    for i in range(m):
        sub_table.append([])
        for j in range(m):
            z = table[i].index(j)
            if z == m-1:
                sub_table[-1].append(table[i][0])
            else:
                sub_table[-1].append(table[i][z+1])

    is_rdistr = True
    # the right sub-operation is left distributive if x*(y+z)=(x*y)+(x*z) for all x,y,z
    # the right sub-operation is right distributive if (y+z)*x=(y*x)+(z*x) for all x,y,z
    for i in range(m):
        for j in range(m):
            for k in range(m):
                if table[sub_table[j][k]][i] != sub_table[table[j][i]][table[k][i]]:
                    is_rdistr = False
                    break
            if not is_rdistr:
                break
        if not is_rdistr:
            break
    # check for associativity of *
    is_assoc = True
    for i in range(m):
        for j in range(m):
            for k in range(m):
                # associativity is (x*y)*z = x*(y*z)
                if table[table[i][j]][k] != table[i][table[j][k]]:
                    is_assoc = False
                    break
            if not is_assoc:
                break
        if not is_assoc:
            break

    if is_rdistr:
        total_rdistr += 1
        if is_assoc:
            total_assoc += 1
            total_follow += 1
        else:
            total_break += 1
    else:
        if is_assoc:
            total_assoc += 1
            total_impossible += 1
        else:
            total_predicted += 1





for x in range(2, 5):
    print(str(x)+": ")
    total_impossible = 0  # not left distributive, associative
    total_predicted = 0  # not left distributive, not associative
    total_follow = 0  # left distributive, associative
    total_break = 0  # left distributive, not associative
    total_rdistr = 0  # all left distributive
    total_assoc = 0  # all associative
    total_tables = 0
    start_table = [[-1] * x for j in range(x)]
    lazy_gen_test_tables_rec(x, start_table, (0,0), False, True)
    # Conjecture was: left distributive -> associative
    # Counter examples would be: left distributive, not associative (total_break)
    # Proven: associative -> left distributive
    # Counter examples would be: not left distributive, associative (total_impossible)
    print("Left Distr: "+str(total_rdistr))
    print("Assoc: "+str(total_assoc))
    print("Not Left Distr, Assoc: "+str(total_impossible))
    print("Not Left Distr, Not Assoc: " + str(total_predicted))
    print("Left Distr, Assoc: " + str(total_follow))
    print("Left Distr, Not Assoc: " + str(total_break))
    print("Tables: "+str(total_tables))
    print()