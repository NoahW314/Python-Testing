"""Program for testing different strategy ideas for each player

With random strategy, ~12 turns per game
With winning strategy, ~6 turns per game, 2nd player always wins
With winning-random strategy and stalling, 2nd player wins ~80% of the time

"""
from itertools import product
from random import randrange, seed
from timeit import default_timer as time

from root.nested.chopsticks.analysis import find_trap_nodes, allow_stall
from root.nested.chopsticks.tree import Node, generate_circle, start_node, hands, fingers


def random_strategy(moves):
    return moves[randrange(0, len(moves))]

def winning_strategy(moves):
    for trap_nodes in trap_nodes_list:
        for move in moves:
            # return the first move that we come across that takes us to a trap node
            # this should advance us towards the end nodes safely as quickly as possible
            if move in trap_nodes:
                return move
    return moves[randrange(0, len(moves))]


def play_a_game(starting_state, moves, strategy1, strategy2):
    state = starting_state
    player_turn = 0
    while state.winner() is None:
        if not player_turn:
            state = strategy1(moves[state])
        else:
            state = strategy2(moves[state])
        player_turn = not player_turn
    assert player_turn



all_nodes = set()
all_values = product(range(0, fingers), repeat=2*hands)
for value in all_values:
    all_nodes.add(Node([[value[i] for i in range(0, hands)], [value[i] for i in range(hands, 2*hands)]]))
all_moves = generate_circle(all_nodes, allow_stall=allow_stall, use_list=True)

trap_nodes_list = find_trap_nodes(start_node)


seed()
games = 10**2
start_time = time()
for i in range(0, games):
    play_a_game(start_node, all_moves, winning_strategy, random_strategy)
end_time = time()
print(end_time-start_time)
