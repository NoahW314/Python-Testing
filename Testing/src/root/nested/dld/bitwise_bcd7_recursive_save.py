import json

from root.nested.dld.bitwise_logic import logical_function, logical_variable, LogicalOperators, LogicalExpression, \
    total_size, operate
from itertools import permutations, combinations
from timeit import default_timer as time, Timer

# TODO: We have optimized the program enough that, given enough time, we could evaluate 4-5, maybe even 6, gates, and analyze
# these results for the global minimum solution.  However, we need to make some progress in proving what the maximum number
# of gates that need to be checked is, otherwise we have to go up to around 11-23 gates, which is well beyond practical.
"""Note that the full brute force implementation here is still IMPRACTICAL, however it is getting more practical.
Currently, calculations for 3 gates takes around 5 seconds, and 4 gates finishes in just under 6 minutes.  5 gates would
be our next target.  It should be noted that attempting to store the expressions from 4 gates results in a MemoryError 
after going through ~10 trees, so this makes calculating 5 gates trickier.

We could attempt to write these trees to a file, and only retrieve them when needed, but this will significantly slow 
down the program.  The benefit of being able to use the 4 gate values might be worth the time it takes to read from a 
file.

Doing this problem in a different language like C++ might help reduce the overall time somewhat or save on
memory.
"""
 

# TODO: we now have enough results that we should start writing them to a file when we discover them.  This might help
# save enough memory to store more intermediate calculations from the 4 gates, since we shouldn't need to keep the
# results in an array if we write them to the file.

# TODO: we might also be able to help with the memory problem by changing the algorithm to evaluate the expressions while
# generating them, rather than discovering them all, then evaluating them.  This would probably be slower, but by combining
# this with the file storage plan above, it would allow the program to continue running for long periods of time without
# worrying about running out of memory.  This memory/speed trade-off seems like it would be worth it.

outputs = {
    "a": logical_function([1, 4], are_minterms=False),
    "b": logical_function([5, 6],  are_minterms=False),
    "c": logical_function([2], are_minterms=False),
    "d": logical_function([1, 4, 7], are_minterms=False),
    "e": logical_function([0, 2, 6, 8], are_minterms=True),
    "f": logical_function([1, 2, 3, 7], are_minterms=False),
    "g": logical_function([0, 1, 7], are_minterms=False)
}

inverted_outputs = {name + "'": ~output for name, output in outputs.items()}

empty_results = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
    "e": [],
    "f": [],
    "g": []
}
intermediate = []
single_vars = {
    "A": logical_variable(1),
    "B": logical_variable(2),
    "C": logical_variable(3),
    "D": logical_variable(4)
}
single_inverted_vars = {name + "'": ~var for name, var in single_vars.items()}
inputs_to_inverse = {**{name + "'": name for name in single_vars.keys()},
                     **{name[0]: name for name in single_inverted_vars.keys()},
                     **{name + "'": name for name in outputs.keys()},
                     **{name[0]: name for name in inverted_outputs.keys()}}

inputs = {**single_vars, **single_inverted_vars, **outputs, **inverted_outputs}
gates = {
    "+": LogicalOperators.OR,
    "*": LogicalOperators.AND,
    "^": LogicalOperators.XOR
}

perms_list = []
gate_combs = []
reduced_inputs = []
trees_list = []

results_file = None


def file_init():
    global results_file
    if overwrite_results:
        results_file = open("output_expressions", 'w')


def fill_perms(max_num):
    global perms_list, intermediate
    perms_list = [[]]
    intermediate = [[]]
    for i in range(1, max_num + 1):
        # case for i elements, from 1 to max_num elements, inclusive
        perms_list.append(tuple(permutations(range(0, i))))
        intermediate.append({})


def generate_gate_combs_recursive(start, gates_list, gate_num):
    if gate_num == 0:
        gates_list.append(start.copy())
    else:
        for gate in gates:
            start.append(gate)
            generate_gate_combs_recursive(start, gates_list, gate_num - 1)
            del start[-1]


def simplify_gate_comb(gate_comb):
    temp = []
    continues = 0
    for i in range(0, len(gate_comb)):
        if continues > 0:
            continues -= 1
            continue
        j = 1
        while i + j < len(gate_comb) and gate_comb[i + j - 1] == gate_comb[i + j]:
            j += 1
        temp.append(gate_comb[i] * j)
        continues = j - 1
    gate_comb[:] = temp.copy()


def fill_gate_combinations(gate_num):
    global gate_combs
    gate_combs = [[]]  # case for 0 gates
    for i in range(1, gate_num + 1):
        # case for i elements
        gate_combs_n = []
        generate_gate_combs_recursive([], gate_combs_n, i)
        new_gate_combs_n = []
        # Evaluate and only accept new ones
        for gate_comb in gate_combs_n:
            simplify_gate_comb(gate_comb)
            # Neither the gate combination nor its reverse must already be in the list
            if gate_comb not in new_gate_combs_n and gate_comb[::-1] not in new_gate_combs_n:
                new_gate_combs_n.append(gate_comb)
        gate_combs.append(new_gate_combs_n)


def generate_next_input_combs(start, inputs_list):
    # This could be further optimized if needed, since the reduced inputs are already sorted
    for single_input in inputs.keys():
        if single_input in start or inputs_to_inverse[single_input] in start:
            continue
        start.append(single_input)
        inputs_list.append(tuple(sorted(start)))
        del start[-1]


def fill_inputs(gate_num):
    global reduced_inputs
    reduced_inputs = [[]]  # case for 0 gates
    for i in range(1, gate_num + 2):
        input_combs = []  # each input will be sorted
        if i == 1:
            for name in inputs.keys():
                input_combs.append((name,))
        else:
            for r_input in reduced_inputs[i - 1]:
                generate_next_input_combs(list(r_input).copy(), input_combs)
        reduced_input_combs = list(set(input_combs))
        reduced_inputs.append(reduced_input_combs)
    reduced_inputs.pop(0)


def simplify_tree15(tree):
    if isinstance(tree.input1, LogicalExpression) and not isinstance(tree.input2, LogicalExpression):
        # check gates for stuff
        while isinstance(tree.input1, LogicalExpression) and tree.input1.gate[0] == tree.gate[0] and \
                not isinstance(tree.input1.input2, LogicalExpression):
            tree.gate += tree.input1.gate
            tree.input1 = tree.input1.input1
    # recursively simplify subtrees as well
    if isinstance(tree.input1, LogicalExpression):
        simplify_tree15(tree.input1)
    if isinstance(tree.input2, LogicalExpression):
        simplify_tree15(tree.input2)


def simplify_tree(tree):
    # Part 1.
    # Converts ()+)+) into ()++) at the end/top of the expression/tree
    while isinstance(tree.input1, LogicalExpression) and tree.input1.gate[0] == tree.gate[0] and \
            not isinstance(tree.input1.input2, LogicalExpression):
        tree.gate += tree.input1.gate
        tree.input1 = tree.input1.input1

    # Part 1.5
    # Converts ()+)+) into ()++) anywhere in the tree
    simplify_tree15(tree)

    # Part 2.
    # Converts ()++() into ()+())+) at the end/top of the expression/tree
    if len(tree.gate) > 1 and isinstance(tree.input2, LogicalExpression):
        tree.gate = tree.gate[1:]
        tree.input1 = LogicalExpression(tree.input1, tree.gate[0], tree.input2)
        tree.input2 = " "


def fill_trees(gate_num):
    global trees_list
    trees_list = [[]]  # case for 0 gates
    # loop through all the gate numbers, up to and including gate_num
    for i in range(1, gate_num + 1):
        trees = []
        # loop through all the gate combos
        for gate_comb in gate_combs[i]:
            leng = len(gate_comb)
            # and loop through all the parenthetical permutations
            for perm in perms_list[leng]:
                # generate a tree for each of possible combinations
                tree = gate_comb.copy()
                gate_activity = [1] * leng
                # 2 is expression
                # 1 is normal gate
                # 0 is deleted
                for p in perm:
                    l_index = p - 1
                    r_index = p + 1
                    while l_index >= 0 and gate_activity[l_index] == 0:
                        l_index -= 1
                    while r_index < leng and gate_activity[r_index] == 0:
                        r_index += 1
                    left = " "
                    right = " "
                    # is_left
                    if l_index >= 0 and gate_activity[l_index] == 2:
                        gate_activity[l_index] = 0
                        left = tree[l_index]
                    # is_right
                    if r_index < leng and gate_activity[r_index] == 2:
                        gate_activity[r_index] = 0
                        right = tree[r_index]
                    tree[p] = LogicalExpression(left, tree[p], right)
                    gate_activity[p] = 2

                # order the tree
                final_tree = tree[perm[-1]]
                final_tree.order()
                simplify_tree(final_tree)
                trees.append(final_tree)
        # remove any duplicates by converting to a set
        trees_list.append(list(set(trees)))


def generate_expressions(gate_num):
    for i in range(1, gate_num + 1):
        start_t = time()
        print(i)
        print(len(trees_list[i]))
        cnt = 0
        for tree in trees_list[i]:
            cnt += 1
            if i >= 4:
                print(cnt)
            # start_ti = time()
            expressions = generate_all_expressions(tree)
            add_tree(tree, expressions, i)
            # end_ti = time()
            # if i >= 4:
            #     print("Tree Time: " + str(end_ti - start_ti), end="")
            # print()
        print("Loop " + str(i) + " Time: " + str(time() - start_t))
        print()


def try_append(expressions, expr):
    try:
        expressions.append(expr)
    except MemoryError as e:
        del expressions
        import gc
        gc.collect()
        sum_len = 0
        for trees in intermediate[4]:
            sum_len += len(trees)
        print(sum_len)
        raise e


def generate_all_expressions(tree):
    known_subtree = express_if_possible(tree, len(tree))
    if known_subtree:
        # print(tree, end=" ")
        return known_subtree  # expressions
    expressions = []
    # traverse the left side of the tree first recursively
    if isinstance(tree.input1, LogicalExpression):
        left_evaluations = generate_all_expressions(tree.input1)
        # generate all possible evaluations for the right side of the tree
        if isinstance(tree.input2, LogicalExpression):
            non_expression = False
            right_evaluations = generate_all_expressions(tree.input2)
        elif len(tree.gate) == 1:
            non_expression = True
            right_evaluations = list(inputs.keys()).copy()
        else:
            non_expression = True
            right_evaluations = generate_all_expressions(LogicalExpression(" ", tree.gate[1:], " "))
        # then generate all combinations of left mixed with right
        for l_expr in left_evaluations:
            for r_expr in right_evaluations:
                if len(tree.gate) == 1 or non_expression:
                    expr = "(" + l_expr + tree.gate[0] + r_expr + ")"
                    try_append(expressions, expr)
                else:
                    for r_inputs in reduced_inputs[len(tree.gate) - 1]:
                        expr = "(" + l_expr + tree.gate[0] + r_expr
                        for r_input in r_inputs:
                            expr += tree.gate[0] + r_input
                        expr += ")"
                        try_append(expressions, expr)
    else:
        for r_inputs in reduced_inputs[len(tree.gate)]:
            expr = "(" + r_inputs[0]
            for i in range(1, len(tree.gate) + 1):
                expr += tree.gate[0] + r_inputs[i]
            expr += ")"
            try_append(expressions, expr)
    return expressions


def express_if_possible(subtree, gate_num):
    try:
        return intermediate[gate_num][subtree]
    except KeyError:
        return False
    # if subtree in intermediate[gate_num].keys():
    #     return intermediate[gate_num][subtree]
    # return False


def generate_evaluations(gate_num):
    for i in range(1, gate_num + 1):
        start_t = time()
        results = {name: [] for name in empty_results.keys()}
        print(i)
        print(len(trees_list[i]))
        cnt = 0
        for tree in trees_list[i]:
            cnt += 1
            print(str(tree) + "  " + str(cnt), end=" ")
            start_ti = time()
            evaluations = generate_all_evaluations(tree)
            # for expression, evaluation in evaluations.items():
            #     check(expression, evaluation, i)

            evaluations = check_all(evaluations, i, results)
            if i != num_of_gates or next_level_test:
                add_tree(tree, evaluations, i)
            # add_tree(tree, evaluations, i)
            end_ti = time()
            if i >= 4:
                print("Tree Time: " + str(end_ti - start_ti), end="")
            print()
        if overwrite_results:
            write_results(results)
        # print("IM " + str(i) + " : " + str(total_size(intermediate)))
        print("Loop " + str(i) + " Time: " + str(time() - start_t))
        print()


def try_set(dictionary, key, value):
    try:
        dictionary[key] = value
    except MemoryError as e:
        global intermediate
        del intermediate
        import gc
        gc.collect()
        print("Memory: "+str(total_size(dictionary)))
        print(time()-start_time)
        raise e


def evaluate(non_expression, gate, evaluations, l_expr, l_eval, r_expr, r_eval):
    if len(gate) == 1 or non_expression:
        expr = "(" + l_expr + gate[0] + r_expr + ")"
        try_set(evaluations, expr, operate(gates[gate[0]], l_eval, r_eval))
    else:
        for r_inputs in reduced_inputs[len(gate) - 1]:
            expr = "(" + l_expr + gate[0] + r_expr
            for r_input in r_inputs:
                expr += gate[0] + r_input
            expr += ")"
            try_set(evaluations, expr, operate(gates[gate[0]], l_eval, r_eval,
                                               *[inputs[r_input] for r_input in r_inputs]))


def generate_all_evaluations(tree):
    known_subtree = evaluate_if_possible(tree, len(tree))
    if known_subtree:
        print(tree, end=" ")
        return known_subtree  # evaluations
    evaluations = {}
    gate = gates[tree.gate[0]]
    # traverse the left side of the tree first recursively
    if isinstance(tree.input1, LogicalExpression):
        left_evaluations = generate_all_evaluations(tree.input1)
        # generate all possible evaluations for the right side of the tree
        if isinstance(tree.input2, LogicalExpression):
            if tree.input1 == tree.input2:
                combs = list(combinations(left_evaluations.keys(), 2))
                for comb in combs:
                    l_expr = comb[0]
                    r_expr = comb[1]
                    l_eval = left_evaluations[l_expr]
                    r_eval = left_evaluations[r_expr]
                    evaluate(False, tree.gate, evaluations, l_expr, l_eval, r_expr, r_eval)
                return evaluations
            non_expression = False
            right_evaluations = generate_all_evaluations(tree.input2)
        elif len(tree.gate) == 1:
            non_expression = True
            right_evaluations = {r_input: inputs[r_input] for r_input in inputs}
        else:
            non_expression = True
            right_evaluations = generate_all_evaluations(LogicalExpression(" ", tree.gate[1:], " "))

        # then generate all combinations of left mixed with right
        for l_expr, l_eval in left_evaluations.items():
            for r_expr, r_eval in right_evaluations.items():
                evaluate(non_expression, tree.gate, evaluations, l_expr, l_eval, r_expr, r_eval)
    else:
        for r_inputs in reduced_inputs[len(tree.gate)]:
            expr = "(" + r_inputs[0]
            for i in range(1, len(tree.gate) + 1):
                expr += tree.gate[0] + r_inputs[i]
            expr += ")"
            right_side = [inputs[r_input] for r_input in r_inputs]
            try_set(evaluations, expr, operate(gate, *right_side))
    return evaluations


def evaluate_if_possible(subtree, gate_num):
    try:
        return intermediate[gate_num][subtree]
    except KeyError:
        return False
    # if subtree in intermediate[gate_num].keys():
    #     return intermediate[gate_num][subtree]
    # return False


def check_all(evaluations, gate_num, results):
    evals2 = {}
    for expression, evaluation in evaluations.items():
        add_to_2 = True
        for output_str in outputs.keys():
            if output_str not in expression and evaluation == outputs[output_str]:
                if overwrite_results:
                    results[output_str].append(expression)
                add_to_2 = False
                break
        if add_to_2 and (gate_num != num_of_gates or next_level_test):
            evals2[expression] = evaluation.copy()
    return evals2


def check(expression, evaluation, results):
    for output_str in outputs.keys():
        if output_str not in expression and evaluation == outputs[output_str]:
            results[output_str].append(expression)
            break


def add_tree(tree, evaluations, gate_num):
    # every tree whose evaluations we calculate go in this list.
    intermediate[gate_num][tree] = evaluations


def write_intermediates(values):
    f = open("intermediate_calcs", 'w')
    json_str = json.dumps(values)
    f.write(json_str)
    f.close()


# noinspection PyUnresolvedReferences
def write_results(res):
    json_str = json.dumps(res, indent=1)+"\n$$$$\n"
    if results_file is not None:
        results_file.write(json_str)
    elif overwrite_results:
        raise ValueError("file_init() must be called before write_results!")


# noinspection PyUnresolvedReferences
def file_close():
    if results_file is not None:
        results_file.close()
    elif overwrite_results:
        raise ValueError("file_init() must be called before file_close!")


num_of_gates = 1
# if we store the intermediates for the num_of_gates level
# True if we plan to test a specific case on the next level up
next_level_test = True
# if we want to overwrite the output_expressions file or not
overwrite_results = False

test_number = 1
file_init()
print("Perms: " + str(Timer(lambda: fill_perms(num_of_gates)).timeit(number=test_number)))
print("Gates: " + str(Timer(lambda: fill_gate_combinations(num_of_gates)).timeit(number=test_number)))
print("Inputs: " + str(Timer(lambda: fill_inputs(num_of_gates)).timeit(number=test_number)))
print("Trees: " + str(Timer(lambda: fill_trees(num_of_gates)).timeit(number=test_number)))
start_time = time()
generate_evaluations(num_of_gates)
# generate_expressions(num_of_gates)
end_time = time()
print("Evaluations: " + str(end_time - start_time))
file_close()
#
# for index in range(0, num_of_gates + 1):
#     print(str(len(trees_list[index])) + " " + str(sorted(trees_list[index])))
# for index in range(0, num_of_gates + 1):
#     print(str(len(gate_combs[index])) + " " + str(gate_combs[index]))
# for index in range(0, num_of_gates+1):
#     print(len(reduced_inputs[index]))
# for index in range(1, num_of_gates + 1):
#     print(len(intermediate[index]))
# print()

# print("Memory: " + str(total_size(intermediate)))


for i in range(0, 8):
    intermediate.append({})
# (( * )^^( + ))  15 ( * ) ( + ) Tree Time: 25.5033471 (~25 s)
# ((( * )^( + ))^ ) 15 (( * )^( + ) Tree Time: 1.7766589 (~1-2 s)
# tree = LogicalExpression(LogicalExpression(LogicalExpression(" ", "*", " "), "^",
#                                            LogicalExpression(" ", "+", " ")), "^", " ")
# tree = LogicalExpression(LogicalExpression(" ", "*", " "), "+", LogicalExpression(" ", "*", " "))
#  ((((((( * )+( ^ ))* ) ^ ( + ))
# print(tree)
# start_time = time()
# generate_all_evaluations(tree)
# end_time = time()
# print()
# print(end_time-start_time)

# Note that this 6 gate expression below causes a memory error by itself.  A major speed-for-memory sacrifice may have
# to be made to be able to evaluate larger expressions like this, even one at a time
# tree = LogicalExpression(LogicalExpression(LogicalExpression(LogicalExpression(" ", "*", " "), "+",
#                                                              LogicalExpression(" ", "^", " ")), "*", " "), "^",
#                          LogicalExpression(" ", "+", " "))

"""
Current Timing for 7 gates
fill_perms: 1.2*10^-5 s
fill_gate_combinations: 0.06 s
fill_inputs: 0.95 s
fill_trees: 15.5 s
Total: 16.5 s

Timing (generate_evaluations):
1g: 0.002 s  (61011 B     = 60 KB)
2g: 0.07 s   (2994615 B   = 3 MB)
3g: 4.7 s      (220335869 B = 210 MB)
4g: 5' 42"   (X)
5g:
6g:
7g:
"""
"""Number of trees per gate level
0
3
9
36
166
904
5055
29397
"""
"""Number of correct expressions per output (Currently, may be reduced later)
a: 1 49 2463 165547 
b: 1 45 2281 147817 
c: 2 75 3761 267873 
d: 0 26 1343 85136 
e: 2 57 2449 140913 
f: 0 0 310 22695 
g: 0 0 204 11659 
Total: 6 252 12811 841640
Factor:  42 50 65
"""
