"""Goal:
Generate all possible combinations for getting the outputs a-g, using as few inputs as possible.

Next Step: Make a function to count the number of inputs (both locally and globally)
"""
from root.nested.dld.logic import LogicalFunction, LogicalVariable, LogicalOperators

outputs = {
    "a": LogicalFunction([1, 4], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=False),
    "b": LogicalFunction([5, 6], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=False),
    "c": LogicalFunction([2], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=False),
    "d": LogicalFunction([1, 4, 7], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=False),
    "e": LogicalFunction([0, 2, 6, 8], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=True),
    "f": LogicalFunction([1, 2, 3, 7], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=False),
    "g": LogicalFunction([0, 1, 7], dont_cares=[10, 11, 12, 13, 14, 15], size=16, are_minterms=False)
}

inverted_outputs = {name + "'": ~output for name, output in outputs.items()}

two_input_results = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
    "e": [],
    "f": [],
    "g": []
}
three_input_results = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
    "e": [],
    "f": [],
    "g": []
}
four_input_single_results = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
    "e": [],
    "f": [],
    "g": []
}
four_input_two_results = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
    "e": [],
    "f": [],
    "g": []
}

single_vars = {
    "A": LogicalVariable(4, 1),
    "B": LogicalVariable(4, 2),
    "C": LogicalVariable(4, 3),
    "D": LogicalVariable(4, 4)
}
single_inverted_vars = {name + "'": ~var for name, var in single_vars.items()}

inputs = {**outputs, **inverted_outputs, **single_vars, **single_inverted_vars}
gates = {
    "+": LogicalOperators.OR,
    "*": LogicalOperators.AND,
    "^": LogicalOperators.XOR
}
"""
# Loop through all possible single gate combinations
# Loop through all inputs for the first input
for input1 in inputs.keys():
    # Loop for second input
    for input2 in inputs.keys():
        # Loop for gate type
        for gate in gates.keys():
            result = inputs[input1].combine(gates[gate], inputs[input2])
            # Check if inputs in gate produce any of the desired outputs
            for o in outputs:
                if result == outputs[o] and o != input1 and o != input2 and (o + "'") != input1 and (o + "'") != input2:
                    # Record if they do
                    single_gate_results[o][input1 + gate + input2] = result

for key, value in single_gate_results.items():
    print(key)
    print(list(value.keys()))

print()
print()


def custom_checks(out, *ins):
    if out == "a":
        return not ("d" in ins or "d'" in ins)
    if out == "b":
        return not ("d" in ins or "d'" in ins)
    if out == "c":
        return not ("f" in ins or "f'" in ins)
    if out == "e":
        return not ("a" in ins or "a'" in ins or "d" in ins or "d'" in ins)
    return True


# Loop through all possible dual gate combinations
for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for gate1 in gates.keys():
                for gate2 in gates.keys():
                    result = (inputs[input1].combine(gates[gate1], inputs[input2])).combine(gates[gate2],
                                                                                            inputs[input3])
                    # Check if inputs in gate produce any of the desired outputs
                    for o in outputs:
                        if result == outputs[o] and o != input1 and o != input2 and o != input3 \
                                and (o + "'") != input1 and (o + "'") != input2 and (o + "'") != input3 \
                                and input1 != input2 and input1 != input3 and input2 != input3 \
                                and custom_checks(o, input1, input2, input3):
                            # Record if they do
                            dual_gate_results[o]["(" + input1 + gate1 + input2 + ")" + gate2 + input3] = result

for key, value in dual_gate_results.items():
    print(key)
    print(list(value.keys()))

print()
print()

# TODO: After doing three gate combinations, look for equations which only involve one (or two) gate type(s)
#   Do the same strategy if the three gate combinations are too numerous

# Loop through all possible three gate combinations
for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for input4 in inputs.keys():
                for gate1 in gates.keys():
                    for gate2 in gates.keys():
                        for gate3 in gates.keys():
                            if input1 != input2 and input1 != input3 and input1 != input4 and input2 != input3 \
                                    and input2 != input4 and input3 != input4:
                                result = (inputs[input1].combine(gates[gate1], inputs[input2])) \
                                    .combine(gates[gate2], inputs[input3]).combine(gates[gate3], inputs[input4])
                                # Check if inputs in gate produce any of the desired outputs
                                for o in outputs:
                                    if result == outputs[o] and o != input1 and o != input2 and o != input3 \
                                            and o != input4 and (o + "'") != input4 \
                                            and (o + "'") != input1 and (o + "'") != input2 and (o + "'") != input3 \
                                            and custom_checks(o, input1, input2, input3, input4):
                                        # Record if they do
                                        three_gate_results[o]["((" + input1 + gate1 + input2 + ")" + gate2 + input3 +
                                                              ")" + gate3 + input4] = result

for key, value in three_gate_results.items():
    print(key)
    print(list(value.keys()))

print()
print()"""


def is_not_in_reversed(o, gate, input1, input2):
    equations = two_input_results[o]
    for eq in equations:
        if gate == eq[1]:
            if eq[2] == input1 and eq[0] == input2:
                return False
    return True


def is_not_in_comb(o, gate, results, *ins):
    equations = results[o]
    for eq in equations:
        if gate == eq[0]:
            if sorted(ins) == sorted(eq[1:]):
                return False
    return True


def is_not_in_four(o, gate, results, *ins):
    equations = results[o]
    for eq in equations:
        if gate == eq[0]:
            if sorted(ins) == sorted([eq[2], eq[3]]):
                return False
    return True


for input1 in inputs.keys():
    # Loop for second input
    for input2 in inputs.keys():
        # Loop for gate type
        for gate in gates.keys():
            result = inputs[input1].combine(gates[gate], inputs[input2])
            # Check if inputs in gate produce any of the desired outputs
            for o in outputs:
                if result == outputs[o] and o != input1 and o != input2 and (o + "'") != input1 and (o + "'") != input2\
                        and is_not_in_reversed(o, gate, input1, input2):
                    # Record if they do
                    two_input_results[o].append([input1, gate, input2])

for key, output_eq in two_input_results.items():
    print(key)
    print([eq[0]+eq[1]+eq[2] for eq in output_eq])

print()
print()


for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for gate in gates.keys():
                result = inputs[input1].combine(gates[gate], inputs[input2], inputs[input3])
                # Check if inputs in gate produce any of the desired outputs
                for o in outputs:
                    if result == outputs[o] and o != input1 and o != input2 and o != input3 \
                            and (o + "'") != input1 and (o + "'") != input2 and (o + "'") != input3 \
                            and input1 != input2 and input1 != input3 and input2 != input3 \
                            and is_not_in_comb(o, gate, three_input_results, input1, input2, input3):
                        # Record if they do
                        three_input_results[o].append([gate, input1, input2, input3])

for key, output_eq in three_input_results.items():
    print(key)
    print([eq[1]+eq[0]+eq[2]+eq[0]+eq[3] for eq in output_eq])

print()
print()


def custom_check(o, *ins):
    return True

"""
for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for input4 in inputs.keys():
                for gate in gates.keys():
                    result = inputs[input1].combine(gates[gate], inputs[input2], inputs[input3], inputs[input4])
                    # Check if inputs in gate produce any of the desired outputs
                    for o in outputs:
                        if result == outputs[o] and o != input1 and o != input2 and o != input3 and o != input4 \
                                and (o+"'") != input1 and (o+"'") != input2 and (o+"'") != input3 and (o+"'") != input4\
                                and input1 != input2 and input1 != input3 and input1 != input4 \
                                and input2 != input3 and input2 != input4 and input3 != input4 \
                                and is_not_in_comb(o, gate, four_input_single_results, input1, input2, input3, input4):
                            # Record if they do
                            four_input_single_results[o].append([gate, input1, input2, input3, input4])

for key, output_eq in four_input_single_results.items():
    print(key)
    print([eq[1]+eq[0]+eq[2]+eq[0]+eq[3]+eq[0]+eq[4] for eq in output_eq])

print()
print()
"""
for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for gate1 in gates.keys():
                for gate2 in gates.keys():
                    result = inputs[input1].combine(gates[gate1], inputs[input2]).combine(gates[gate2], inputs[input3])
                    # Check if inputs in gate produce any of the desired outputs
                    for o in outputs:
                        if result == outputs[o] and o != input1 and o != input2 and o != input3 \
                                and (o+"'") != input1 and (o+"'") != input2 and (o+"'") != input3 \
                                and input1 != input2 and input1 != input3 and input2 != input3 \
                                and is_not_in_four(o, gate1, four_input_two_results, input1, input2) and gate1 != gate2:
                            # Record if they do
                            four_input_two_results[o].append([gate1, gate2, input1, input2, input3])
for key, output_eq in four_input_two_results.items():
    print(key)
    print(["("+eq[2]+eq[0]+eq[3]+")"+eq[1]+eq[4] for eq in output_eq])

print()
print()
