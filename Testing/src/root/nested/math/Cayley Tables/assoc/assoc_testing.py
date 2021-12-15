from timeit import default_timer as time
"""
Basic Plan:
Use a list (probably 2d, maybe 3d if needed?) to represent the table
Signs will be designated by integers from 0 to m-1, this way the sign corresponds to the table index
The table contents will be strings "1", "2", etc.  "0" will indicate no value.
The table contents aren't directly relatable to the signs, so these will help avoid confusion.
We check for contradictions by ensuring that the table is still commutative and Latin. (Commutative probably isn't necessary.)

We will test using statements of the form [[x,y],a]=[x,[y,z]].  There are m*(m-1)*(m-2) statements of this form.
WLOG let [[x,y],a]=[x,[y,z]] be the first statement we select.
We then select n-1 more of these per test, so there are C(m*(m-1)*(m-2)-1,n-1) tests we could run.
For n=m*(m-1)*(m-2), there are C(m*(m-1)*(m-2)-1,m*(m-1)*(m-2)-1) =  1 test to run.
For m=5,n=2 there are C(5*4*3-1,1)=C(59,1) =  59 tests to run.
For m=6,n=2 there are C(6*5*4-1,1)=C(119,1) =  119 tests to run.
For m=6,n=3 there are C(6*5*4-1,2)=C(119,2)=119*118/2 =  7021 tests to run.
For m=6,n=4 there are C(6*5*4-1,3)=C(119,3)=119*118*117/6 =  273,819 tests to run.
For m=6,n=5 there are C(6*5*4-1,4)=C(119,4)=119*118*117*116/24 =  7,940,751 tests to run.
For m=7,n=4 there are C(7*6*5-1,3)=C(209,3)=209*208*207/6 =  1,499,784 tests to run.
Each of these statements will be accompanied by a similar statement of this form [y,z]=[a,j] (or [x,y]=[a,k], though this is a secondary test, only if needed).


Our goal is to find a group of these statements that ensure a contradiction whenever a is not z.
Ideally, we want the minimum number of statements required and hope to find a pattern among those chosen.
"""
"""
m=4:
    n=1: 24/24  1/24
m=5:
    n=1: 0/60
    n=2: 480/1770  15/1770
m=6:
    n=2: 0/119
    n=3: 0/7021
    n=4: 0/273,819
    n=5: 0/7,840,751
"""

sign_symbols = ["x","y","z","w","v","u"]
unknown3_symbols = ["a","b","c","d","e","f"]
unknown2_symbols = ["l","p","q","r","s","t"]
m = 6 # number of signs
n = 3 # number of statements to select
possible_statements = []
working_statements = []
num_tested = 0


def generate_possible_statements():
    for i in range(m):
        for j in set(range(m)) - {i}:
            for k in set(range(m)) - {i, j}:
                possible_statements.append((i, j, k))

def generate_and_test_combinations(num_left, statements, index):
    if num_left == 0:
        test_statements(statements)
    else:
        for i in range(index+1, len(possible_statements)-num_left+1):
            new_statements = statements.copy()
            new_statements.append(possible_statements[i])

            generate_and_test_combinations(num_left-1, new_statements, i)

def test_statements(statements):
    global num_tested
    num_tested += 1
    statement_signs = {i: {statements[i][j] for j in range(3)} for i in range(n)}
    # values -1,-2,-3, etc. denote the unknown3s for statement 1,2,3, etc.
    # values "-1","-2","-3", etc. denote the unknown2s for statement 1,2,3, etc.
    # values (-1,),(-2,),(-3,), etc. denote the other unknown2s for the statement 1,2,3, etc.
    # values 0,1,2, etc. denote the signs
    possible_values = {} # this contains values from the set of signs {0,1,2,...}
    impossible_values = {} # this contains any values
    unknowns = [(-i-1,) for i in range(n)]
    unknowns.extend([str(-i - 1) for i in range(n)])
    unknowns.extend([-i-1 for i in range(n)])
    # signs can only be themselves
    for i in range(m):
        possible_values[i] = [i]
        impossible_values[i] = [j for j in range(m) if j != i]
    # unknown3s
    for i in range(n):
        # the first two in the statement produce a contradiction
        # the third proves associativity, so we assume to the contrary that it is not that
        possible_values[-i-1] = set(range(m))-statement_signs[i]
        impossible_values[-i-1] = statement_signs[i].copy()
        # TODO: this could be done more efficiently
        for j in set(range(n))-{i}:
            if statements[i][0] == statements[j][0] and \
                statements[i][1] == statements[j][2] and \
                statements[i][2] == statements[j][1]:
                impossible_values[-i-1].add(-j-1)
    # unknown2s
    for i in range(n):
        possible_values[str(-i-1)] = set(range(m))-statement_signs[i]
        impossible_values[str(-i-1)] = statement_signs[i] | {-i-1}
    # other unknown2s
    for i in range(n):
        possible_values[(-i-1,)] = set(range(m))-{statements[i][0], statements[i][1]}
        impossible_values[(-i-1,)] = {statements[i][0], statements[i][1]} | {str(-i-1)}
    produces_contradiction = generate_and_test_pairings(unknowns, possible_values, impossible_values, {}, statements, 0)
    if produces_contradiction:
        working_statements.append(statements)
        # for i in range(7):
        #     if len(working_statements) == 10**i:
        #         print("At least "+str(10**i)+" working statements exist!")

def generate_and_test_pairings(unknowns, possible_values, impossible_values, pairings, statements, depth):
    """Returns true if the given pairings are contradictory.
    In the case of the initial call, it returns true if the possible values and impossible values
    for these unknowns are contradictory"""
    if len(unknowns) == 0:
        # contradictions_per_level[depth][2] += 1
        # t_statements = tuple(statements)
        # try:
        #     contra_per_statements[t_statements][1] += 1
        # except KeyError:
        #     contra_per_statements[t_statements] = [0,1]
        if test_for_contradictions(pairings, impossible_values, statements):
            # contradictions_per_level[depth][1] += 1
            # contra_per_statements[t_statements][0] += 1
            return True
        else:
            # if t_statements in unique_statements_to_check:
            #     try:
            #         non_contras_per_statements[t_statements].append(pairings.copy())
            #     except KeyError:
            #         non_contras_per_statements[t_statements] = [pairings.copy()]
            return False
        # return test_for_contradictions(pairings, impossible_values, statements)
    else:
        is_contradictory = True
        unknown = unknowns.pop()
        for value in possible_values[unknown]:
            pairings[unknown] = value
            if isinstance(unknown, int):
                possible_values[str(unknown)].remove(value)
            if isinstance(unknown, str):
                possible_values[(int(unknown),)].remove(value)
            # if depth > n:
            #     if test_for_contradictions(pairings, impossible_values, statements):
            #         # return True
            #         contradictions_per_level[depth][1] += 1
            #     contradictions_per_level[depth][2] += 1
            if not generate_and_test_pairings(unknowns.copy(), possible_values, impossible_values, pairings.copy(), statements, depth+1):
                # if any particular assignment is potentially consistent, then the pairings as a whole could be consistent
                is_contradictory = False
                break
            if isinstance(unknown, int):
                possible_values[str(unknown)].add(value)
            if isinstance(unknown, str):
                possible_values[(int(unknown),)].add(value)
        return is_contradictory

def replace(old, new, table):
    """Replace every occurrence of old with new in the table."""
    for i in range(m):
        for j in range(m):
            if table[i][j] == old:
                table[i][j] = new

num_tested_contra = 0
# level is the index
# contradictions, total
contradictions_per_level = [[i,0,0] for i in range(2*n+1)]
contra_per_statements = {}
non_contras_per_statements = {}
unique_statements_to_check = [((0, 1, 2), (0, 2, 1), (3, 1, 2)),
                                ((0, 1, 2), (0, 2, 1), (3, 2, 1)),
                                ((0, 1, 2), (3, 1, 2), (3, 2, 1))]
ustc_list = [list(state_group) for state_group in unique_statements_to_check]


def test_for_contradictions(pairings, impossible_values, statements):
    """Returns true if the given pairings are contradictory.
    Returns false if the given pairings might be consistent.
    (Tests are not strong enough to definitively determine consistency).\n
    m=4:
        Sufficient: 1
    m=5:
        Sufficient: 1,2.a
    m=6:
        Sufficient:
    """
    global num_tested_contra
    num_tested_contra += 1
    # TODO: Possible tests that we can do consist of:
    # 1) Check if the given pairings contradict with the impossible_values
    # key is the unknown and val is the sign value of the unknown
    for key, val in pairings.items():
        contradictory_signs = {sign for sign in impossible_values[key] if isinstance(sign, int) and sign >= 0}
        contradictory_unknowns = {unknw for unknw in impossible_values[key] if isinstance(unknw, str)or unknw < 0}
        contradictory_values = contradictory_signs | {pairings[unknw] for unknw in contradictory_unknowns}
        if val in contradictory_values:
            return True

    # 2) Check if the table is still Latin and commutative
    # construct table
    table = [["0"] * m for i in range(m)]
    # for i in range(len(statements)):
    for key in pairings:
        if isinstance(key, str) or isinstance(key, tuple) or \
                str(key) not in pairings or (key,) not in pairings:
            continue
        i = -key-1

        original_spot = (statements[i][1], statements[i][2])
        new_spot = (pairings[-i-1], pairings[str(-i-1)])

        if table[original_spot[0]][original_spot[1]] != "0":
            replace(table[original_spot[0]][original_spot[1]], str(i+1), table)
        if table[new_spot[0]][new_spot[1]] != "0":
            replace(table[new_spot[0]][new_spot[1]], str(i+1), table)
        table[original_spot[0]][original_spot[1]] = str(i+1)
        table[original_spot[1]][original_spot[0]] = str(i+1)
        table[new_spot[0]][new_spot[1]] = str(i+1)
        table[new_spot[1]][new_spot[0]] = str(i+1)

        original_spot2 = (statements[i][0], statements[i][1])
        new_spot2 = (pairings[-i - 1], pairings[(-i - 1,)])
        if table[original_spot2[0]][original_spot2[1]] != "0":
            replace(table[original_spot2[0]][original_spot2[1]], str(key), table)
        if table[new_spot2[0]][new_spot2[1]] != "0":
            replace(table[new_spot2[0]][new_spot2[1]], str(key), table)
        table[original_spot2[0]][original_spot2[1]] = str(key)
        table[original_spot2[1]][original_spot2[0]] = str(key)
        table[new_spot2[0]][new_spot2[1]] = str(key)
        table[new_spot2[1]][new_spot2[0]] = str(key)


    # a) check for Latin
    for i in range(m):
        row_set = set()
        for j in range(m):
            # ignore places that we know nothing about
            if table[i][j] == "0":
                continue
            # if we encounter two of the same elements then the table is not Latin
            if table[i][j] in row_set:
                return True
            else:
                row_set.add(table[i][j])
    # b) check for commutative
    for i in range(m):
        for j in range(i, m):
            if table[i][j] != table[j][i]:
                return True

    # It seems unlikely that we could check these last two conditions at all.
    # It could possibly be done using a 3d table and checking for Latin/commutative, but that seems difficult
    # 3) Check if the original statements still hold.
    # 4) Check if the condition [x,[y,y]]=[y,[x,y]] still holds for all x,y (probably requires use of table? if at all possible)


    # If none of the checks indicate that the pairing is contradictory, then we admit that it could potentially be consistent.
    return False

def next_perm(perm):
    # Working from right to left, find the first j such that perm[j] < perm[j+1]
    j = n-2
    while perm[j] > perm[j+1]:
        j -= 1
    # Next find the index, i, of the smallest integer in perm to the right of j that is greater than perm[j]
    i = n-1
    while perm[i] < perm[j]:
        i -= 1
    # Swap perm[j] and perm[i]
    temp = perm[j]
    perm[j] = perm[i]
    perm[i] = temp
    # Reverse the perm from perm[j+1] to perm[n-1]
    k = j+1
    l = n-1
    while k < l:
        temp = perm[k]
        perm[k] = perm[l]
        perm[l] = temp
        k += 1
        l -= 1

def is_equivalent(st1, st2):
    curr_perm = [i for i in range(n)]
    end_perm = [n-i-1 for i in range(n)]
    while curr_perm != end_perm:
        next_perm(curr_perm)
        permuted_st2 = [st2[i] for i in curr_perm]
        offset = permuted_st2[0][0]-st1[0][0] # st1[0][0] should always equal 0, but paranoia
        are_same = True
        for i in range(n):
            for j in range(3):
                if (st1[i][j]+offset)%m != permuted_st2[i][j]:
                    are_same = False
                    break
            if not are_same:
                break
        if are_same:
            return True
    return False




start_time = time()
generate_possible_statements()
generate_and_test_combinations(n-1, [possible_statements[0]], 0)
# generate_and_test_combinations(n-len(ustc_list[0]), ustc_list[0].copy(), 0)
# test_statements(possible_statements)
end_time = time()
print(str(num_tested)+" tested in "+str(end_time-start_time))
# print(num_tested_contra)

# for level in contradictions_per_level:
#     print(level)

# if len(working_statements) == 1:
#     print("There exists a contradiction among these statements!  Yeah!")
print(len(working_statements))

# for statements, tests in contra_per_statements.items():
#     print(str(statements)+": "+str(tests))
#
# max_statement_groups = []
# max_contras = 0
# for statement_group, tests in contra_per_statements.items():
#     if tests[0] > max_contras:
#         max_statement_groups = [statement_group]
#         max_contras = tests[0]
#     elif tests[0] == max_contras:
#         max_statement_groups.append(statement_group)
#
#
# print(len(max_statement_groups))
# for statement_group in max_statement_groups:
#     print(str(statement_group)+": "+str(contra_per_statements[statement_group]))
#
#
# for ustc, tests in non_contras_per_statements.items():
#     print(str(ustc)+": "+str(tests))

# start_time = time()
# unique_working_statements = []
#
# for ws in working_statements:
#     is_contained = False
#     for uuws in unique_working_statements:
#         if is_equivalent(ws, uuws):
#             is_contained = True
#             break
#     if not is_contained:
#         unique_working_statements.append(ws)
# print(len(unique_working_statements))
# end_time = time()
# print("Checking for duplicates took: "+str(end_time-start_time)+" seconds")
# for ws in unique_working_statements:
#     for item in ws:
#         # print("".join(sign_symbols[item[i]] for i in range(3)), end=", ")
#         print(item, end=", ")
#     print()