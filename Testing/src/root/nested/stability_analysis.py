from tabulate import tabulate
from itertools import combinations_with_replacement, product, permutations
from math import factorial

letters = 'abcdefghijklmnopqrstuvwxyz'
letter_to_pref = {}
def is_different(comb):
    for c in comb:
        if letter_to_pref[c][0] != letter_to_pref[comb[0]][0]:
            return True
    return False
def generate_combs(n):
    prefs = sorted(permutations(''.join(list(map(str, range(1,n+1))))))
    if len(prefs) > 26:
        raise ValueError()
    for i in range(len(prefs)):
        letter_to_pref[letters[i]] = ''.join(list(map(str, prefs[i])))
    print(letter_to_pref)
    
    combs = list(combinations_with_replacement(letter_to_pref.keys(), n))
    combs = list(map(''.join, combs))
    
    combs = [comb for comb in combs if is_different(comb)]
    print(combs)
    return combs
def shrinkable(prefs1, prefs2):
    for pref in prefs1:
        first_choice = letter_to_pref[pref][0]
        if prefs1[int(letter_to_pref[prefs2[int(first_choice)-1]][0])-1] == pref:
            return True
    return False
def generate_perms_single(comb, n):
    perms = sorted(list(map(''.join, product(letters[:factorial(n)], repeat=n))))
    return [perm for perm in perms if not shrinkable(comb, perm)]
def will_swap_comb_basic(comb, i, pair):
    return pair[i] != int(letter_to_pref[comb[i]][0])
def will_swap(comb, perm, ic, ip, pair):
    c_pref = letter_to_pref[comb[ic]]
    p_pref = letter_to_pref[perm[ip]]
    
    try:
        return c_pref.index(str(ip+1)) < c_pref.index(str(pair[ic])) and p_pref.index(str(ic+1)) < p_pref.index(str(pair.index(ip+1)+1))
    except:
        raise
def is_stable(comb, perm, pair):
    for i in range(len(comb)):
        if will_swap_comb_basic(comb, i, pair):
            c_pref = letter_to_pref[comb[i]]
            
            pair_index_in_pref = c_pref.index(str(pair[i]))
            will_swap_with = c_pref[:pair_index_in_pref]
            for j in range(len(will_swap_with)):
                if will_swap(comb, perm, i, int(will_swap_with[j])-1, pair):
                    return False
    return True
def stable_pairings(comb, perm):
    pairs = list(permutations(range(1, len(comb)+1)))
    return [pair for pair in pairs if is_stable(comb, perm, pair)]
def stable_pairings_perms(comb, perms):
    pairings = {}
    for perm in perms:
        pairings[perm] = stable_pairings(comb, perm)
    return pairings
def all_stable_pairings(combs, n):
    pairings = {}
    for i in range(len(combs)):
        perms = generate_perms_single(combs[i], n)
        pairings[combs[i]] = {}
        for perm in perms:
            pairings[combs[i]][perm] = stable_pairings(combs[i], perm)
    return pairings
def tabulate_pairings_perms(pairings):
    return tabulate(pairings)
def count_of(perm_pairs, n):
    count = [0]*(factorial(n)+1)
    for perm_pair in perm_pairs:
        count[len(perm_pairs[perm_pair])]+=1
    return count
def tabulate_pairings(pairings, n):
    string = ''
    for comb in pairings:
        string+="\n"+comb+"  "+str(count_of(pairings[comb], n))+"\n"
        string+=tabulate(pairings[comb], headers='keys')
    return string+'\n'
num = 3
combs = generate_combs(num)
#comb = combs[0]
#perms = generate_perms_single(comb, num)
print()
print(combs)
#print(perms)
print()
#stable_pairs = stable_pairings_perms(comb, perms)
stable_pairs = all_stable_pairings(combs, num)
tabled_pairings = tabulate_pairings(stable_pairs, num)

print(tabled_pairings)
f = open('pairings.txt', 'w')
f.write(tabled_pairings)
print("Done")

