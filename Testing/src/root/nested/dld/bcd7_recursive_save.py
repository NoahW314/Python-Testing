import json

from root.nested.dld.logic import LogicalFunction, LogicalVariable, LogicalOperators, LogicalExpression, total_size
from itertools import permutations
from timeit import default_timer as time, Timer

"""Note that the brute force implementation here is still IMPRACTICAL.  Even for just 3 gates the number of
possible expressions is way too large.  Calculations for 3 gates takes around 25 seconds, and 4 gates would take around
100 times longer than 3 gates, that is around 40 minutes.

Doing this problem in a different language like C++ or Java might help reduce the overall time somewhat or save on
memory.

Purely generating the expression (without evaluating them at all) for 3 gates takes only 1 s, but 4 gates takes 170 s if
the expressions are not stored.  Attempting to store the expressions from 4 gates results in a MemoryError after going
through ~20 trees.

Trying to do generation and/or evaluation for 5 gates would be practically impossible, especially since we would not
have the benefit of the 4 gate subtrees to help us, due to lack of memory.
"""

# TODO: Can we store the LogicalFunction info more efficiently?  Try using the bitarray library we found
"""Memory Usage:
At Approximate failure (10-20 4 trees): Intermediate 623798446 Bytes = ~600MB; Results 8181180 Bytes = ~8MB;
After 3 gates: Intermediate 8893179 Bytes = ~8.5MB; Results 605046 Bytes = ~600KB;

With bitarray:
After 3 gates:

"""

# TODO: The program can only go through about 12-13 trees of 4 gates before it runs into a memory error, so we will
#  want to do this piecewise, determining around 10 trees, writing them to a file, then deleting that section of memory
#  and doing another ten trees.  (Or do this on a per tree basis with the same memory slots being overwritten each time)


outputs = {
    "a": LogicalFunction([1, 4], size=10, are_minterms=False),
    "b": LogicalFunction([5, 6], size=10, are_minterms=False),
    "c": LogicalFunction([2], size=10, are_minterms=False),
    "d": LogicalFunction([1, 4, 7], size=10, are_minterms=False),
    "e": LogicalFunction([0, 2, 6, 8], size=10, are_minterms=True),
    "f": LogicalFunction([1, 2, 3, 7], size=10, are_minterms=False),
    "g": LogicalFunction([0, 1, 7], size=10, are_minterms=False)
}

inverted_outputs = {name + "'": ~output for name, output in outputs.items()}

empty_results = {
    "a": [[]],
    "b": [[]],
    "c": [[]],
    "d": [[]],
    "e": [[]],
    "f": [[]],
    "g": [[]]
}
transposed_results = []
intermediate = []
single_vars = {
    "A": LogicalVariable(4, 1, 10),
    "B": LogicalVariable(4, 2, 10),
    "C": LogicalVariable(4, 3, 10),
    "D": LogicalVariable(4, 4, 10)
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

# OLD Recursive functions that calculate the output of all expressions of a certain length
"""def create_expressions(start, gate_num, is_start=False):
    if gate_num == 0:
        add_parenthesis(start)
        return
    if is_start:
        for i in inputs.keys():
            start.append(i)
            create_expressions(start, gate_num)
            del start[0]
    else:
        for g in gates.keys():
            for i in inputs.keys():
                start.append(g)
                start.append(i)
                create_expressions(start, gate_num - 1)
                del start[-1]
                del start[-1]
def add_parenthesis(expression):
    values = range(0, int((len(expression)-1)/2))
    perms = permutations(values)
    for perm in perms:
        parenth_expression = expression.copy()
        gate_indices = [2*val+1 for val in values]
        for i in range(0, len(perm)):
            index = gate_indices[perm[i]]
            temp_express = LogicalExpression(parenth_expression[index-1], parenth_expression[index],
                                             parenth_expression[index+1])
            del parenth_expression[index+1]
            del parenth_expression[index]
            parenth_expression[index-1] = temp_express
            for j in range(perm[i]+1, len(gate_indices)):
                gate_indices[j] -= 2
        check_and_add(parenth_expression)
"""

perms_list = []
gate_combs = []
reduced_inputs = []
trees_list = []


def fill_perms(max_num):
    global perms_list, intermediate, transposed_results
    perms_list = [[]]
    intermediate = [[]]
    transposed_results = [{}]
    for i in range(1, max_num + 1):
        # case for i elements, from 1 to max_num elements, inclusive
        perms = tuple(permutations(range(0, i)))
        perms_list.append(perms)
        intermediate.append({})
        transposed_results.append({output_key: [] for output_key in empty_results.keys()})


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
                # Method 1.
                while isinstance(final_tree.input1, LogicalExpression) and \
                        final_tree.input1.gate[0] == final_tree.gate[0] and \
                        not isinstance(final_tree.input1.input2, LogicalExpression):
                    final_tree.gate += final_tree.input1.gate
                    final_tree.input1 = final_tree.input1.input1

                # Method 2.  Slower than Method 1
                # if isinstance(tree[perm[-1]].input1, LogicalExpression):
                #     while len(tree[perm[-1]].gate) != 1:
                #         tree[perm[-1]].input1 = LogicalExpression(tree[perm[-1]].input1, tree[perm[-1]].gate[0],
                #                                                   tree[perm[-1]].input2)
                #         tree[perm[-1]].gate = tree[perm[-1]].gate[1:]
                #         tree[perm[-1]].input2 = " "
                trees.append(final_tree)
        # remove any duplicates by converting to a set
        trees_list.append(list(set(trees)))


def expr_cant_simplify(expr, gate_num):
    for key in empty_results.keys():
        if expr in transposed_results[gate_num][key]:
            return False
    return True


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
    if subtree in intermediate[gate_num].keys():
        return intermediate[gate_num][subtree]
    return False


def generate_evaluations(gate_num):
    for i in range(1, gate_num + 1):
        start_t = time()
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

            # 26.5 s w/  21.5 s w/o  20.8 s w/mod
            # 20 s w/mod+trees  25.5 s w/mod+trees on 4
            evaluations = check_all(evaluations, i)
            if i != num_of_gates or next_level_test:
                add_tree(tree, evaluations, i)
            end_ti = time()
            if i >= 4:
                print("Tree Time: " + str(end_ti - start_ti), end="")
            print()
        print("Loop " + str(i) + " Time: " + str(time() - start_t))
        print()


def try_set(dictionary, key, value):
    try:
        dictionary[key] = value
    except MemoryError as e:
        del dictionary
        import gc
        gc.collect()
        print("Memory: " + str(total_size(intermediate)))
        print("Memory: " + str(total_size(transposed_results)))
        raise e


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
                if len(tree.gate) == 1 or non_expression:
                    expr = "(" + l_expr + tree.gate[0] + r_expr + ")"
                    try_set(evaluations, expr, l_eval.combine(gate, r_eval))
                    # evaluations[expr] = l_eval.combine(gate, r_eval)
                else:
                    for r_inputs in reduced_inputs[len(tree.gate) - 1]:
                        expr = "(" + l_expr + tree.gate[0] + r_expr
                        for r_input in r_inputs:
                            expr += tree.gate[0] + r_input
                        expr += ")"
                        try_set(evaluations, expr, l_eval.combine(gate, r_eval,
                                                                  *[inputs[r_input] for r_input in r_inputs]))
                        # evaluations[expr] = l_eval.combine(gate, r_eval,
                        #                                    *[inputs[r_input] for r_input in r_inputs])
    else:
        for r_inputs in reduced_inputs[len(tree.gate)]:
            expr = "(" + r_inputs[0]
            for i in range(1, len(tree.gate) + 1):
                expr += tree.gate[0] + r_inputs[i]
            expr += ")"
            right_side = [inputs[r_input] for r_input in r_inputs[1:]]
            try_set(evaluations, expr, inputs[r_inputs[0]].combine(gate, *right_side))
            # evaluations[expr] = inputs[r_inputs[0]].combine(gate, *right_side)
    return evaluations


def evaluate_if_possible(subtree, gate_num):
    if subtree in intermediate[gate_num].keys():
        return intermediate[gate_num][subtree]
    return False


def check_all(evaluations, gate_num):
    evals2 = {}
    for expression, evaluation in evaluations.items():
        add_to_2 = True
        for output_str in outputs.keys():
            if output_str not in expression and evaluation == outputs[output_str]:
                transposed_results[gate_num][output_str].append(expression)
                add_to_2 = False
                break
        if add_to_2 and gate_num != num_of_gates:
            evals2[expression] = evaluation.copy()
    return evals2


def check(expression, evaluation, gate_num):
    for output_str in outputs.keys():
        if output_str not in expression and evaluation == outputs[output_str]:
            transposed_results[gate_num][output_str].append(expression)
            break


def add_tree(tree, evaluations, gate_num):
    # every tree whose evaluations we calculate go in this list.
    intermediate[gate_num][tree] = evaluations


def write_intermediates(values):
    f = open("intermediate_calcs", 'w')
    json_str = json.dumps(values)
    f.write(json_str)
    f.close()


def write_results(res):
    f = open("output_expressions", 'w')
    json_str = json.dumps(res)
    f.write(json_str)
    f.close()


num_of_gates = 3
next_level_test = True

test_number = 1
print("Perms: " + str(Timer(lambda: fill_perms(num_of_gates)).timeit(number=test_number)))
print("Gates: " + str(Timer(lambda: fill_gate_combinations(num_of_gates)).timeit(number=test_number)))
print("Inputs: " + str(Timer(lambda: fill_inputs(num_of_gates)).timeit(number=test_number)))
print("Trees: " + str(Timer(lambda: fill_trees(num_of_gates)).timeit(number=test_number)))
start_time = time()
generate_evaluations(num_of_gates)
# generate_expressions(num_of_gates)
end_time = time()
print("Evaluations: " + str(end_time - start_time))

# for i in range(0, num_of_gates + 1):
#     print(str(len(trees_list[i])))  # + " " + str(sorted(trees_list[i])))
# for i in range(0, num_of_gates + 1):
#     print(str(len(gate_combs[i])))  # + " " + str(gate_combs[i]))
# for i in range(0, num_of_gates+1):
#     print(len(reduced_inputs[i]))
for index in range(1, num_of_gates + 1):
    print(len(intermediate[index]))
print()

for r_key in empty_results.keys():
    print(r_key + ":", end=" ")
    for index in range(1, num_of_gates + 1):
        print(len(transposed_results[index][r_key]), end=" ")
    print()

print("Memory: " + str(total_size(intermediate)))
print("Memory: " + str(total_size(transposed_results)))

# for key in empty_results.keys():
#     print(key)
#     for index in range(1, num_of_gates + 1):
#         print(transposed_results[index][key])


# intermediate.append({})
# # (( * )^^( + ))  15 ( * ) ( + ) Tree Time: 25.5033471
# tree = LogicalExpression(LogicalExpression(" ", "*", " "), "^^", LogicalExpression(" ", "+", " "))
# print(tree)
# start_time = time()
# generate_all_evaluations(tree)
# end_time = time()
# print()
# print(end_time-start_time)


"""
Current Timing for 7 gates
fill_perms: 1.2*10^-5 s
fill_gate_combinations: 0.06 s
fill_inputs: 0.95 s
fill_trees: 15.5 s
Total: 16.5 s

Timing (generate_expressions):
1g: 0.01 s
2g: 0.28 s
3g: 20.5 s
4g: X
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
a: 1 49 2532 
b: 1 45 2399 
c: 2 75 3952 
d: 0 26 1470 
e: 2 57 2552 
f: 0 0 354 
g: 0 0 220 
"""
