

def test_recursion(recursive_relation, closed_formula, **kwargs):
    recursion_result = recursive_relation(kwargs)
    formula_result = closed_formula(kwargs)
    return recursion_result == formula_result


class RecursiveResult:
    def __init__(self, initial_str=None, expressions=None):
        if initial_str is not None:
            self.expressions = {initial_str: ["1"]}
        elif expressions is not None:
            self.expressions = expressions
        else:
            self.expression = {}

    def __add__(self, other):
        new_expressions = {}
        for our_expression in self.expressions.keys():
            if our_expression in other.expressions.keys():
                new_expressions[our_expression] = self.expressions[our_expression] + other.expressions[our_expression]
            else:
                new_expressions[our_expression] = self.expressions[our_expression]
        for their_expression in other.expressions.keys():
            if their_expression not in self.expressions.keys():
                new_expressions[their_expression] = other.expressions[their_expression]
        return RecursiveResult(expressions=new_expressions)

    def __mul__(self, other):
        new_expressions = {}
        for expression, multipliers in self.expressions.items():
            new_expressions[expression] = []
            for multiplier in multipliers:
                new_expressions[expression].append(other + multiplier)
        return RecursiveResult(expressions=new_expressions)

    def __str__(self):
        string = ""
        for expression, multipliers in self.expressions.items():
            are_multipliers_numbers = are_all_numbers(multipliers)
            if are_multipliers_numbers is not False:
                if are_multipliers_numbers != 1:
                    string += str(int(are_multipliers_numbers))

            else:
                string += "("
                for multiplier in multipliers:
                    string += multiplier + "+"
                string = string[:-1]
                string += ")"

            string += expression + "+"
        string = string[:-1]
        return string


def are_all_numbers(multipliers):
    summation = 0
    try:
        for multiplier in multipliers:
            summation += float(multiplier)
    except ValueError:
        return False
    return summation


def risk_recursion_simple(n, x, g=0, h=0):
    if n > g and x > h:
        return "a" * risk_recursion_simple(n - 1, x, g, h) + "b" * risk_recursion_simple(n, x - 1, g, h)
    elif n <= g:
        return RecursiveResult("g(" + str(x) + ")")
    elif x <= h:
        return RecursiveResult("h(" + str(n) + ")")


def fibonacci_recursion(n, a=0, b=1):
    if n > b:
        return fibonacci_recursion(n - 1) + fibonacci_recursion(n - 2)
    elif n == b:
        return RecursiveResult("b")
    elif n == a:
        return RecursiveResult("a")


for i in range(0, 10):
    print(str(fibonacci_recursion(i)))
