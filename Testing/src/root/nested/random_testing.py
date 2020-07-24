'''
Created on Apr 26, 2020

@author: Tavis
'''
from enum import Enum

def method2(*args):
    print(args)
    print(not args)
def method(*args):
    method2(*args)
    print("Non Star")
    method2(args)
    
#method()

class E(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    def is_vowel(self):
        return self == E.A or self == E.E

def enum_test():
    for letter in E:
        print(str(letter)+": "+str(E.B is not letter))
#enum_test()

class Foo():
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
    def __str__(self):
        return str(self.arg1)+", "+str(self.arg2)+", "+str(self.arg3)
cls = Foo
#print(cls)
foo = cls(0, 1, 2)
#print(foo)

old_list = [1, 1, 2, 2, 3, 4, 5]
old_list.remove(2)
print(old_list)