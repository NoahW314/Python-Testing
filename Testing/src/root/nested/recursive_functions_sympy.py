from sympy import *


def fibonacci(n):
    if n > 1:
        return fibonacci(n - 1) + +fibonacci(n - 2)
    elif n == 1:
        return symbols("a")
    elif n == 0:
        return symbols("b")


a, b, c = symbols("a b c")


def risk_recursion_simple(n, x, c=0, d=0):
    if n > c and x > d:
        return a * risk_recursion_simple(n - 1, x, c, d) + b * risk_recursion_simple(n, x - 1, c, d)
    elif n <= c:
        return Function("g")(x)
    elif x <= d:
        return Function("h")(n)


def risk_closed_simple(n, x, c=0, d=0):
    i, j = symbols("i j")
    return Sum((a ** (n - c)) * (b ** i) * Function("g")(x - i) * binomial(i + n - c - 1, i),
               (i, 0, x - d - 1)).doit() + \
           Sum((b ** (x - d)) * (a ** i) * Function("h")(n - i) * binomial(i + x - d - 1, i), (i, 0, n - c - 1)).doit()


"""for n in range(4, 7):
    for x in range(3, 7):
        recurs = simplify(expand(risk_recursion_simple(n, x, 3, 2)))
        closed = simplify(expand(risk_closed_simple(n, x, 3, 2)))
        # print(str(n) + " " + str(x) + ": " + str(recurs))
        # print(str(n) + " " + str(x) + ": " + str(closed))
        print(recurs - closed == 0)"""


def risk_recursion(n, x, upper_d=0, upper_e=0, switched=(False, False)):
    d_0 = upper_d if n % 2 == upper_d % 2 else upper_d - 1
    d_1 = upper_d - 1 if n % 2 == upper_d % 2 else upper_d
    e_0 = upper_e if x % 2 == upper_e % 2 else upper_e - 1
    e_1 = upper_e - 1 if x % 2 == upper_e % 2 else upper_e

    if n > upper_d and x > upper_e:
        return a * risk_recursion(n - 2, x, upper_d, upper_e, switched) + \
               b * risk_recursion(n - 1, x - 1, upper_d, upper_e, (not switched[0], not switched[1])) + \
               c * risk_recursion(n, x - 2, upper_d, upper_e, switched)
    elif n == d_0:
        return Function("g_0")(x) if not switched[0] else Function("g_1")(x)
    elif n == d_1:
        return Function("g_1")(x) if not switched[0] else Function("g_0")(x)
    elif x == e_0:
        return Function("h_0")(n) if not switched[1] else Function("h_1")(n)
    elif x == e_1:
        return Function("h_1")(n) if not switched[1] else Function("h_0")(n)


def risk_partial_recursion(n, x, upper_d=0, upper_e=0, switched=(False, False)):
    d_0 = upper_d if n % 2 == upper_d % 2 else upper_d - 1
    d_1 = upper_d - 1 if n % 2 == upper_d % 2 else upper_d
    e_0 = upper_e if x % 2 == upper_e % 2 else upper_e - 1
    e_1 = upper_e - 1 if x % 2 == upper_e % 2 else upper_e
    assert (n - d_0) % 2 == 0
    assert (x - e_0) % 2 == 0
    d = int((n - d_0) / 2)
    e = int((x - e_0) / 2)

    if n > upper_d and x > upper_e:
        _sum1, _sum2, _sum3 = 0, 0, 0
        g_func_str = "g_0" if not switched[0] else "g_1"
        h_func_str = "h_0" if not switched[1] else "h_1"
        for i in range(0, e):
            _sum1 += (a ** d) * (c ** i) * Function(g_func_str)(x - 2 * i) * binomial(i + d - 1, i)
        for i in range(0, d):
            _sum2 += (c ** e) * (a ** i) * Function(h_func_str)(n - 2 * i) * binomial(i + e - 1, i)
        for i in range(0, e):
            for j in range(0, d):
                _sum3 += b * (a ** j) * (c ** i) * binomial(i + j, i) * \
                         risk_partial_recursion(n - 2 * j - 1, x - 2 * i - 1, upper_d, upper_e,
                                                (not switched[0], not switched[1]))
        return _sum1 + _sum2 + _sum3

    elif n == d_0:
        return Function("g_0")(x) if not switched[0] else Function("g_1")(x)
    elif n == d_1:
        return Function("g_1")(x) if not switched[0] else Function("g_0")(x)
    elif x == e_0:
        return Function("h_0")(n) if not switched[1] else Function("h_1")(n)
    elif x == e_1:
        return Function("h_1")(n) if not switched[1] else Function("h_0")(n)


def partial_recursion(n, x, upper_d, upper_e, switched):
    d_0 = upper_d if n % 2 == upper_d % 2 ^ switched[0] else upper_d - 1
    e_0 = upper_e if x % 2 == upper_e % 2 ^ switched[1] else upper_e - 1
    d = (n - d_0) / 2
    e = (x - e_0) / 2

    _sum = 0
    try:
        for i in range(0, int(e)):
            for j in range(0, int(d)):
                _sum += b * (a ** j) * (c ** i) * binomial(i + j, i) * \
                        risk_partial_recursion(n - 2 * j - 1, x - 2 * i - 1, upper_d, upper_e,
                                               switched=(not switched[0], not switched[1]))
    except TypeError as err:
        print(err)
        raise err
    return _sum


def test_risk_partial_recursion(last_n, last_x):
    for n in range(5, last_n+1):
        for x in range(4, last_x+1):
            recurs = simplify(expand(risk_recursion(n, x, 3, 2)))
            closed = simplify(expand(risk_partial_recursion(n, x, 3, 2)))

            same = (recurs - closed == 0)
            print(str(same) + " " + str(n) + " " + str(x))
            if not same:
                print(recurs)
                print(closed)
                print()

    print("Done")


test_risk_partial_recursion(10, 10)
