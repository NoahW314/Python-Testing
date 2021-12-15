from math import comb


def compute(m,n):
    combs = comb(m*(m-1)*(m-2),n)
    power = pow(m-3, 2*n)
    poly = n*m*m+2*m*m+n*m
    return combs*power*poly

def compute2(m,n):
    combs = comb(m*(m-1)*(m-2)-1,n-1)
    power = pow(m-3,n)*pow(m-4,n)
    poly = n*m*m+2*m*m+n*m
    return combs*power*poly


# for m in range(4, 7):
#     print(m)
#     for n in range(1,5):
#         print(str(n)+" %e" % compute(m,n))
#     for n in range(5, m*(m-1)*(m-2), 10):
#         print(str(n)+" %e" % compute(m,n))
#     print(str(m*(m-1)*(m-2))+" %e" % compute(m,m*(m-1)*(m-2)))
#     print()

# print("%e" % compute2(6,3))
# print("%e" % compute2(6,4))
# print("%e" % compute2(6,5))
# print("%e" % compute2(6,120))
print("%e" % compute2(6,6))