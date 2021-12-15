from math import sqrt
from typing import Dict, Any, Union

cases = [0, 0, 0, 0]
for i in range(-4, 5):
    for j in range(-4, 5):
        if i != 0 and j != 0:
            determinant = (i-1)**2-4*j
            if determinant > 0 and abs(i-1) != abs(determinant):
                if sqrt(determinant).is_integer():
                    cases[0] += 1
            elif determinant == 0 and i != 1:
                cases[1] += 1
            elif determinant < 0:
                if sqrt(-determinant).is_integer():
                    cases[2] += 1
            else:
                cases[3] += 1
# print(cases)


# acceptable = []
# wrong = []
# maxTerms = 0
# maxTerm = 0
# for a in range(-4, 5):
#     for b in range(-4, 5):
#         for c in range(-4, 5):
#             for d in range(-4, 5):
#                 for e in range(-3, 4):
#                     f = e/10
#                     if a == 0 or b == 0 or c == 0 or d == 0 or f == 0:
#                         continue
#
#                     works = True
#                     an1 = d
#                     an = c
#                     ans = c
#                     n = 2
#                     term = d*f
#                     prevTerm = c
#                     while abs(term) > 0.01 or abs(prevTerm) > 0.01:
#                         maxTerm = max(maxTerm, abs(term))
#                         if abs(term) >= 1000 or abs(ans) > 10**6:
#                             works = False
#                             break
#                         ans += term
#                         an2 = -3*an1/(a*n)-(n-2+b)*an/(a*n*(n-1))
#                         prevTerm = term
#                         term = an2*(f**n)
#                         n += 1
#                     if works:
#                         maxTerms = max(maxTerms, n)
#                         acceptable.append((b, c, d, f, n))
#                     else:
#                         wrong.append((b, c, d, f, n))
#
# print(len(acceptable))
# print(maxTerms)
# print(maxTerm)

freqs = {
    "e": 12,
    "t": 9.1,
    "a": 8.1,
    "o": 7.7,
    "i": 7.3,
    "n": 7,
    "s": 6.3,
    "h": 5.9,
    "r": 6,
    "d": 4.3,
    "l": 4,
    "c": 2.7,
    "u": 2.9,
    "m": 2.6,
    "w": 2.1,
    "f": 2.3,
    "g": 2,
    "y": 2.1,
    "p": 1.8,
    "b": 1.5,
    "v": 1.1,
    "k": 0.7,
    "j": 0.1,
    "x": 0.17,
    "q": 0.11,
    "z": 0.07
}
ordered_freqs = [freq for let, freq in freqs.items()]
ordered_freqs.sort(reverse=True)


def getTapsNum(spot):
    if spot == 0:
        return 2
    if 1 <= spot <= 2:
        return 3
    if 3 <= spot <= 5:
        return 4
    if 6 <= spot <= 9:
        return 5
    if 10 <= spot <= 14:
        return 6
    if 15 <= spot <= 18:
        return 7
    if 19 <= spot <= 21:
        return 8
    if 22 <= spot <= 23:
        return 9
    if spot == 24:
        return 10

oneD = 0
twoD = 0
for i in range(0, 25):
    freq = ordered_freqs[i]
    oneD += freq/100*(i+1)
    twoD += freq/100*getTapsNum(i)
print(oneD)
print(twoD)

