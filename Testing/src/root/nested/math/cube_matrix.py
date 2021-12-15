'''
Created on Apr 3, 2019

@author: Tavis
'''
from itertools import permutations

class Matrix():
    
    def __init__(self, d=[0,1,2]):
        self.data = d

    def __add__(self, other):
        return Matrix(Matrix.operate_lists_elementwise(self.data, other.data, lambda x,y: (x+y)%3))
    def __sub__(self, other):
        return Matrix(Matrix.operate_lists_elementwise(self.data, other.data, lambda x,y: (x-y)%3))
    def __repr__(self):
        return str(self.data[:2])+'\n'+str(self.data[2:])
    def __eq__(self, other):
        return self.data == other.data

    @staticmethod
    def operate_lists_elementwise(data1, data2, f):
        new_data = []
        for i in range(len(data1)):
            new_data.append(f(data1[i], data2[i]))
        return new_data    
    @classmethod
    def all_permutations(cls):
        perms = list(permutations([0, 1, 2]))
        print(perms)
        matrices = []
        for p in perms:
            matrices.append(Matrix(list(p)))
        return matrices
Matrix.move0 = Matrix([1,2,0])
Matrix.move1 = Matrix([2,0,1])

#print(Matrix()+Matrix([1, 2, 0]))
#print(Matrix.move1+Matrix())

#find a matrix which when added to the start equals the end
def find_solution(start, end):
    data = [0,0,0]
    return Matrix(data)
def test_solution(solution_finder):
    asserted = True
    start_p = list(map(list, permutations([0, 1, 2])))
    end_p = list(map(list, permutations([0, 1, 2])))
    for start in start_p:
        for end in end_p:
            #print(end)
            t = solution_finder(start, end)
            try:
                assert Matrix(start)+t == Matrix(end)
            except AssertionError:
                print("Start: "+str(Matrix(start)))
                print("T: "+str(t))
                print("End: "+str(Matrix(end)))
                #print("S+T: "+str(Matrix(start)+t))
                print()
                asserted = False
    if asserted:
        print("It worked!")
test_solution(find_solution)


