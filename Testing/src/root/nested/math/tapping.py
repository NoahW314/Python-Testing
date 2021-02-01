
from itertools import combinations, product, permutations
from math import floor, factorial
from timeit import default_timer as time

primes = []
def generate_primes(max_num):
    global primes
    possible_numbers = list(range(2, max_num + 1))
    for num in possible_numbers:
        primes.append(num)
        for i in range(2, floor(max_num / num) + 1):
            try:
                possible_numbers.remove(num * i)
            except ValueError:
                pass


seen_pairs = {}

def generate_almost_primes(max_num, num_of_primes, max_prime=None):
    if num_of_primes == 0:
        return {1: []}
    if (max_num, num_of_primes, max_prime) in seen_pairs:
        return seen_pairs[(max_num, num_of_primes, max_prime)]
    if max_prime is None:
        max_prime = floor(max_num / (2 ** (num_of_primes - 1)))
    else:
        max_prime = min(floor(max_num / (2 ** (num_of_primes - 1))), max_prime)
    nums_to_factors = {}
    for prime in primes:
        if max_prime >= prime:
            break
        smaller_nums_to_factors = generate_almost_primes(floor(max_num / prime), num_of_primes - 1, prime)
        for smaller_num, factors in smaller_nums_to_factors.items():
            nums_to_factors[prime * smaller_num] = [prime, *factors]

    seen_pairs[(max_num, num_of_primes, max_prime)] = nums_to_factors
    return nums_to_factors


def find_lowest_sum(prime_factors, sum_forms):
    sums = []
    for sum_form in sum_forms:
        sums.append(sum_form(*prime_factors))
    lowest_sum = sums[0]
    lowest_sum_indexes = [1]
    for i in range(1, len(sums)):
        if sums[i] < lowest_sum:
            lowest_sum = sums[i]
            lowest_sum_indexes = [i + 1]
        elif sums[i] == lowest_sum:
            lowest_sum_indexes.append(i + 1)
    return lowest_sum_indexes


def filter_primes(almost_primes_to_factors):
    return sorted([prime for prime, factors in almost_primes_to_factors.items() if
                   #   q     *   t       >=     r      *     s      >=     p      >=     r      *      t     >=
                   # factors[1]*factors[4] >= factors[2] * factors[3] >= factors[0] >= factors[2] * factors[4] >=
                                              factors[2] * factors[3] >= factors[0] >= factors[2] * factors[4] >=
                   #   r     *    u      >=    q       >=     t     *   u       >=    s
                   factors[2]*factors[5] >= factors[1] >= factors[4]*factors[5] >= factors[3]])
                   #   q     *   t       >=     p
                   # factors[1]*factors[4] >= factors[0]])


def generate_predictions():
    conjunction_predictions = set()
    predictions = set()
    operations = ["+", "-"]
    operators = ["^", "v"]
    terms = [0]
    sides = []
    perms = list(combinations(range(0, 6), 2))
    for perm in perms:
        terms.append(str(perm[0])+str(perm[1]))
    for term1 in terms:
        for term2 in terms:
            for operation in operations:
                sides.append((term1, operation, term2))

    for side1 in sides:
        for side2 in sides:
            predictions.add((side1, (side2[0],)))
    for predict1 in predictions:
        for predict2 in predictions:
            for operator in operators:
                conjunction_predictions.add((predict1, operator, predict2))
    return conjunction_predictions


# implies_three_lt1 = generate_predictions()
# three_lt1_implies = generate_predictions()
# equivalent_to_3lt1 = generate_predictions()


def eval_sub_predict(factors, prediction, eval_half=False):
    prod1 = factors[int(prediction[0][0])] if isinstance(prediction[0], str) else 0
    prod2 = factors[int(prediction[0][1])] if isinstance(prediction[0], str) else 0
    if not eval_half:
        prod3 = factors[int(prediction[2][0])] if isinstance(prediction[2], str) else 0
        prod4 = factors[int(prediction[2][1])] if isinstance(prediction[2], str) else 0
        if prediction[1] == "+":
            return prod1 * prod2 + prod3 * prod4
        elif prediction[1] == "-":
            return prod1 * prod2 - prod3 * prod4
        else:
            raise ValueError
    else:
        return prod1*prod2


def evaluate_prediction(factors, prediction):
    side1 = eval_sub_predict(factors, prediction[0][0])
    side2 = eval_sub_predict(factors, prediction[0][1], True)
    side3 = eval_sub_predict(factors, prediction[2][0])
    side4 = eval_sub_predict(factors, prediction[2][1], True)
    if prediction[1] == "^":
        return side1 <= side2 and side3 <= side4
    elif prediction[1] == "v":
        return side1 <= side2 or side3 <= side4

def eval_simple_sub_predict(factors, prediction):
    sides = []
    for i in range(0, 4, 2):
        prod1 = factors[int(prediction[i])] if int(prediction[i]) != 6 else 1
        prod2 = factors[int(prediction[i+1])] if int(prediction[i+1]) != 6 else 1
        sides.append(prod1*prod2)
    return sides[0] <= sides[1]

def evaluate_simple_prediction(factors, prediction, indices):
    sides = [True, True]
    for i in range(0, 2):
        for prediction_part in prediction[i]:
            sides[i] &= eval_simple_sub_predict(factors, prediction_part)
    return (sides[0] and (2 in indices)), sides[1]

def test_predictions_implies(factors, indices):
    global implies_three_lt1, three_lt1_implies
    remove_implies = set()
    for prediction in implies_three_lt1:
        if evaluate_prediction(factors, prediction) and 2 not in indices:
            remove_implies.add(prediction)
    implies_three_lt1 -= remove_implies

    remove_implies = set()
    for prediction in three_lt1_implies:
        if not evaluate_prediction(factors, prediction) and 2 in indices:
            remove_implies.add(prediction)
    three_lt1_implies -= remove_implies


def test_predictions(factors, indices):
    global equivalent_to_3lt1
    remove = set()
    for prediction in equivalent_to_3lt1:
        if evaluate_prediction(factors, prediction) != (2 in indices):
            remove.add(prediction)
    equivalent_to_3lt1 -= remove

wrong_count = 0
def test_all_predictions(prediction):
    global filtered_primes, almost_primes_and_factors, wrong_count
    has_false = False
    has_true = False
    for almost_prime, factors in filtered_primes:
        indexes = find_lowest_sum(factors,
                                  [lambda p, q, r, s, t, u: p * u + q * t + r * s,
                                   lambda p, q, r, s, t, u: p + q * s + r * t * u])
        # if evaluate_prediction(almost_primes_and_factors[almost_prime], prediction) != 2 in indexes:
        evaluation = evaluate_simple_prediction(factors, prediction, indexes)
        if not evaluation[0]:
            has_false = True
        else:
            has_true = True
        if evaluation[0] != evaluation[1]:
            return False
    # This ensures that no prediction whose sides are always true is reported as accurate
    # Note that this could cause a false negative if not enough values are tested for a true value to come from the side
    wrong_count += 1
    return has_false and has_true


def less_than_expressions():
    perms = set()
    for i in range(0, 6):
        for j in range(i+1, 7):
            for k in range(0, j):
                for l in range(k+1, 7):
                    if i != k and j != l:
                        if not (i < k and j < l):
                            if not (i > k and j > l):
                                perms.add((i,j,k,l))
    # rs >= p >= rt
    # ru >= q >= tu >= s
    # Remove things we know are true by the above filters we applied to the almost primes
    # (There are more that we could add, involving things that p,q is less than)
    removal = {(0,6,2,3),(2,4,0,6),(2,5,0,6),(3,4,0,6),(3,5,0,6),(4,5,0,6),
              (1,6,2,5),(1,6,2,4),(1,6,2,3),(4,5,1,6),(3,6,4,5),
               (0,6,1,2),(0,6,1,3)}
    perms -= removal
    perms -= {(remove[2],remove[3],remove[0],remove[1]) for remove in removal}
    return perms

def generate_and_test_predictions(n1, n2):
    conjunction_predictions = set()
    predictions = set()
    perms = less_than_expressions()
    for perm in perms:
        predictions.add(str(perm[0]) + str(perm[1]) + str(perm[2]) + str(perm[3]))

    count = 0
    print("Starting prediction and generation...")
    num_pred = len(predictions)
    print(num_pred)
    print((factorial(num_pred)**2)/(factorial(n1)*factorial(n2)*factorial(num_pred-n1)*factorial(num_pred-n2)))
    # for element in predictions:
    #     string = ""
    #     for k in range(0, 4, 2):
    #         string += factor_names[int(element[k])]
    #         string += factor_names[int(element[k + 1])]
    #         string += " <= "
    #     string = string[:-4]
    #     print(string, end="   ")
    #     print(element)

    for prediction1 in combinations(predictions, n1):
        for prediction2 in combinations(predictions, n2):
            if not set(prediction1).isdisjoint(set(prediction2)):
                continue
            if test_all_predictions((prediction1, (*prediction1, *prediction2))):
                conjunction_predictions.add((*prediction1, *(*prediction1, *prediction2)))
            count += 1
            if (count % 1_000_000) == 0:
                print(count)
                if len(conjunction_predictions) > 0:
                    print(len(conjunction_predictions))
                    print_sample(conjunction_predictions)
    print(count)
    return conjunction_predictions


# def prediction(factors, al_prime):
#     return 1


# test_nums = [[6, 5000]]
# for prime_nums, max_num in test_nums:
#     print(sorted(list(generate_almost_primes(max_num, prime_nums).keys())))


# print(len(implies_three_lt1))
# print(len(three_lt1_implies))
# print(len(equivalent_to_3lt1))

start = time()
prime_cap = 10**5
almost_prime_num = 6
generate_primes(floor(prime_cap / (2 ** (almost_prime_num - 1))))
almost_primes_and_factors = generate_almost_primes(prime_cap, almost_prime_num)
end = time()
print(end-start) # 4.511
# six_almost_primes = sorted(list(almost_primes_and_factors.keys()))
filtered_primes = filter_primes(almost_primes_and_factors)
# filtered_primes = filtered_almost_primes(10**6, 6)

factor_names = ["p", "q", "r", "s", "t", "u", ""]
ap_by_factors = {name:{} for name in factor_names}
# for almost_prime in filtered_primes:
#     indexes = find_lowest_sum(almost_primes_and_factors[almost_prime], [lambda p, q, r, s, t, u: p * u + q * t + r * s,
#                                                                         # lambda p, q, r, s, t, u: p + q * r + s * t * u,
#                                                                         lambda p, q, r, s, t, u: p + q * s + r * t * u,
#                                                                         # lambda p, q, r, s, t, u: p + q * t + r * s * u,
#                                                                         # lambda p, q, r, s, t, u: p + q * u + r * s * t,
#                                                                         # lambda p, q, r, s, t, u: p + r * s + q * t * u,
#                                                                         # lambda p, q, r, s, t, u: p + q + r * s * t * u
#                                                                         ])
#     # print(str(almost_prime) + ": " + str(indexes) + ", " + str(almost_primes_and_factors[almost_prime]))
#     # test_predictions_implies(almost_primes_and_factors[almost_prime], indexes)
#     test_predictions(almost_primes_and_factors[almost_prime], indexes)
#
#     # lowests[almost_prime] = indexes
#     # predicted = prediction(almost_primes_and_factors[almost_prime], almost_prime)
#     # if predicted in indexes:
#     #     correct = True
#     # else:
#     #     correct = False
#     #     failed_predictions.append([almost_prime, predicted])
#     # print(str(almost_prime) + ": " + str(indexes) + ", " + str(almost_primes_and_factors[almost_prime])+" "+str(correct))
#     # print(str(almost_prime) + ": " + str(indexes) + ", " + str(almost_primes_and_factors[almost_prime]))
#
#     # factors = almost_primes_and_factors[almost_prime]
#     # for i in range(0, len(factors)):
#     #     try:
#     #         ap_by_factors[factor_names[i]][tuple(factors[:i]+factors[i+1:])].append(
#     #             str(almost_primes_and_factors[almost_prime]) + ": " + str(almost_prime) + ", " + str(indexes))
#     #     except KeyError:
#     #         ap_by_factors[factor_names[i]][tuple(factors[:i]+factors[i+1:])] = [
#     #             str(almost_primes_and_factors[almost_prime]) + ": " + str(almost_prime) + ", " + str(indexes)]

"""(Target, Match)
Match -->    0  1  2  3  4  5  6  7
Target    0  
|         1  
v         2  
          3    
          4  
"""

match = 0
target = 1
equivalent_to_3lt1 = generate_and_test_predictions(target, match)

print()
# print(len(implies_three_lt1))
# print(len(three_lt1_implies))
# intersection = implies_three_lt1 & three_lt1_implies
# print(len(intersection))
wrong_count -= len(equivalent_to_3lt1)
print(len(equivalent_to_3lt1))
print(wrong_count)
# print(test_all_predictions((("1406",),("1406",))))

# Print sample
def print_sample(sets):
    copy_set = sets.copy()
    for i in range(0, min(len(copy_set), 100)):
        element = copy_set.pop()
        str1 = ""
        str2 = ""
        for j in range(2*target+match):
            string = ""
            for k in range(0, 4, 2):
                string += factor_names[int(element[j][k])]
                string += factor_names[int(element[j][k+1])]
                string += " <= "
            string = string[:-4]
            if j < target:
                str1 += string+" ^ "
            else:
                str2 += string+" ^ "
        str1 = str1[:-3]
        str2 = str2[:-3]
        print("3 <= 1 ^ "+str1+" <=> "+str2)

print()
print_sample(equivalent_to_3lt1)
# print(equivalent_to_3lt1)

# print_sample(implies_three_lt1)
print()
print()
# print_sample(three_lt1_implies)

# for name, dicts in ap_by_factors.items():
#     print(name)
#     for factors, num_strs in dicts.items():
#         print("\t"+str(factors))
#         for num_str in num_strs:
#             print("\t\t"+num_str)
#     print()

