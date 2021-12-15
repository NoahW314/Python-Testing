
class WarResult:
    def __init__(self, attackers, defenders):
        self.result = [attackers, defenders]
        
    def __add__(self, other):
        return WarResult(self.result[0]+other.result[0], self.result[1]+other.result[1])

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))
    
    def __mul__(self, scale):
        return WarResult(self.result[0]*scale, self.result[1]*scale)

    def __abs__(self):
        return WarResult(abs(self.result[0]), abs(self.result[1]))

    def __eq__(self, other):
        return self.result == other.result
    
    def __str__(self):
        return "[{:.2f}, {:.2f}]".format(self.result[0], self.result[1])

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.result[item]