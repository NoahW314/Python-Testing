import sys
from enum import Enum
from itertools import chain

from bitarray import bitarray

"""This file is an attempt to use the bitarray library to reduce the memory usage of these logical classes, 
specifically for the bcd7 problem"""


def logical_function(values, are_minterms=None):
    if are_minterms is None:
        bool_map = values
    elif are_minterms:
        bool_map = [False] * 10
        for value in values:
            bool_map[value] = True
    else:
        bool_map = [True] * 10
        for value in values:
            bool_map[value] = False
    return bitarray(bool_map)


def logical_variable(var_num):
    values = [0] * (2**4)
    for i in range(0, 2**(var_num - 1)):
        for j in range(0, 2**(4 - var_num)):
            values[(2 * i + 1) * 2**(4 - var_num) + j] = True
    return bitarray(values[:10])


def operate(operator, *operands):
    if operator == LogicalOperators.OR:
        result = bitarray(operands[0])
        for i in range(1, len(operands)):
            result |= operands[i]
    elif operator == LogicalOperators.AND:
        result = bitarray(operands[0])
        for i in range(1, len(operands)):
            result &= operands[i]
    elif operator == LogicalOperators.XOR:
        result = bitarray(operands[0])
        for i in range(1, len(operands)):
            result ^= operands[i]
    elif operator == LogicalOperators.NOR:
        result = bitarray(operands[0])
        for i in range(1, len(operands)):
            result |= operands[i]
        result = ~result
    elif operator == LogicalOperators.NAND:
        result = bitarray(operands[0])
        for i in range(1, len(operands)):
            result &= operands[i]
        result = ~result
    elif operator == LogicalOperators.XNOR:
        result = bitarray(operands[0])
        for i in range(1, len(operands)):
            result ^= operands[i]
        result = ~result
    elif operator == LogicalOperators.NOT:
        result = ~operands[0]
    else:
        raise ValueError("Invalid operator code "+str(operator))
    return result


class LogicalOperators(Enum):
    NOT = -1
    OR = 0
    AND = 1
    XOR = 2
    NOR = 3
    NAND = 4
    XNOR = 5
    EQUIV = 5


class LogicalExpression:
    # evaluate recursively, using new/inputted inputs
    def __init__(self, input1, gate, input2):
        self.input1 = input1
        self.input2 = input2
        self.gate = gate

    # operator always goes on the left, with strict ordering of operator
    # greater is on the left
    def order(self):
        # switch when expression is input2 and input1 is input or input2>input1
        if isinstance(self.input2, LogicalExpression):
            if isinstance(self.input1, LogicalExpression):
                # we must order them to compare them
                temp1 = self.input1.copy_order()
                temp2 = self.input2.copy_order()
                # if 2 > 1, then we switch them
                if temp2 > temp1:
                    self.input1 = temp2
                    self.input2 = temp1
                else:
                    self.input1 = temp1
                    self.input2 = temp2
            # if 2 is an expression and 1 is an input, then we should switch them, putting a recursively ordered 2 in 1
            else:
                temp = self.input1
                self.input1 = self.input2.copy_order()
                self.input2 = temp
        elif isinstance(self.input1, LogicalExpression):
            self.input1.order()
        # if they are both inputs, then we do nothing (inputs should already be sorted)

    # Performs a deep copy and orders the expression at the same time
    def copy_order(self):
        # switch when expression is input2 and input1 is input or input2>input1
        if isinstance(self.input2, LogicalExpression):
            if isinstance(self.input1, LogicalExpression):
                # they must be ordered for comparison, so we copy_order them since we are performing a deep copy
                temp1 = self.input1.copy_order()
                temp2 = self.input2.copy_order()
                # if 2 > 1, then we switch them
                if temp2 > temp1:
                    return LogicalExpression(temp2, self.gate, temp1)
                else:
                    return LogicalExpression(temp1, self.gate, temp2)
            # if 2 is an expression and 1 is an input, then we should switch them, putting a recursively ordered 2 in 1
            else:
                return LogicalExpression(self.input2.copy_order(), self.gate, self.input1)
        else:
            if isinstance(self.input1, LogicalExpression):
                return LogicalExpression(self.input1.copy_order(), self.gate, self.input2)
            # if they are both inputs, then we create a shallow copy (inputs should be strings)
            else:
                return LogicalExpression(self.input1, self.gate, self.input2)

    # AND, XOR, OR preference (*, ^, +)
    # These expressions must be sorted!
    def __gt__(self, other):
        if self.gate[0] == other.gate[0]:
            if isinstance(self.input1, LogicalExpression):
                if isinstance(other.input1, LogicalExpression):
                    return self.input1 > other.input1
                else:
                    # a LogicalExpression is greater than a str input
                    return True
            else:
                if isinstance(other.input1, LogicalExpression):
                    # a LogicalExpression is greater than a str input
                    return False
                else:
                    return self.input1 > other.input1
        if self.gate[0] == "*":
            return True
        if self.gate[0] == "^":
            return other.gate[0] == "+"
        if self.gate[0] == "+":
            return False

    def copy(self):
        copied_input1 = self.input1.copy() if isinstance(self.input1, LogicalExpression) else self.input1
        copied_input2 = self.input2.copy() if isinstance(self.input2, LogicalExpression) else self.input2
        return LogicalExpression(copied_input1, self.gate, copied_input2)

    # compare equality recursively, should be ordered inputs
    def __eq__(self, other):
        # we can only check equality if the inputs are of the same type, if not then the expressions are clearly unequal
        if isinstance(self.input2, type(other.input2)) and isinstance(self.input1, type(other.input1)):
            return self.gate == other.gate and self.input2 == other.input2 and self.input1 == other.input1
        else:
            return False

    def __len__(self):
        gate_len = len(self.gate)
        left_len = len(self.input1) if isinstance(self.input1, LogicalExpression) else 0
        right_len = len(self.input2) if isinstance(self.input2, LogicalExpression) else 0
        return left_len + gate_len + right_len

    def __str__(self):
        return "(" + str(self.input1) + str(self.gate) + str(self.input2) + ")"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.input1, self.gate, self.input2))


def total_size(o):
    seen = set()  # track which object id's have already been seen
    default_size = sys.getsizeof(0)  # estimate sizeof object without __sizeof__
    dict_handler = lambda d: chain.from_iterable(d.items())

    def sizeof(obj):
        if id(obj) in seen:  # do not double count the same object
            return 0
        seen.add(id(obj))
        s = sys.getsizeof(obj, default_size)

        if isinstance(obj, list):
            s += sum(map(sizeof, iter(obj)))
        if isinstance(obj, dict):
            s += sum(map(sizeof, dict_handler(obj)))
        return s

    return sizeof(o)
