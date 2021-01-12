from itertools import combinations
from timeit import default_timer as time

combos = 10
runs = 1000
perms = combinations(range(0, combos), 2)
set_perms = set()
l_perms = list(combinations(range(0, combos), 2))
l_set_perms = set()
t_perms = tuple(combinations(range(0, combos), 2))
t_set_perms = set()
s_perms = set(combinations(range(0, combos), 2))
s_set_perms = set()

start_time = time()
for i in range(0, runs):
    set_perms = set()
    for perm in perms:
        set_perms.add(perm)
end_time = time()
print(end_time-start_time)

start_time = time()
for i in range(0, runs):
    l_set_perms = set()
    for perm in l_perms:
        l_set_perms.add(perm)
end_time = time()
print(end_time-start_time)

start_time = time()
for i in range(0, runs):
    t_set_perms = set()
    for perm in t_perms:
        t_set_perms.add(perm)
end_time = time()
print(end_time-start_time)

start_time = time()
for i in range(0, runs):
    s_set_perms = set()
    for perm in s_perms:
        s_set_perms.add(perm)
end_time = time()
print(end_time-start_time)
print()
print(set_perms == l_set_perms)
print(set_perms == t_set_perms)
print(set_perms == s_set_perms)
