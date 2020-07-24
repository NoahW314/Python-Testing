'''
Created on May 15, 2020

@author: Tavis
'''

def calculate_losses(attackers, defenders):
    attackers.sort(reverse=True)
    defenders.sort(reverse=True)
    losses = [0, 0]
    for i in range(0, min(len(attackers), len(defenders))):
        if attackers[i] > defenders[i]:
            losses[1] -= 1
        else:
            losses[0] -= 1
    return tuple(losses)
def calc_total(prob):
    total = 0
    for value in prob.values():
        total += value
    return total
def parse_key(key):
    if key[0] == 0:
        string = "Defender"+str(key[1])
    elif key[1] == 0:
        string = "Attacker"+str(key[0])
    else:
        string = "Attacker"+str(key[0])+", Defender"+str(key[1])
    return string
def parse_prob(prob, total):
    string = "\n"
    for key, value in prob.items():
        string+= (parse_key(key)+": "+str(round(value/total, 2))+"%\n")
    return string

probabilities = {}

def recursive_dice(attacker_dice_num, defender_dice_num, probabilities, attacker=[], defender=[]):
    if attacker_dice_num > 0:
        for a in range(1, 7):
            new_attacker = attacker + [a]
            probabilities = recursive_dice(attacker_dice_num-1, defender_dice_num, probabilities, new_attacker, defender)
    elif defender_dice_num > 0:
        for d in range(1, 7):
            new_defender = defender + [d]
            probabilities = recursive_dice(attacker_dice_num, defender_dice_num-1, probabilities, attacker, new_defender)
    else:
        losses = calculate_losses(attacker, defender)
        if losses not in probabilities:
            probabilities[losses] = 0
        probabilities[losses]+=1
    return probabilities

probabilities = recursive_dice(3,2, probabilities)
total = calc_total(probabilities)

print("Probabilities: "+str(probabilities))
print(parse_prob(probabilities, total))
print("Total: "+str(total))
            