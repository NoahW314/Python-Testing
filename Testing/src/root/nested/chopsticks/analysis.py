
from itertools import product

from root.nested.chopsticks.tree import generate_circle, Node, generate_tree, Tree

"""Notes about the game:
Two versions (or more) are possible, one with stalling and one without stalling.
We make the without stalling game the default version.

Of the 225 valid game states, only 205 can be reached from (1,1),(1,1), 207 can be reached with stalling (Unreachable states listed below)

A node has no children if and only if the game is over (i.e. there is a winner)


"""
# Allow moves which do nothing (e.g. Swapping which hand the fingers are on;  (3,0),(4,1) -> (0,3),(4,1) or (2,1),(4,1) -> (1,2),(4,1))
allow_stall = False

levels = 11
tree = generate_tree(Tree(Node(((1,1),(1,1)))), levels, turn=0, max_depth=levels, env_size=(1000, 1000), allow_stall=allow_stall)
tree_nodes = set()
for node_level in tree.nodes:
    for node in node_level:
        tree_nodes.add(node)
all_nodes = set()
all_values = product(range(0, 5), repeat=4)
for value in all_values:
    all_nodes.add(Node([[value[0], value[1]], [value[2], value[3]]]))
print(len(all_nodes))
# print(all_nodes)
print()

linked_list = generate_circle(all_nodes, allow_stall)
possible_nodes = set()
possible_nodes_0 = set()
losing_nodes_0 = set()
possible_nodes_1 = set()
losing_nodes_1 = set()
possible_loop_nodes = set()

def list_nodes(starting_node, nodes):
    """Determine all nodes which can be reached from starting_node"""
    nodes.add(starting_node)
    for child in linked_list[starting_node]:
        # only explore new nodes
        if child not in nodes:
            list_nodes(child, nodes)

# # Determine all nodes which always result in a loss for player
# def list_losing_nodes(starting_node, nodes, losing_nodes, player, history):
#     nodes.add(starting_node)
#     # If this is an end Node, then determine who won
#     if starting_node.winner() is not None:
#         if player != starting_node.winner():
#             losing_nodes.add(starting_node)
#         return
#     # Otherwise, determine if any of these paths lead to the player's victory
#     is_losing_node = True
#     for child in linked_list[starting_node]:
#         if child not in nodes:
#             history.append(starting_node)
#             list_losing_nodes(child, nodes, losing_nodes, player, history)
#             history.pop()
#             if child not in losing_nodes:
#                 is_losing_node = False
#         # If we have encountered this path directly before, then disregard it.
#         # We don't want to get stuck in a loop
#         # Otherwise, if this child has a path to victory, then we can win using this path
#         elif child not in history and child not in losing_nodes:
#             is_losing_node = False
#         # Sometimes, we can't evaluate a child until resolving something in its history
#         # (e.g. Consider the path (2,0),(1,0) -> ... -> (1,0),(1,0) -> (2,0),(1,0))
#         # The node (1,0),(1,0) has only one child, but we can't determine if it is a losing node until evaluating its
#         # history, specifically the node (2,0),(1,0).
#
#         # Two possibilities
#         # (1) We arrive at this node (1,0),(1,0) through some other chain.  Then if we remove this node from the nodes set now,
#         # we will be able to determine if it is a losing node later.
#         # (2) We never arrive at this node (1,0),(1,0) any other way.  Then it has the same losing-ness as the (2,0),(1,0) node
#         # and can only be accessed through that node, so it is virtually irrelevant.  Could we correct this after though?
#     if is_losing_node:
#         losing_nodes.add(starting_node)

def list_end_nodes(starting_node, nodes, end_nodes):
    """Determine all the end nodes which can be reached from starting_node"""
    nodes.add(starting_node)
    for child in linked_list[starting_node]:
        # If there is a winner, then this child is an end node
        if child.winner() is not None:
            end_nodes.add(child)


# # Determine if any nodes exist which trap the players in an infinite loop, regardless of moves made
# def list_loop_nodes(starting_node, nodes, loop_nodes, history):
#     nodes.add(starting_node)
#     # True if all the children of this node are also in the history list
#     only_in_history = True
#     for child in linked_list[starting_node]:
#         # If we have directly encountered this path before, then check for looping problems
#         if child in history:
#
#         if child not in nodes:
#
print()


# The two overlaps, where both 0 and 1 always lose (how?)[infinite loop?]
# Node(((1, 0), (1, 0)), 1)
# Node(((3, 3), (1, 1)), 1)
# Five overlaps with stalling allowed
# Node(((3, 0), (1, 1)), 1)
# Node(((3, 3), (2, 1)), 1)
# Node(((2, 0), (2, 1)), 1)
# Node(((3, 3), (1, 1)), 1)
# Node(((1, 1), (1, 0)), 1)

# list_losing_nodes(Node(((1,0), (1,0)), turn=1), possible_nodes_0, losing_nodes_0, 0, [])
# list_losing_nodes(Node(((1,0), (1,0)), turn=1), possible_nodes_1, losing_nodes_1, 1, [])
# list_losing_nodes(Node(((1,1), (1,1))), possible_nodes_0, losing_nodes_0, 0, [])
# list_losing_nodes(Node(((1,1), (1,1))), possible_nodes_1, losing_nodes_1, 1, [])
#
# print(len(possible_nodes_0))
# print(len(losing_nodes_0))
# print()
# print(len(possible_nodes_1))
# print(len(losing_nodes_1))
#
# intersection = losing_nodes_0 & losing_nodes_1
# print(len(intersection))
# print(intersection)

list_nodes(Node(((1,1), (1,1))), possible_nodes)



""" Impossible States (w/o Stalling)(Turn: 0):
(0, 0), (0, 0)
(1, 1), (4, 3)
(1, 1), (4, 4)
(2, 1), (4, 3)
(2, 1), (4, 4)
(2, 2), (4, 3)
(2, 2), (4, 4)
(3, 1), (4, 3)
(3, 1), (4, 4)
(3, 2), (4, 3)
(3, 2), (4, 4)
(3, 3), (4, 3)
(3, 3), (4, 4)
(4, 1), (4, 4)
(4, 2), (4, 4)
(4, 3), (4, 0)
(4, 3), (4, 4)
(4, 4), (0, 0)
(4, 4), (4, 0)
(4, 4), (4, 4)
"""
""" Impossible States (w/ Stalling)(Turn: 0):
(0, 0), (0, 0)
(1, 1), (4, 3)
(1, 1), (4, 4)
(2, 1), (4, 3)
(2, 1), (4, 4)
(2, 2), (4, 3)
(2, 2), (4, 4)
(3, 1), (4, 3)
(3, 1), (4, 4)
(3, 2), (4, 3)
(3, 2), (4, 4)
(3, 3), (4, 3)
(3, 3), (4, 4)
(4, 1), (4, 4)
(4, 2), (4, 4)
(4, 3), (4, 4)
(4, 4), (0, 0)
(4, 4), (4, 4)
"""
""" States added by stalling (Turn: 0):
(4, 3), (4, 0)
(4, 4), (4, 0)
"""
