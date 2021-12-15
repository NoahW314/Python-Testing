from timeit import default_timer as time
from itertools import permutations

def print_table(table):
    for x in range(len(table)):
        for y in range(len(table[x])):
            print(table[x][y],end=" ")
        print()
    print()

# we assume that the table is commutative and Latin
def allowed_signs(m, table, spot, row_only=False):
    signs = set(range(m))
    row_signs = {table[spot[0]][j] for j in range(m) if j != spot[1]}
    signs -= row_signs
    if not row_only:
        col_signs = {table[j][spot[1]] for j in range(m) if j != spot[0]}
        signs -= col_signs

    # odd tables can't have repeats on the diagonal
    if m%2 == 1 and spot[0] == spot[1]:
        diag_signs = {table[j][j] for j in range(m) if j != spot[0]}
        signs -= diag_signs

    return signs

def generate_derangements(m, used, remaining_hats, remaining_people):
    if m == 0:
        yield used
    elif m == 1:
        return
    else:
        for i in range(1, len(remaining_hats)):
            # First assign a hat i to person 0 (where i\not=0)
            used[remaining_people[0]] = remaining_hats[i]
            # Next assign any hat to person i
            # If this hat is hat 0, then the problem is reduced to m-2 people and m-2 hats
            used[remaining_people[i]] = remaining_hats[0]
            next_people = [remaining_people[j] for j in range(m) if j != 0 and j != i]
            next_hats = [remaining_hats[j] for j in range(m) if j != 0 and j != i]
            yield from generate_derangements(m-2, used, next_hats, next_people)
            # Otherwise, the problem is reduced to m-1 people and m-1 hats
            next_people = [remaining_people[j] for j in range(m) if j != 0]
            next_hats = []
            for j in range(m):
                if j != i and j != 0:
                    next_hats.append(remaining_hats[j])
                elif j == i:
                    next_hats.append(remaining_hats[0])
            yield from generate_derangements(m-1, used, next_hats, next_people)

def generate_perms(m, used, remaining_hats, remaining_people):
    return permutations(range(m))

# we assume that the table is commutative and Latin
def gen_weak_assoc_table(m, table, filled_cols, col, col_filled=False):
    if len(filled_cols) == m:
        test(m, table)
        increment_ends(0)
    elif col_filled:
        # here is where we make use of the weak associativity
        next_col = table[col][col]
        set_spots = set()
        for j in range(m):
            signs = allowed_signs(m, table, (j, next_col))
            if table[j][next_col] == -1:
                if table[col][table[col][j]] not in signs:
                    for spot in set_spots:
                        table[spot][next_col] = -1
                        table[next_col][spot] = -1
                    increment_ends(2)
                    return
                table[j][next_col] = table[col][table[col][j]]
                table[next_col][j] = table[col][table[col][j]]
                set_spots.add(j)
            elif table[j][next_col] != table[col][table[col][j]]:
                for spot in set_spots:
                    table[spot][next_col] = -1
                    table[next_col][spot] = -1
                increment_ends(3)
                return
        new_filled_cols = filled_cols | {next_col}
        if len(set_spots) == 0:
            gen_weak_assoc_table(m, table, new_filled_cols, -1)
        else:
            gen_weak_assoc_table(m, table, new_filled_cols, next_col, col_filled=True)
            for spot in set_spots:
                table[spot][next_col] = -1
                table[next_col][spot] = -1
    else:
        if col == -1:
            for j in range(m):
                if j not in filled_cols:
                    col = j
                    break

        # """
        empty_rows = {r for r in range(m) if table[r][col] == -1}
        for der in generate_perms(m, {}, list(range(m)), list(range(m))):
            is_valid = True
            for row in range(m):
                if table[row][col] == -1:
                    signs = allowed_signs(m, table, (row, col), row_only=True)
                    if der[row] not in signs:
                        is_valid = False
                        break
                    table[row][col] = der[row]
                    table[col][row] = der[row]
                elif der[row] != table[row][col]:
                    is_valid = False
                    break
            if is_valid:
                new_filled_cols = filled_cols | {col}
                gen_weak_assoc_table(m, table, new_filled_cols, col, col_filled=True)
                for row in empty_rows:
                    table[row][col] = -1
                    table[col][row] = -1
        for row in empty_rows:
            table[row][col] = -1
            table[col][row] = -1
        # """
        """
        # find the first empty row in this col
        row = -1
        # we prioritize the diagonal, because if [x,x]=x, then x is the identity element, so the column will be determined
        if table[col][col] == -1:
            row = col
        else:
            for j in range(m):
                if table[j][col] == -1:
                    row = j
                    break
        if row == -1:
            new_filled_cols = filled_cols | {col}
            gen_weak_assoc_table(m, table, new_filled_cols, col, col_filled=True)
        else:
            signs = allowed_signs(m, table, (row, col))
            for s in signs:
                table[row][col] = s
                table[col][row] = s
                gen_weak_assoc_table(m, table, filled_cols, col)
                table[row][col] = -1
                table[col][row] = -1
            if len(signs) == 0:
                increment_ends(1)
        """

total_ends = 0
ends = [0,0,0,0]
def increment_ends(end_type):
    global total_ends, total_counted
    total_ends += 1
    ends[end_type] += 1
    """
    0 is table tested
    1 is no permissible signs (fails latin test)
    2 is sign demanded by weak associativity fails latin
    3 is current element fails weak associativity
    """
    if total_ends % 100_000 == 0:
        print("Ends: "+str(ends)+"  Tested: "+str(total_counted)+"  "+str(int(time()-start_time))+" seconds")

total_counted = 0
weakly_assoc = 0
non_assoc = 0
table_print = False
def test(m, table):

    global total_counted, weakly_assoc, non_assoc, table_print
    # if not table_print and table[1][1] == 2:
    #     print(total_counted)

    total_counted += 1
    if assoc_check(m, table):
        weakly_assoc += 1
        if not is_associative(m, table):
            non_assoc += 1
            assert False
    # else:
    #     print_table(table)
    # if total_counted % 100 == 0:
    #     print(str(total_counted)+" in "+str(int((time()-start_time)))+" seconds")
        # print(time()-start_time)
        # print("Non-associative: "+str(non_assoc))

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

""" We have verified the conjecture that associativity is equivalent to weak associativity for m<=9.
However for m=10, the conjecture is false.  There are 8400 non-associative tables.
Strangely for m=11, the conjecture still holds."""

"""Oddly enough though, we haven't found any of these tables for m=11,12,13.
This could be because I haven't looked much, but they were easy to find for m=10, so this seems odd.
For m>=12, this could be because the algorithm is running really slowly.  It took 97 seconds to check just 100 tables.
My guess is that this is because the algorithm gets deep into constructing a table only to find out that it is already flawed.
It is also possible that there is something going on with the first few tables in particular, as even for m=10,11 the algorithm
seems to be taking several times longer to test the first 10,000 tables than later 10,000 tables.
The algorithm speeds up when going from [1,1]=0 to [1,1]=2, but I still don't know why."""

"""The problem with the algorithm is that many tables are started to be constructed but ultimately turn out to be contradictory.
There are two main reasons for the contradictory.  First, we encounter spots that have no possible signs that meet the Latin requirements
Second, we encounter spots where the current sign is not compatible with weak associativity.
We had 1 million of each contradiction by the time that we had reached just 64 weakly associative tables.

The first problem: Latin contradictions
We need to generate a permutation (actually a derangement) for the whole row instead of doing it piecewise.
Current Latin contradictions (starting at 2):
0,0,1,2,85,44,11285,17814
"""

"""
1.05
3.7
"""
for i in range(2, 6):
    print(str(i)+": ")
    start_time = time()
    total_counted = 0
    total_ends = 0
    ends = [0,0,0,0]
    weakly_assoc = 0
    start_table = [[-1]*i for j in range(i)]
    # WLOG, we can make the first col the identity element (this must exist because of weak associativity and commutativity)
    for j in range(i):
        start_table[0][j] = j
        start_table[j][0] = j
    gen_weak_assoc_table(i, start_table, {0}, 1, False)
    end_time = time()
    print("Weakly Associative: "+str(weakly_assoc))
    print("Weakly Assoc non-Assoc: "+str(non_assoc))
    print("Tables: "+str(total_counted))
    print("Ends: " + str(ends))
    print(end_time-start_time)
    print()

"""
Rates of generation: (in tables/s)
2: 26247
3: 13819
4: 10826
5: 4414
6: 4020
7: 2044 
8: 1775
9: 727
10: 640 
11: 
"""