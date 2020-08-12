'''
Created on Aug 5, 2020

@author: Tavis
'''

class WarResult():
    def __init__(self, attackers, defenders):
        self.result = [attackers, defenders]
        
    def __add__(self, other):
        return WarResult(self.result[0]+other.result[0], self.result[1]+other.result[1])
    
    def __mul__(self, scale):
        return WarResult(self.result[0]*scale, self.result[1]*scale)
    
    def __str__(self):
        return "[{:.2f}, {:.2f}]".format(self.result[0], self.result[1])