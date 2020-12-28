import sys
from enum import Enum
from itertools import chain


class LogicalFunction:
    def __init__(self, values, dont_cares=None, size=0, are_minterms=None):
        if dont_cares is None:
            dont_cares = []
        if are_minterms is None:
            self.map = values
        elif are_minterms:
            self.map = [False] * size
            for value in values:
                self.map[value] = True
            for dc in dont_cares:
                self.map[dc] = None
        else:
            self.map = [True] * size
            for value in values:
                self.map[value] = False
            for dc in dont_cares:
                self.map[dc] = None

    def combine(self, operation, *others):
        # LogicalFunction.count += 1
        return operation.perform(self, *others)

    def __str__(self):
        return str(self.map)

    def __repr__(self):
        return str(self.map)

    def size(self):
        return len(self.map)

    def __eq__(self, other):
        # if not isinstance(other, LogicalFunction):
        #     return False
        # if len(self.map) != len(other.map):
        #     return False
        # for i in range(0, 10):
        #     if self.map[i] != other.map[i]:
        #         return False
        #     if self.map[i] is None or other.map[i] is None:
        #         continue
        # return True
        return self.map[:10] == other.map[:10]

    def __add__(self, other):
        return self.__or__(other)

    def __or__(self, other):
        return self.combine(LogicalOperators.OR, other)

    def __mul__(self, other):
        return self.__and__(other)

    def __and__(self, other):
        return self.combine(LogicalOperators.AND, other)

    def __xor__(self, other):
        return self.combine(LogicalOperators.XOR, other)

    def __invert__(self):
        return self.combine(LogicalOperators.NOT)

    def __deepcopy__(self, memodict={}):
        return self.copy()

    def __copy__(self):
        return self.copy()

    def copy(self):
        return LogicalFunction(self.map.copy())

    def __sizeof__(self):
        return total_size(map)


class LogicalVariable(LogicalFunction):
    def __init__(self, num_of_vars, var_num, size):
        if num_of_vars == -1 and var_num == -1:
            super().__init__([0])
            return

        values = [0] * pow(2, num_of_vars)
        for i in range(0, pow(2, var_num - 1)):
            for j in range(0, pow(2, (num_of_vars - var_num))):
                values[(2 * i + 1) * pow(2, num_of_vars - var_num) + j] = True

        super().__init__(values[:size])


class LogicalOperators(Enum):
    NOT = -1
    OR = 0
    AND = 1
    XOR = 2
    NOR = 3
    NAND = 4
    XNOR = 5
    EQUIV = 5

    # @staticmethod
    # def _or(r, o):
    #     return r or o
    #
    # @staticmethod
    # def _and(r, o):
    #     return r and o
    #
    # @staticmethod
    # def _xor(r, o):
    #     return r != o
    #
    # @staticmethod
    # def _equiv(r, o):
    #     return r == o

    def perform(self, *operands):
        if self == LogicalOperators.OR:
            return self._or(*operands)
        elif self == LogicalOperators.AND:
            return self._and(*operands)
        elif self == LogicalOperators.XOR:
            return self._xor(*operands)
        elif self == LogicalOperators.NOR:
            return self._nor(*operands)
        elif self == LogicalOperators.NAND:
            return self._nand(*operands)
        elif self == LogicalOperators.XNOR:
            return self._equiv(*operands)
        # if self == LogicalOperators.OR:
        #     return self.generic_operation(self._or, *operands)
        # elif self == LogicalOperators.AND:
        #     return self.generic_operation(self._and, *operands)
        # elif self == LogicalOperators.XOR:
        #     return self.generic_operation(self._xor, *operands)
        # elif self == LogicalOperators.NOR:
        #     return self._not(self.generic_operation(self._or, *operands))
        # elif self == LogicalOperators.NAND:
        #     return self._not(self.generic_operation(self._and, *operands))
        # elif self == LogicalOperators.EQUIV:
        #     return self.generic_operation(self._equiv, *operands)
        elif self == LogicalOperators.NOT:
            return self._not(operands[0])
        else:
            # TODO: throw error here
            return None

    # @staticmethod
    # def generic_operation(operation_function, *operands):
    #     # TODO: We assume that all operands are the same size, in general, we should throw an error if they aren't
    #     size = operands[0].size()
    #     result = operands[0].copy()
    #     for o in range(1, len(operands)):
    #         for i in range(0, size - 6):
    #             result.map[i] = operation_function(result.map[i], operands[o].map[i])
    #     return result

    @staticmethod
    def _not(operand):
        result = operand.copy()
        for i in range(0, operand.size()):
            if operand.map[i] is None:
                result.map[i] = None
            else:
                result.map[i] = not operand.map[i]
        return result

    @staticmethod
    def _or(*operands):
        # TODO: Currently, we assume that all operands are the same size, we should throw an error if they aren't
        size = operands[0].size()
        result = operands[0].copy()
        for o in range(1, len(operands)):
            for i in range(0, size):
                # if operands[o].map[i] is None or result.map[i] is None:
                #     result.map[i] = None
                # else:
                result.map[i] = result.map[i] or operands[o].map[i]
        return result

    @staticmethod
    def _and(*operands):
        size = operands[0].size()
        result = operands[0].copy()
        for o in range(1, len(operands)):
            for i in range(0, size):
                # if operands[o].map[i] is None or result.map[i] is None:
                #     result.map[i] = None
                # else:
                result.map[i] = result.map[i] and operands[o].map[i]
        return result

    @staticmethod
    def _xor(*operands):
        size = operands[0].size()
        result = operands[0].copy()
        for o in range(1, len(operands)):
            for i in range(0, size):
                # if operands[o].map[i] is None or result.map[i] is None:
                #     result.map[i] = None
                # else:
                result.map[i] = result.map[i] != operands[o].map[i]
        return result

    @staticmethod
    def _nor(*operands):
        return LogicalOperators._not(LogicalOperators._or(*operands))

    @staticmethod
    def _nand(*operands):
        return LogicalOperators._not(LogicalOperators._and(*operands))

    @staticmethod
    def _equiv(*operands):
        return LogicalOperators._not(LogicalOperators._xor(*operands))


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
