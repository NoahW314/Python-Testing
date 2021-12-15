
# returns a tuple containing the number of solutions as the first element and the solution as the second (if it exists)
# 0 - no solutions, 1 - unique solution, 2 - infinite number of solutions
# Assume that matrix is of the form A[row][column]
def solve(A, b):
    # Create ACM
    ACM = [row.copy() for row in A]
    for i in range(0, len(A)):
        ACM[i].append(b[i])

    col = 0
    rowsDown = 0
    # Repeat for all columns
    while col != -1:
        # Find the left-most column with a non-zero entry,
        # ignoring the first rowsDown-1 elements of each column
        # when rowsDown == len(ACM), then col = -1 and the loop will end
        col = -1
        row = -1
        for j in range(0, len(ACM[0])):
            for k in range(rowsDown, len(ACM)):
                if ACM[k][j] != 0:
                    col = j
                    row = k
                    break
            if col != -1:
                break
        # If there is no such element, then the matrix is all zeros, so we are done
        if col != -1:
            # Switch two rows so that this column has a non-zero entry on row rowsDown
            if row != rowsDown:
                tempRow = ACM[row].copy()
                ACM[row] = ACM[rowsDown].copy()
                ACM[rowsDown] = tempRow.copy()
            # Divide row rowsDown by the left-most non-zero element so that it becomes 1
            diag = ACM[rowsDown][col] # The previous switch ensures that this is non-zero
            for j in range(col, len(ACM[0])):
                ACM[rowsDown][j] /= diag
            # Zero out all the other elements in this column
            for j in range(0, len(ACM)):
                if j != rowsDown:
                    mult = -ACM[j][col]
                    for k in range(col, len(ACM[0])):
                        ACM[j][k] += mult*ACM[rowsDown][k]
            rowsDown += 1

    # Determine if the system is consistent, inconsistent, and/or has a free column
    consistent = True
    has_free = False

    inconsistent_row = [0]*len(ACM[0])
    inconsistent_row[-1] = 1
    for row in ACM:
        if row == inconsistent_row:
            consistent = False
            break

    for j in range(0, len(ACM[0]) - 1):
        is_pivot = False
        for k in range(0, len(ACM)):
            if ACM[k][j] != 0:
                first_el = ACM[k][j]
                # check if this element is a pivot
                if first_el == 1:
                    is_pivot = True
                    l = 0
                    while l <= j:
                        if l < j and ACM[k][l] != 0:
                            is_pivot = False
                            break
                        l += 1
                break
        if not is_pivot:
            has_free = True
            break

    if not consistent:
        code = 0
    elif not has_free:
        code = 1
    else:
        code = 2

    return code, ACM

def print_mat(mat):
    for row in mat:
        for el in row:
            print('{:g}'.format(el), end="  ")
        print()
    print()
