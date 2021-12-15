'''
Created on Mar 30, 2019

@author: Tavis
'''

def permutations(number):
    numString = str(number)
    if len(numString) == 1:
        return list(map(int, numString))
    perms = []
    r_perms = list(map(str, permutations(int(numString[1:]))))
    first_digit = numString[0]
    for perm in r_perms:
        for i in range(len(perm)+1):
            p_perm = perm[:i]+first_digit+perm[i:]
            perms.append(p_perm)
    return list(map(int, perms))

def permutations_unique(number):
    #number of occurences per number
    num_occur = group_by_num(number)
    starting_string = '0'*num_occur[0]
    perms = [starting_string]
    for i in range(1, 10):
        if num_occur[i] == 0:
            continue
        perms = permute(perms, i, num_occur[i])
    return list(map(int, perms))

def permute(perms, num, occurrences):
    r_perms = perms
    for i in range(occurrences):
        r_perms = permute2(r_perms, num)
    return r_perms
def permute2(perms, num):
    r_perms = []
    for perm in perms:
        for i in range(perm.rfind(str(num))+1, len(perm)+1):
            r_perms.append(perm[:i]+str(num)+perm[i:])
    return r_perms

def group_by_num(number):
    list = [0,0,0,0,0,0,0,0,0,0]
    for n in str(number):
        list[int(n)]+=1
    return list

def div2(num):
    return int(str(num)[-1:]) % 2 == 0
def div3(num):
    return sum(list(map(int, str(num)))) % 3 == 0
def div5(num):
    return int(str(num)[-1:]) == 0 or int(str(num)[-1:]) == 5
def div7(num):
    return num % 7 == 0
#checks if a number is divisible by only single digit numbers
def digit_div(num):
    while True:
        if not div2(num):
            break
        num = int(num/2)
    while True:
        if not div3(num):
            break
        num = int(num/3)
    while True:
        if not div5(num):
            break
        num = int(num/5)
    while True:
        if not div7(num):
            break
        num = int(num/7)
    return num == 1 or num == 0

def digit_div_min(num):
    while True:
        if not div2(num):
            break
        num = int(num/2)
    while True:
        if not div7(num):
            break
        num = int(num/7)
    return num == 1 or num == 0
#checks if any of the numbers in the list are divisible by only single digit numbers and returns those that are
def list_div(nums):
    div_nums = []
    for num in nums:
        if digit_div_min(num):
            div_nums.append(num)
    return div_nums
#perms = permutations_unique(19208)
#perms = permutations_unique(19208)
#print(perms)
#print(str(len(perms)))
#print(list_div(perms))

#x = random.randint(0, 100000)
#print(x)
#print(div2(x))
#print(div3(x))
#print(div5(x))
#print(div7(x))





