from tabulate import tabulate
from random import randint


def calc_probs(ship_length, board):
    probs = []
    for letter in range(0, 10):
        probs.append([])
        for num in range(0, 10):
            if letter % 2 != num % 2:
                probs[letter].append(" ")
                continue
            # up/down
            positions = 0
            for oset in range(0, ship_length):
                possible = True
                for dist in range(0, ship_length):
                    # out of bounds
                    if num - oset + dist < 0 or num - oset + dist >= 10:
                        possible = False
                        break
                    # contains already hit square
                    if board[letter][num - oset + dist] == 1:
                        possible = False
                        break
                if possible:
                    positions += 1

            # left/right
            for oset in range(0, ship_length):
                possible = True
                for dist in range(0, ship_length):
                    # out of bounds
                    if letter - oset + dist < 0 or letter - oset + dist >= 10:
                        possible = False
                        break
                    # contains already hit square
                    if board[letter - oset + dist][num] == 1:
                        possible = False
                        break
                if possible:
                    positions += 1

            probs[letter].append(positions)
    return probs


def calc_probs_simple(ship_length):
    probs = []
    for letter in range(0, 10):
        probs.append([])
        for num in range(0, 10):
            if letter % 2 != num % 2:
                probs[letter].append(" ")
                continue
            min_dist_l = min(letter + 1, 10 - letter, ship_length)
            min_dist_n = min(num + 1, 10 - num, ship_length)
            probs[letter].append(min_dist_l + min_dist_n)
    return probs


def calc_weighted_sum(ship_probs, weights):
    sum_probs = []
    for letter in range(0, 10):
        sum_probs.append([])
        for num in range(0, 10):
            if letter % 2 != num % 2:
                sum_probs[letter].append("  ")
                continue
            sum = 0
            for i in range(0, len(ship_probs)):
                sum += ship_probs[i][letter][num] * weights[i]
            sum_probs[letter].append(sum)
    return sum_probs


def generate_board(num_shots=None):
    if num_shots is None:
        num_shots = randint(0, 50)
    shots = {}
    for i in range(0, num_shots):
        index = randint(0, 99)
        while index in shots:
            index = randint(0, 99)
        shots[index] = 1

    board = []
    for letter in range(0, 10):
        board.append([])
        for num in range(0, 10):
            if (letter*10+num) in shots:
                board[letter].append(1)
            else:
                board[letter].append(" ")

    return board


weights = [1, 1, 1, 1, 1]
ship_lengths = [2, 3, 3, 4, 5]
board = generate_board()
ship_probs = []
for i in ship_lengths:
    probs = calc_probs(i, board)
    ship_probs.append(probs)
    print(tabulate(probs))
    print(tabulate(board))

weighted_probs = calc_weighted_sum(ship_probs, weights)
print(tabulate(weighted_probs))
print(tabulate(board))
