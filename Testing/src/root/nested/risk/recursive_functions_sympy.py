from math import ceil, floor

from sympy import *


def fibonacci(n):
    if n > 1:
        return fibonacci(n - 1) + +fibonacci(n - 2)
    elif n == 1:
        return symbols("a")
    elif n == 0:
        return symbols("b")


a, b, c = symbols("a b c")

# f(d_0,e_0) = f_00, f(d_0,e_1) = f_01
# f(d_1,e_0) = f_10, f(d_1,e_1) = f_11

def base_func(func_str, val, de_tuple):
    """
    :param func_str:
    :param val:
    :param de_tuple: (d_0, d_1, e_0, e_1)
    """
    if func_str == "g_0":
        if val == de_tuple[2]:
            return symbols("f_00")
        if val == de_tuple[3]:
            return symbols("f_01")
    elif func_str == "g_1":
        if val == de_tuple[2]:
            return symbols("f_10")
        if val == de_tuple[3]:
            return symbols("f_11")
    elif func_str == "h_0":
        if val == de_tuple[0]:
            return symbols("f_00")
        if val == de_tuple[1]:
            return symbols("f_10")
    elif func_str == "h_1":
        if val == de_tuple[0]:
            return symbols("f_01")
        if val == de_tuple[1]:
            return symbols("f_11")
    return Function(func_str)(val)

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

# TODO: This could be calculated much faster if done iteratively and recorded results for each combination of n,x, and switches
def risk_recursion(n, x, upper_d=0, upper_e=0, switched=(False, False)):
    d_0 = upper_d if n % 2 == upper_d % 2 else upper_d - 1
    d_1 = upper_d - 1 if n % 2 == upper_d % 2 else upper_d
    e_0 = upper_e if x % 2 == upper_e % 2 else upper_e - 1
    e_1 = upper_e - 1 if x % 2 == upper_e % 2 else upper_e
    de = (d_0, d_1, e_0, e_1)
    de_s = (d_1, d_0, e_1, e_0)

    if n > upper_d and x > upper_e:
        return a * risk_recursion(n - 2, x, upper_d, upper_e, switched) + \
               b * risk_recursion(n - 1, x - 1, upper_d, upper_e, (not switched[0], not switched[1])) + \
               c * risk_recursion(n, x - 2, upper_d, upper_e, switched)
    elif n == d_0:
        return base_func("g_0", x, de) if not switched[0] else base_func("g_1", x, de_s)
    elif n == d_1:
        return base_func("g_1", x, de) if not switched[0] else base_func("g_0", x, de_s)
    elif x == e_0:
        return base_func("h_0", n, de) if not switched[1] else base_func("h_1", n, de_s)
    elif x == e_1:
        return base_func("h_1", n, de) if not switched[1] else base_func("h_0", n, de_s)


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


def risk_no_recursion(n, x, upper_d=0, upper_e=0):
    d_0 = upper_d if n % 2 == upper_d % 2 else upper_d - 1
    d_1 = upper_d - 1 if n % 2 == upper_d % 2 else upper_d
    e_0 = upper_e if x % 2 == upper_e % 2 else upper_e - 1
    e_1 = upper_e - 1 if x % 2 == upper_e % 2 else upper_e
    d_2 = 1 if d_1 == d_0+1 else 0
    e_2 = 1 if e_1 == e_0+1 else 0
    assert (n - d_0) % 2 == 0
    assert (x - e_0) % 2 == 0
    d = int((n - d_0) / 2)
    e = int((x - e_0) / 2)
    d_3 = d - d_2
    e_3 = e - e_2
    de = (d_0, d_1, e_0, e_1)

    if n > upper_d and x > upper_e:
        main_part, f1, f2, f3 = 0, 0, 0, 0
        if d < e:
            M = d + d_3 - 1
            g_func_str = "g_0" if d_2 == 0 else "g_1"
            for i in range(e_3-d+e_2*d_2+1):
                main_part += (b ** (M+1)) * (c ** i) * binomial(i+M, i) * base_func(g_func_str, x - 2 * i - M -1, de)
        else:
            M = e + e_3 -1
            h_func_str = "h_0" if e_2 == 0 else "h_1"
            for i in range(d_3-e+d_2*e_2+1):
                main_part += (b ** (M+1)) * (a ** i) * binomial(i+M, i) * base_func(h_func_str, n - 2 * i - M -1, de)
        for j in range(1, ceil(M/2)+1):
            for i in range(e_3-j+1):
                f1 += (a**(d_3-j+1))*(b**(2*j-1))*(c**i)*binomial(i+d_3+j-1,i)*base_func("g_1",x-2*i-2*j+1,de)*binomial(d+j-1,2*j-1)
            for i in range(d_3-j+1):
                f2 += (a**i)*(b**(2*j-1))*(c**(e_3-j+1))*binomial(i+e_3+j-1,i)*base_func("h_1",n-2*i-2*j+1,de)*binomial(e+j-1,2*j-1)
            f3 += d_2*e_2*(a**(d_3-j+1))*(b**(2*j-1))*(c**(e_3-j+1))*binomial(d+j-2,2*j-2)*binomial(d+e-2,d+j-2)*base_func("g_1",e_1,de)
        for j in range(0, floor(M/2)+1):
            for i in range(e-j):
                f1 += (a**(d-j))*(b**(2*j))*(c**i)*binomial(i+d+j-1,i)*base_func("g_0",x-2*i-2*j,de)*binomial(d_3+j,2*j)
            for i in range(d-j):
                f2 += (a**i)*(b**(2*j))*(c**(e-j))*binomial(i+e+j-1,i)*base_func("h_0",n-2*i-2*j,de)*binomial(e_3+j,2*j)
            f3 += (1-d_2)*(1-e_2)*(a**(d-j))*(b**(2*j))*(c**(e-j))*binomial(d+j-1,2*j-1)*binomial(d+e-1,d+j-1)*base_func("g_0",e_0,de)

        return main_part + f1 + f2 + f3
    elif n == d_0:
        return base_func("g_0",x,de)
    elif n == d_1:
        return base_func("g_1",x,de)
    elif x == e_0:
        return base_func("h_0",n,de)
    elif x == e_1:
        return base_func("h_1",n,de)
    else:
        raise ValueError("n and x are less than their minimum allowable values")

# This doesn't use the new updated terminology for f at two base cases, so it will fail on most tests until the partial recursion algorithm is updated
def test_risk_partial_recursion(last_n, last_x):
    for n in range(5, last_n+1):
        for x in range(4, last_x+1):
            recurs = risk_recursion(n, x, 3, 2)
            closed = risk_partial_recursion(n, x, 3, 2)

            same = (simplify(recurs - closed) == 0)
            print(str(same) + " " + str(n) + " " + str(x))
            if not same:
                print(recurs)
                print(closed)
                print(simplify(recurs-closed))
                print()

    print("Done")


def test_risk_no_recursion(last_n, last_x, exact=False):
    min_n = last_n if exact else 5
    min_x = last_x if exact else 4
    for n in range(min_n, last_n+1):
        for x in range(min_x, last_x+1):
            recurs = risk_recursion(n, x, 3, 2)
            closed = risk_no_recursion(n, x, 3, 2)

            same = (simplify(recurs - closed) == 0)
            print(str(same) + " " + str(n) + " " + str(x))
            if not same:
                print(recurs)
                print(closed)
                print(simplify(recurs-closed))
                print()

    print("Done")


# test_risk_partial_recursion(10, 10)
test_risk_no_recursion(10,10)
