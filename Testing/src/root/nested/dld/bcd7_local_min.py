"""Goal:
Generate all possible combinations for getting the outputs a-g, using as few inputs as possible.
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
outputs2 = {
    "d": outputs["d"],
    "f": outputs["f"],
    "g": outputs["g"]
}

empty_results = {
    "a": [],
    "b": [],
    "c": [],
    "d": [],
    "e": [],
    "f": [],
    "g": []
}
results = empty_results.copy()
single_vars = {
    "A": LogicalVariable(4, 1),
    "B": LogicalVariable(4, 2),
    "C": LogicalVariable(4, 3),
    "D": LogicalVariable(4, 4)
}
single_inverted_vars = {name + "'": ~var for name, var in single_vars.items()}

inputs = {**single_vars, **single_inverted_vars}
gates = {
    "+": LogicalOperators.OR,
    "*": LogicalOperators.AND,
    "^": LogicalOperators.XOR
}

"""
for input1 in inputs.keys():
    for input2 in inputs.keys():
        for gate1 in gates.keys():
            result = inputs[input1].combine(gates[gate1], inputs[input2])
            # Check if inputs in gate produce any of the desired outputs
            for o in outputs2:
                if result == outputs2[o]:
                    # Record if they do
                    results[o].append([input1, gate1, input2])

print("2")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print([eq[0]+eq[1]+eq[2] for eq in output_eq])

print()
print()
results = empty_results.copy()


for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for gate1 in gates.keys():
                result = inputs[input1].combine(gates[gate1], inputs[input2], inputs[input3])
                # Check if inputs in gate produce any of the desired outputs
                for o in outputs2:
                    if result == outputs2[o]:
                        # Record if they do
                        results[o].append([input1, gate1, input2, input3])

print("3")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print([eq[0]+eq[1]+eq[2]+eq[1]+eq[3] for eq in output_eq])

print()
print()
results = empty_results.copy()

for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for input4 in inputs.keys():
                for gate1 in gates.keys():
                    result = inputs[input1].combine(gates[gate1], inputs[input2], inputs[input3], inputs[input4])
                    # Check if inputs in gate produce any of the desired outputs
                    for o in outputs2:
                        if result == outputs2[o]:
                            # Record if they do
                            results[o].append([input1, gate1, input2, input3, input4])

print("4a")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print([eq[0]+eq[1]+eq[2]+eq[1]+eq[3]+eq[1]+eq[4] for eq in output_eq])

print()
print()
results = empty_results.copy()


for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for gate1 in gates.keys():
                for gate2 in gates.keys():
                    if gate1 == gate2:
                        continue
                    result = (inputs[input1].combine(gates[gate1], inputs[input2])).combine(gates[gate2], inputs[input3])
                    # Check if inputs in gate produce any of the desired outputs
                    for o in outputs2:
                        if result == outputs2[o]:
                            # Record if they do
                            results[o].append([input1, gate1, input2, gate2, input3])

print("4b")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print(["("+eq[0]+eq[1]+eq[2]+")"+eq[3]+eq[4] for eq in output_eq])

print()
print()
results = empty_results.copy()


for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for input4 in inputs.keys():
                for gate1 in gates.keys():
                    for gate2 in gates.keys():
                        result = inputs[input1].combine(gates[gate1], inputs[input2], inputs[input3]).combine(gates[gate2], inputs[input4])
                        # Check if inputs in gate produce any of the desired outputs
                        for o in outputs2:
                            if result == outputs2[o]:
                                # Record if they do
                                results[o].append([input1, gate1, input2, input3, gate2, input4])

print("5")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print(["("+eq[0]+eq[1]+eq[2]+eq[1]+eq[3]+")"+eq[4]+eq[5] for eq in output_eq])

print()
print()
results = empty_results.copy()

for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for input4 in inputs.keys():
                for input5 in inputs.keys():
                    for gate1 in gates.keys():
                        for gate2 in gates.keys():
                            result = inputs[input1].combine(gates[gate1], inputs[input2], inputs[input3], inputs[input4])\
                                                    .combine(gates[gate2], inputs[input5])
                            # Check if inputs in gate produce any of the desired outputs
                            for o in outputs2:
                                if result == outputs2[o]:
                                    # Record if they do
                                    results[o].append([input1, gate1, input2, input3, input4, gate2, input5])

print("6a")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print(["("+eq[0]+eq[1]+eq[2]+eq[1]+eq[3]+eq[1]+eq[4]+")"+eq[5]+eq[6] for eq in output_eq])

print()
print()
results = empty_results.copy()

for input1 in inputs.keys():
    for input2 in inputs.keys():
        for input3 in inputs.keys():
            for input4 in inputs.keys():
                for gate1 in gates.keys():
                    for gate2 in gates.keys():
                        for gate3 in gates.keys():
                            temp1 = inputs[input1].combine(gates[gate1], inputs[input2])
                            temp2 = inputs[input3].combine(gates[gate3], inputs[input4])
                            result = temp1.combine(gates[gate2], temp2)
                            # Check if inputs in gate produce any of the desired outputs
                            for o in outputs2:
                                if result == outputs2[o]:
                                    # Record if they do
                                    results[o].append([input1, gate1, input2, gate2, input3, gate3, input4])

print("6b")
for key, output_eq in results.items():
    if len(output_eq) != 0:
        print(key)
        print(["("+eq[0]+eq[1]+eq[2]+")"+eq[3]+"("+eq[4]+eq[5]+eq[6]+")" for eq in output_eq])

print()
print()
results = empty_results.copy()
"""
