from itertools import combinations
from math import floor


def generate_primes(max_num):
    primes = []
    possible_numbers = list(range(2, max_num + 1))
    for num in possible_numbers:
        primes.append(num)
        for i in range(2, floor(max_num / num) + 1):
            try:
                possible_numbers.remove(num * i)
            except ValueError:
                pass
    return primes


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
    primes = generate_primes(max_prime)
    nums_to_factors = {}
    for prime in primes:
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
        if evaluate_prediction(factors, prediction) != 2 in indices:
            remove.add(prediction)
    equivalent_to_3lt1 -= remove


def test_all_predictions(prediction):
    global filtered_primes, almost_primes_and_factors
    for almost_prime in filtered_primes:
        indexes = find_lowest_sum(almost_primes_and_factors[almost_prime],
                                  [lambda p, q, r, s, t, u: p * u + q * t + r * s,
                                   lambda p, q, r, s, t, u: p + q * s + r * t * u])
        if evaluate_prediction(almost_primes_and_factors[almost_prime], prediction) != 2 in indexes:
            return False
    return True


def generate_and_test_predictions():
    conjunction_predictions = set()
    predictions = set()
    operations = ["+", "-"]
    operators = ["^", "v"]
    terms = [0]
    sides = []
    perms = list(combinations(range(0, 6), 2))
    for perm in perms:
        terms.append(str(perm[0]) + str(perm[1]))
    for term1 in terms:
        for term2 in terms:
            for operation in operations:
                sides.append((term1, operation, term2))

    for side1 in sides:
        for side2 in sides:
            predictions.add((side1, (side2[0],)))
    count = 0
    print("Starting prediction and generation...")
    print(len(predictions))
    for predict1 in predictions:
        for predict2 in predictions:
            for operator in operators:
                if test_all_predictions((predict1, operator, predict2)):
                    conjunction_predictions.add((predict1, operator, predict2))
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

almost_primes_and_factors = generate_almost_primes(10**5, 6)
# six_almost_primes = sorted(list(almost_primes_and_factors.keys()))
filtered_primes = filter_primes(almost_primes_and_factors)
factor_names = ["p", "q", "r", "s", "t", "u"]
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

equivalent_to_3lt1 = generate_and_test_predictions()

print()
# print(len(implies_three_lt1))
# print(len(three_lt1_implies))
# intersection = implies_three_lt1 & three_lt1_implies
# print(len(intersection))
print(len(equivalent_to_3lt1))

# Print sample
def print_sample(sets):
    copy_set = sets.copy()
    for i in range(0, min(len(copy_set), 10)):
        element = copy_set.pop()
        str1 = factor_names[int(element[0][0][0])]+"*"+factor_names[int(element[0][0][1])] if isinstance(element[0][0], str) else str(0)
        str2 = factor_names[int(element[0][2][0])]+"*"+factor_names[int(element[0][2][1])] if isinstance(element[0][2], str) else str(0)
        str3 = factor_names[int(element[1][0][0])]+"*"+factor_names[int(element[1][0][1])] if isinstance(element[1][0], str) else str(0)
        print(str1+element[0][1]+str2+" <= "+str3)

print()
print_sample(equivalent_to_3lt1)
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

