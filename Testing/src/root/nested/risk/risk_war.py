'''
Created on Aug 5, 2020

@author: Tavis
'''
from root.nested.risk.war_result import WarResult
from tabulate import tabulate

def expected_war_value(attackers, defenders):
    if defenders == 0 or attackers == 1:
        return WarResult(attackers, defenders)
    if defenders == 1:
        if attackers == 2:
            a1 = expected_war_value(attackers-1, defenders)
            d1 = expected_war_value(attackers, defenders-1)
            a2 = a1*(7/12)
            d2 = d1*(5/12)
            r = a2+d2
            return r
        if attackers == 3:
            return expected_war_value(attackers-1, defenders)*(91/216)+expected_war_value(attackers, defenders-1)*(125/216)
        if attackers > 3:
            return expected_war_value(attackers-1, defenders)*(441/1296)+expected_war_value(attackers, defenders-1)*(855/1296)
    if defenders > 1:
        if attackers == 2:
            return expected_war_value(attackers-1, defenders)*(161/216)+expected_war_value(attackers, defenders-1)*(55/216)
        if attackers == 3:
            return expected_war_value(attackers-2, defenders)*(571/1296)+expected_war_value(attackers-1, defenders-1)*(440/1296)+expected_war_value(attackers, defenders-2)*(285/1296)
        if attackers > 3:
            return expected_war_value(attackers-2, defenders)*(2275/7776)+expected_war_value(attackers-1, defenders-1)*(2611/7776)+expected_war_value(attackers, defenders-2)*(2890/7776)
        
max_attacker = 11
max_defender = 11
values = []
for a in range(2, max_attacker+1):
    values.append([a])
    for d in range(1, max_defender+1):
        values[a-2].append(expected_war_value(a, d))
d_headers = [""]
d_headers.extend(["{}".format(i) for i in range(1, max_defender+1)])
print(tabulate(values, headers=d_headers))



