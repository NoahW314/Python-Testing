"""
This program tried to find a simple equation to approximate the expected value of a battle in risk.
Unfortunately, this did not work well.  I first attempted to use a linear-ish approximation, but that was too inaccurate
(it varied by up to 1 in some cases [which for values < 10 is a lot (10%ish)]).  Using a quadratic approximation, yielded
better results and reduced error (< 4%), but this equation required 9 constants, with some needing precision down to the
0.001, so it was equally problematic.
Testing in Excel indicated that quadratic was the best fit for this function and it seemed that neither logarithmic nor
exponential would work.  Based on the forms of specific cases of this function, it is possible that a combination of
linear and exponential (i.e. something of the form ax+bc^x) might be a good approximation, but I don't know how to find
these constants.
"""

from root.nested.risk.war_result import WarResult
from numpy import matmul
from numpy.linalg import inv


n = 11
table = [[]]
for x in range(1, n):
    table.append([])
    for y in range(0, n):
        if y == 0 or x == 1:
            table[x].append(WarResult(x, y))
        elif y == 1:
            if x == 2:
                a1 = table[x - 1][y]
                d1 = table[x][y - 1]
                a2 = a1 * (7 / 12)
                d2 = d1 * (5 / 12)
                r = a2 + d2
                table[x].append(r)
            elif x == 3:
                table[x].append(table[x - 1][y] * (91 / 216) + table[x][y - 1] * (125 / 216))
            else:
                table[x].append(table[x - 1][y] * (441 / 1296) + table[x][y-1] * (855 / 1296))
        else:
            if x == 2:
                table[x].append(table[x - 1][y] * (161 / 216) + table[x][y-1] * (55 / 216))
            elif x == 3:
                table[x].append(table[x - 2][y] * (571 / 1296) + table[x - 1][y - 1] * (440 / 1296) + table[x][y - 2] * (285 / 1296))
            else:
                table[x].append(table[x - 2][y] * (2275 / 7776) + table[x - 1][y - 1] * (2611 / 7776) + table[x][y - 2] * (2890 / 7776))

for i in range(1, n):
    print(str(i)+": "+str(table[i]))

# The first thing is to condense the 2d table to a 1d array of linear approximations
# We arbitrarily choose the y dimension to be condensed first.
# Thus, we take a bunch of data points with a constant x and compute the linear approximation across the ys
# The points (x,y) are the y-value of the input and the x/y-value of the output
C = []
A = [[1, j, j**2] for j in range(1, n)]
At = [[A[j][i]  for j in range(len(A))] for i in range(len(A[0]))]
Ac = matmul(inv(matmul(At, A)),At)
for i in range(2,n):
    Yx = [table[i][j].result[0] for j in range(1,n)]
    Yy = [table[i][j].result[1] for j in range(1,n)]
    Cx = matmul(Ac,Yx)
    Cy = matmul(Ac,Yy)
    C.append((Cx, Cy))
    print(i, end=": ")
    print((Cx[0], Cx[1], Cx[2]), end=", ")
    print((Cy[0], Cy[1], Cy[2]))
print()
print()
# Now we have a bunch of linear approximations for E(x,y) for a constant x
# That is, we have approximations for E(1,y), E(2,y), E(3,y), etc.
# So we now want a linear approximation of these approximations
# The data points are then fourfold, one for each constant in each output as the y-value
# The x-value remains the same
A = [[1, j, j**2] for j in range(2, n)]
At = [[A[j][i]  for j in range(len(A))] for i in range(len(A[0]))]
Ac = matmul(inv(matmul(At, A)),At)

A2 = [[1, j] for j in range(2, n)]
At2 = [[A2[j][i]  for j in range(len(A2))] for i in range(len(A2[0]))]
Ac2 = matmul(inv(matmul(At2, A2)),At2)

Yxc = [C[i][0][0] for i in range(0,n-2)]
Yxl = [C[i][0][1] for i in range(0,n-2)]
Yxs = [C[i][0][2] for i in range(0,n-2)]
Yyc = [C[i][1][0] for i in range(0,n-2)]
Yyl = [C[i][1][1] for i in range(0,n-2)]
Yys = [C[i][1][2] for i in range(0,n-2)]
Cxc = matmul(Ac, Yxc)
Cxl = matmul(Ac, Yxl)
Cxs = matmul(Ac, Yxs)
Cyc = matmul(Ac, Yyc)
Cyl = matmul(Ac, Yyl)
Cys = matmul(Ac, Yys)
print(Cxc)
print(Cxl)
print(Cxs)
print(Cyc)
print(Cyl)
print(Cys)
print()

error1_table = [[],[]]
error2_table = [[],[]]
for i in range(2,n):
    error1_table.append([-1])
    error2_table.append([-1])
    for j in range(1,n):
        approx1 = WarResult(C[i-2][0][0] + C[i-2][0][1] * j + C[i-2][0][2] * (j**2),
                            C[i-2][1][0] + C[i-2][1][1] * j + C[i-2][1][2] * (j**2))
        error1_table[i].append(abs(table[i][j]-approx1))

        # approx2 = WarResult((Cxc[0]+Cxc[1]*i+Cxc[2]*(i**2)) + (Cxl[0]+Cxl[1]*i+Cxl[2]*(i**2)) * j + (Cxs[0]+Cxs[1]*i) * (j**2),
        #                     (Cyc[0]+Cyc[1]*i) + (Cyl[0]+Cyl[1]*i+Cyl[2]*(i**2)) * j + (Cys[0]+Cys[1]*i) * (j**2))
        approx2 = WarResult((Cxc[0] + Cxc[1] * i) + (Cxl[0] + Cxl[1] * i) * j + (Cxs[0] + Cxs[1] * i) * (j ** 2),
                            (Cyc[0] + Cyc[1] * i) + (Cyl[0] + Cyl[1] * i) * j + (Cys[0] + Cys[1] * i) * (j ** 2))
        error2_table[i].append(abs(table[i][j]-approx2))

# (error, x, y)
max_error1_x = (0, -1, -1)
max_error1_y = (0, -1, -1)
max_error2_x = (0, -1, -1)
max_error2_y = (0, -1, -1)
for i in range(2, n):
    for j in range(1, n):
        if error1_table[i][j][0] > max_error1_x[0]:
            max_error1_x = (error1_table[i][j][0], i, j)
        if error1_table[i][j][1] > max_error1_y[0]:
            max_error1_y = (error1_table[i][j][1], i, j)
        if error2_table[i][j][0] > max_error2_x[0]:
            max_error2_x = (error2_table[i][j][0], i, j)
        if error2_table[i][j][1] > max_error2_y[0]:
            max_error2_y = (error2_table[i][j][1], i, j)

print((max_error1_x, max_error1_y))
print((max_error2_x, max_error2_y))

