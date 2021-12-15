from root.nested.risk.risk_war import expected_war_value
from root.nested.risk.war_result import WarResult
from cmath import sqrt

def quad(a,b,c,positive=True):
    if positive:
        return (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    else:
        return (-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a)


def calculate(x,y):
    a = 2275/7776
    b = 2611/7776
    c = 2890/7776
    d = 55/216
    f = sqrt(285)/36
    g = 49/144

    r = [0,d*quad(d**2-c,-b,-a), d*quad(d**2-c,-b,-a,False),
         f*quad(f**2-c,-b,-a), f*quad(f**2-c,-b,-a,False),
         f*quad(f**2-c,b,-a), f*quad(f**2-c,b,-a,False),
         g*quad(g**2-a,-b,-c), g*quad(g**2-a,-b,-c,False)]
    t = [r[i]*quad(r[i]**2-a,-b,-c) for i in range(0, 7)]
    s = [r[i]*quad(r[i]**2-a,-b,-c,False) for i in range(0, 7)]
    h = [0, d, d, f, f, -f, -f]
    k = 2107/1447
    l = 5870585/(208368*sqrt(285))
    A = [0, (18 / 11 * r[2] + 1320 / 1447) / ((r[1] ** 2) * (r[2] - r[1])),
         (18 / 11 * r[1] + 1320 / 1447) / ((r[2] ** 2) * (r[1] - r[2])),
         (k + l) / ((r[3] ** 2) * (r[3] - r[4])), (k + l) / ((r[4] ** 2) * (r[4] - r[3])),
         (k - l) / ((r[5] ** 2) * (r[5] - r[6])), (k - l) / ((r[6] ** 2) * (r[6] - r[5]))]
    B = [0, -(2 * a + b) / (b + 2 * c),
         -c / (b + 2 * c) + (2 * a + b) * (1 - a) / ((b + 2 * c) ** 2) - 144 / 95 * (1 - a) / (b + 2 * c),
         49 * (1 - a) / (95 * (b + 2 * c)) - (2 * a + b) * (1 - a) / ((b + 2 * c) ** 2),
         -6129792 * (g ** 2 - a) / (1596665 * g * sqrt(b ** 2 + 4 * c * (g ** 2 - a))),
         6129792 * (g ** 2 - a) / (1596665 * g * sqrt(b ** 2 + 4 * c * (g ** 2 - a)))]
    C = [A[i] * (h[i] - s[i]) / (s[i] - t[i]) for i in range(1, 7)]
    D = [A[i] * (t[i] - h[i]) / (s[i] - t[i]) for i in range(1, 7)]
    C.insert(0, 0)
    D.insert(0, 0)
    zeta = [C[i] * (t[i] ** y) + D[i] * (s[i] ** y) for i in range(1, 7)]
    zeta.insert(0,0)
    alpha_1 = A[1] * (r[1] ** x) + A[2] * (r[2] ** x)
    alpha_2 = A[3] * (r[3] ** x) + A[4] * (r[4] ** x)
    alpha_3 = A[5] * (r[5] ** x) + A[6] * (r[6] ** x)
    beta_1 = B[1] * y + B[2] + B[3] * ((-c / (1 - a)) ** y)
    beta_2 = B[4] * (r[7] ** y) + B[5] * (r[8] ** y)

    print(x+beta_1+beta_2*(g**x)+sum(zeta[i] * (r[i] ** x) for i in range(0, 7))) # This should be 0

    return WarResult(x + 1 + alpha_1 * (d ** y) + alpha_2 * (f ** y) + alpha_3 * ((-f) ** y) +
                     beta_1 + beta_2 * (g ** x) + sum(zeta[i] * (r[i] ** x) for i in range(0, 7)), 0)

"""
Non-degenerate values that don't work (and shouldn't work?):
(2,1)
"""
for y in range(2, 3):
    exact = expected_war_value(2, y)[0]
    calc = calculate(2, y)[0]
    if round(exact.real, 4) != round(calc.real, 4) or\
            round(exact.imag, 4) != round(calc.imag, 4):
        print(str(y)+": "+str(exact)+"  "+str(calc))
    # exact = expected_war_value(3, y)[0]
    # calc = calculate(3, y)[0]
    # if round(exact.real, 4) != round(calc.real, 4) or\
    #         round(exact.imag, 4) != round(calc.imag, 4):
    #     print(str(y) + ": " + str(exact) + "  " + str(calc))