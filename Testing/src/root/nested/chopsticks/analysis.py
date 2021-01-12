from collections import deque
from timeit import default_timer as time
from typing import List

from root.nested.chopsticks.tree import start_node, Node

"""Analysis Ideas:
Determining a simple winning/not losing strategy (Complex is done)
Determining a simple strategy that loops the game for ever
Determining a simple losing strategy
"""
# TODO: we changed something about what happens when stalling is allowed, this seems to have changed the stats about this game variant
"""Notes about the game:
Two versions (or more) are possible, one with stalling and one without stalling.
We make the "without stalling" game the default version.
The stalling version simply presents too many options to successfully force a win, which makes it rather uninteresting at present

Of the 225 valid game states, only 192 can be reached from (1,1),(1,1), 194 can be reached with stalling (Unreachable states listed below)
Some like (1,0),(0,0) are not possible because the game should always end with the dead player next up.
Others like (2,1),(4,3) are not possible for unknown reasons. 

A node has no children if and only if the game is over (i.e. there is a winner)

11 levels are needed to display the full tree with 590 nodes (653 nodes with stalling)

There are 14 possible end nodes (i.e. different end states) [This is the 15 valid states minus (0,0),(0,0)]
Every node can either reach every end node, is an end node itself, or is the node (1,0),(4,0).  
This last node is an exception since player 1's only move is to hit the 4 hand with its 1 hand (stalling is not allowed), 
thus it can only end on (0,0),(1,0).  Allowing stalling eliminates this exception.

This is the shortest path (with or without stalling) from the starting ((1,1), (1,1)) node to an end node:
Node(((0, 0), (4, 1))), Node(((4, 1), (3, 0))), Node(((3, 0), (1, 1))), Node(((1, 1), (2, 0))), Node(((1, 1), (1, 1)))

Full breakdown of the shortest path length from a given node to an end node:
length: num of nodes
0: 14
1: 38
2: 93
3: 44
4: 3
The nodes with length 0 to an end node are the end nodes themselves.
The nodes with length 4 are these: Node(((1, 0), (1, 1))), Node(((1, 0), (2, 2))), Node(((1, 1), (1, 1)))
With Stalling:
0: 14
1: 40
2: 93
3: 45
4: 2
The nodes with length 4 are these: Node(((1, 0), (1, 1))), Node(((1, 1), (1, 1)))

There are 3 2-away nodes ("death" nodes) that have no children besides 1-away nodes (i.e. If you are in one of these states, you must go
 to a state which allows the other player to win).  They are (1,0),(4,4), (1,0),(3,0), (1,0),(3,3).  Allowing stalling
 reduces these to just (1,0),(4,4).
The 3 death nodes are children of a combined 13 different nodes (parent death nodes).  These 13 parent death nodes have a
 combined total of 38 unique parent nodes (parent parent death nodes).  Of these 38 parent parent death nodes, only 1 of them,
 (1,0),(1,1), has children who are all parent death nodes, (2,1),(1,0).  Thus if your opponent is in the state (1,0),(1,1), 
 then they will have to go to the state (2,1),(1,0) which allows you to choose to go to the state (1,0),(3,0) which is a death node.
 Thus, your opponent will have to go to (4,0),(1,0), which allows you to win at (0,0),(4,0).  Stalling eliminates this possibility.
Continuing this train of thought back several more moves (~10-12 moves) shows us that the player who starts the game from 
 the typical (1,1),(1,1) node can be forced into losing.  Thus, if the second player plays the game correctly, they can always win.
As before, allowing stalling eliminates the possibility of forcing a win from the beginning.

Using the second player winning strategy, there are approximately 10^6-10^9 different games that could be played.

The 10 nodes which are neither parent nor trap nodes (unclassified nodes) all have at least two children, including at least
 one child which is a parent node and at least one child which is a unclassified node.  None of the children were trap nodes.
"""

# start_time = time()
# all_nodes = set()
# all_values = product(range(0, fingers), repeat=2*hands)
# for value in all_values:
#     all_nodes.add(Node([[value[i] for i in range(0, hands)], [value[i] for i in range(hands, 2*hands)]]))
# end_time = time()
# print(end_time - start_time)
# print()
#
# start_time = time()
# linked_list = generate_circle(all_nodes, allow_stall)
# end_time = time()
# print(end_time-start_time)


linked_list = {}

def list_nodes(starting_node, nodes):
    """Determine all nodes which can be reached from starting_node"""
    nodes.add(starting_node)
    for child in linked_list[starting_node]:
        # only explore new nodes
        if child not in nodes:
            list_nodes(child, nodes)

def list_nodes_non_recursive(starting_node, nodes, end_nodes, parent_nodes):
    """Determine all nodes which can be reached from starting_node.
    Also create the linked_list dictionary as we go along"""

    nodes.add(starting_node)
    children, is_end_node = Node.generate_children(starting_node)
    linked_list[starting_node] = children.copy()

    # Depth-first search
    children_to_investigate = deque()
    children_to_investigate.append(children)
    len_max = 0
    try:
        while len(children_to_investigate) != 0:
            level_children = children_to_investigate.pop()
            while len(level_children) != 0:
                child = level_children.pop()
                if child not in nodes:
                    nodes.add(child)
                    # TODO: This function call takes up the majority of our time (~90%) in this function.
                    # That said, I have no ideas on how to make any part of it faster, everything already seems very optimized
                    # The problem seems to be that it is being called way too many times, but we can't change that either
                    children, is_end_node = Node.generate_children(child)
                    # If this is the parent of an end node, then we no longer care about anything else
                    if is_end_node:
                        nodes.add(children)
                        end_nodes.add(children)
                        parent_nodes.add(child)
                        continue
                    linked_list[child] = children
                    children_to_investigate.append(level_children)
                    level_children = children-nodes
            if len(children_to_investigate) > len_max:
                len_max = len(children_to_investigate)
    except MemoryError as e:
        """
        
        Previous: 312,920; 461,584; 664,887;
        Guess: 964,086 
        bitarray: 764,313
        tuple: 850,165
        """
        del children_to_investigate
        del end_nodes
        del parent_nodes
        print(len(nodes))
        raise e

    print(len(nodes))  #
    print(len(end_nodes))  #
    print(len(parent_nodes))  #
    print()
    print(len(linked_list))  #
    print(len([child for children1 in linked_list.values() for child in children1]))  #
    print()
    print(len_max) #
    print()

    # print(total_time)
    # print(get_tt1()) # 0.059
    # print(get_tt2()) # 0.260
    # print(get_tt3()) # 0.609
    # print(get_tt4()) # 0.947
    # print(get_tt5()) # 0.771
    # print(count)  # 43567
    # print()

def process_change_parent(node, parent_nodes, trap_nodes, other_nodes, parents, starting_node, is_end_parent):
    parent_nodes.add(node)
    other_nodes.discard(node)
    if node == starting_node:
        # If we have classified the starting_node, then we are done
        return True

    if not is_end_parent:
        children = Node.generate_children(node)[0] - parent_nodes - trap_nodes
        try:
            for child in children:
                parents[child].discard(node)
        except KeyError:
            pass

    # notify each parent of this status change and see if this affects anything else
    for parent in parents[node].copy():
        if parent not in parent_nodes and parent not in trap_nodes:
            # if all "parent"'s children are parent nodes, then "parent" is a trap node
            children = Node.generate_children(parent)[0]
            if children <= parent_nodes:
                if process_change_trap(parent, parent_nodes, trap_nodes, other_nodes, parents, starting_node):
                    return True


    # We no longer care about "node"'s parents
    del parents[node]

def process_change_trap(node, parent_nodes, trap_nodes, other_nodes, parents, starting_node):
    trap_nodes.add(node)
    other_nodes.discard(node)
    if node == starting_node:
        # If we have classified the starting_node, then we are done
        return True

    children = Node.generate_children(node)[0] - parent_nodes - trap_nodes
    try:
        for child in children:
            parents[child].discard(node)
    except KeyError:
        pass

    # notify each parent of this status change
    for parent in parents[node].copy():
        if parent not in parent_nodes and parent not in trap_nodes:
            # Each parent now has a trap node as a child (specifically, this node), so they each become parent nodes
            if process_change_parent(parent, parent_nodes, trap_nodes, other_nodes, parents, starting_node, False):
                return True

    # We no longer care about "node"'s parents
    del parents[node]

def list_nodes_and_sort(starting_node):
    """Determine all nodes which can be reached from starting_node and
    sort them into the categories of parent nodes, trap_nodes, and unclassified nodes as we go"""
    # TODO: This program seems pretty optimized for games that have a forced solution in terms of memory.  Perhaps consider a
    # variant on this for programs that aren't likely to finish
    # TODO: How do we deal with determining the depth of a game.  Or rather what metric should we use to indicate the complexity of the forced win?
    # Note that the time each game takes to complete doesn't seem to follow a standard pattern with increasing variables
    # This is likely because the order in which the nodes are explored is arbitrary, so how many nodes need to be explored
    # before the needed nodes are explored can vary greatly, though it seems to be fairly constant for a given game.

    # The basic idea:
    # We do the normal search until we find an end node, then we note the parent of this end node and classify it as a parent node
    # We next note the parent of the parent node. If this makes all of its children parent nodes, then we classify it as a trap node
    # We take this trap node and note that its parents are all parent nodes.
    # We repeat this type of thing until we have either classified the starting node or listed all possible nodes
    # The first condition is a forced win for someone, the second condition is an open (unforced) game

    # We need to keep track of a few things:
    # 1) The nodes we have encountered and their classifications (trap, parent, other) [set(s)]
    start_time = time()
    trap_nodes = set()
    parent_nodes = set()
    other_nodes = {starting_node}
    # 2) The parents of unclassified nodes (once they are classified and their parents notified, we no longer care about their parents) [dict of set(s)]
    # This dict is used to notify parent of a status change in their children
    parents = {}
    # 3) The nodes we have discovered that we need to investigate later
    children_to_investigate = deque()
    children, is_end_node = Node.generate_children(starting_node)
    if is_end_node:
        parent_nodes.add(starting_node)
        trap_nodes.add(children.pop())
        print("The first player wins  1")
        return
    children_to_investigate.append(children)

    for child in children:
        parents[child] = {starting_node}

    done = False
    # We quit when run out of children to investigate or when done is true (i.e. the starting node has been classified)
    while len(children_to_investigate) != 0 and not done:
        level_children = children_to_investigate.pop()
        while len(level_children) != 0:
            child = level_children.pop()
            if child not in other_nodes and child not in parent_nodes and child not in trap_nodes:
                other_nodes.add(child)
                children, is_end_node = Node.generate_children(child)
                if is_end_node:
                    trap_nodes.add(children.pop())
                    # Process the needed changes for "child", which is now a parent node
                    if process_change_parent(child, parent_nodes, trap_nodes, other_nodes, parents, starting_node, True):
                        done = True
                        break
                    else:
                        continue
                # We ignore any children that are parent nodes
                children = children - parent_nodes
                # If you have at least one trap node child, then you are a parent node
                if not children.isdisjoint(trap_nodes):
                    if process_change_parent(child, parent_nodes, trap_nodes, other_nodes, parents, starting_node, False):
                        done = True
                        break
                    else:
                        continue
                # If you have all parent node children, then you are a trap node
                elif len(children) == 0:
                    if process_change_trap(child, parent_nodes, trap_nodes, other_nodes, parents, starting_node):
                        done = True
                        break
                    else:
                        continue
                # We only care about this node's children if it is unclassified
                else:
                    # It should also be noted that all of these children are unclassified, since all the parent node children
                    # were removed earlier and a trap node child would make this node a parent node
                    for child_child in children:
                        try:
                            parents[child_child].add(child)
                        except KeyError:
                            parents[child_child] = {child}
                # We set aside the children we were working on and move onto these children
                if len(level_children) != 0:
                    children_to_investigate.append(level_children)
                level_children = children - other_nodes

    end_time = time()
    print(end_time - start_time)  # 3.886
    # Again, about 80% of our time is spent in the Node.generate_children function

    del parents

    # if we didn't classify the starting node, then there is no forced winner
    if not done:
        print("Parent Nodes: " + str(len(parent_nodes)))
        print("Trap Nodes: " + str(len(trap_nodes)))
        print("Unclassified Nodes: " + str(len(other_nodes)))
        print("Explored Nodes: " + str(len(other_nodes) + len(trap_nodes) + len(parent_nodes)))
        print()
        print("No Winner", end="  ")
        # print("No Winner")
        # Depth Metric:
        # How far away from an end node is the last trap-parent node (i.e. how far in advance would you have to see the trap coming?)
        start_time = time()
        end_nodes = {node for node in trap_nodes if Node.winner(node) is not None}
        trap_nodes -= end_nodes
        next_level = end_nodes.copy()
        depth = 0
        # Note that we never end on an odd depth, since any parent of a trap node is a parent node.
        while len(next_level) != 0:
            level = next_level.copy()
            next_level = set()
            if depth % 2 == 0:
                for node in parent_nodes:
                    children = Node.generate_children(node)[0]
                    # If this node has at least one child in level, then it gets placed in next_level
                    if not children.isdisjoint(level):
                        next_level.add(node)
            else:
                for node in trap_nodes:
                    children = Node.generate_children(node)[0]
                    # If this node has at least one child in level, then it gets placed in next_level
                    if not children.isdisjoint(level):
                        next_level.add(node)
            parent_nodes -= next_level
            trap_nodes -= next_level
            depth += 1

        end_time = time()
        print(depth)
        print(end_time-start_time)
    # otherwise, we proceed to calculate the depth of the game
    else:
        print("Parent Nodes: " + str(len(parent_nodes)))
        print("Trap Nodes: " + str(len(trap_nodes)))
        print("Unclassified Nodes: " + str(len(other_nodes)))
        print("Explored Nodes: " + str(len(other_nodes) + len(trap_nodes) + len(parent_nodes)))
        print()
        if starting_node in trap_nodes:
            start_trap = True
            print("The second player wins", end="  ")
        elif starting_node in parent_nodes:
            start_trap = False
            print("The first player wins", end="  ")
        else:
            # If the starting node wasn't classified, then we have a problem
            assert False

        # Depth Metric:
        # Find the farthest end node (or at least the farthest one on the trap-parent path) (i.e. how long can the doomed player survive?)
        # This is technically an inconsistent metric, since we may not find all paths to all end nodes and the paths that we do find can
        # be different each time.  (In reality, this still gives a good ballpark approximation and successive runs of the program generally
        # yield the same results.)
        start_time = time()
        # Remove the end nodes
        trap_nodes = {node for node in trap_nodes if Node.winner(node) is None}
        next_level = {starting_node}
        # First player wins will have an odd depth, while second player wins will always have an even depth
        depth = 0
        while len(next_level) != 0:
            level = next_level.copy()
            next_level = set()
            if (depth%2 == 0) == start_trap:
                # Trap -> Parent
                # Each trap node only has parent node children, so these are all valid
                for node in level:
                    children = Node.generate_children(node)[0]
                    next_level.update(children)
            else:
                # Parent -> Trap
                for node in level:
                    children = Node.generate_children(node)[0]
                    # Consider only the children which are also trap nodes
                    next_level.update(children & trap_nodes)
                # We assume the winning player takes the shortest path to victory, so we never revisit a trap node
                trap_nodes -= next_level
            depth += 1
        end_time = time()

        print(depth)
        print(end_time-start_time)
        print()
    del trap_nodes
    del parent_nodes
    del other_nodes


def list_end_nodes(starting_node, nodes, end_nodes):
    """Determine all the end nodes which can be reached from starting_node"""
    nodes.add(starting_node)
    for child in linked_list[starting_node]:
        # If there is a winner, then this child is an end node
        if child.winner() is not None:
            end_nodes.add(child)
        # only explore new nodes
        elif child not in nodes:
            list_end_nodes(child, nodes, end_nodes)

def find_quickest_end(starting_node):
    """Determine the shortest path to the end of a game"""
    hit_nodes = set()
    node_paths: List[List[Node]] = [[starting_node]]
    while True:
        new_node_paths = []
        for node_path in node_paths:
            # if we have an end node, then we are done
            if node_path[0].winner() is not None:
                return node_path
            # otherwise, add a path for each of its child nodes
            else:
                for child in linked_list[node_path[0]]:
                    # only explore new nodes
                    if child not in hit_nodes:
                        hit_nodes.add(child)
                        new_node_paths.append([child, *node_path])
        node_paths = new_node_paths.copy()

def find_trap_nodes(starting_node, find_all=False, log=0):
    # We control parent -> trap
    # They control trap -> parent
    remaining_nodes = set()
    end_nodes = set()
    parent_nodes = set()
    start_time = time()
    list_nodes_non_recursive(starting_node, remaining_nodes, end_nodes, parent_nodes)
    remaining_nodes.difference_update(end_nodes)
    remaining_nodes.difference_update(parent_nodes)
    end_time = time()
    print(end_time-start_time)
    total_trap_count = len(end_nodes)
    total_parent_count = len(parent_nodes)
    non_parent_children = linked_list
    if log > 1:
        print("Trap 0: " + str(len(end_nodes)) + " " + str(end_nodes))

    """(4,7)
    13762
    4897
    25034
    
    2.999
    3.826
    
    1.384
    2.714
    """

    tt1 = 0
    tt2 = 0

    # TODO: Currently, we use a breadth first search algorithm.  Could we use a depth first search algorithm instead?
    # If so, implement it and see if it is any faster
    i = 0

    start_time = time()
    trap_nodes = end_nodes
    # keep going until we run out of trap nodes to find parents of
    while len(trap_nodes) != 0:

        # Nodes 2i+2-away from win node
        start_time_1 = time()
        trap_nodes = set()
        for node in remaining_nodes:
            non_parent_children[node] = non_parent_children[node] - parent_nodes
            # nodes whose children are all parent nodes
            if len(non_parent_children[node]) == 0:
                trap_nodes.add(node)
                total_trap_count += 1
                del non_parent_children[node]
        # This part takes almost no time (~0.05%)
        remaining_nodes.difference_update(trap_nodes)
        end_time = time()
        tt2 += end_time - start_time_1

        if starting_node in trap_nodes:
            if log:
                print("The second player wins at "+str(i+1))
            if not find_all:
                break

        # parent nodes of trap_node_list[i]
        start_time_1 = time()
        parent_nodes = set()
        for node in remaining_nodes:
            # TODO: perhaps make this faster by pre-computing the set of all parent nodes of each node? Perhaps while listing them?
            # Would this consume too much memory though?  Memory Errors seem to be a bigger problem right now
            # parent_nodes are any nodes who have at least one trap child
            # if not non_parent_children[node].isdisjoint(trap_nodes):
            if len(trap_nodes & non_parent_children[node]) != 0:
                parent_nodes.add(node)
                total_parent_count += 1
                del non_parent_children[node]
        # No time (~0.05%)
        remaining_nodes.difference_update(parent_nodes)
        end_time = time()
        tt1 += end_time - start_time_1

        if starting_node in parent_nodes:
            if log:
                print("The first player wins at "+str(i+1))
            if not find_all:
                break

        if log > 1:
            print("Parent " + str(i) + ": " + str(len(parent_nodes)) + " " + str(parent_nodes))
            print("Trap " + str(i + 1) + ": " + str(len(trap_nodes)) + " " + str(trap_nodes))
        i += 1
    end_time = time()
    print()
    print(tt1)  # 0.953
    print(tt2)  # 1.761
    print(end_time - start_time) # 2.713

    if log:
        if log == 1:
            print()
            print("Total Parent: " + str(total_parent_count))
            print("Total Trap: " + str(total_trap_count))
            print("Remaining Nodes: " + str(len(remaining_nodes)))
            print("End Nodes: " + str(len(end_nodes)))
        elif log >= 2:
            print()
            # print("Total Parent: " + str(len(total_parent_nodes)) + " " + str(total_parent_nodes))
            # print("Total Trap: " + str(len(total_trap_nodes)) + " " + str(total_trap_nodes))
            print("Remaining Nodes: " + str(len(remaining_nodes)) + " " + str(remaining_nodes))

def classify_nodes(starting_node, log=0):
    # We control parent -> trap
    # They control trap -> parent
    possible_nodes = set()
    # list_nodes_non_recursive(starting_node, possible_nodes)
    end_nodes = {node for node in possible_nodes if node.winner() is not None}
    total_parent_nodes = set()
    total_trap_nodes = end_nodes.copy()
    prev_trap_nodes = end_nodes.copy()

    if log > 2:
        print("Trap 0: " + str(len(end_nodes)) + " " + str(end_nodes))

    i = 0
    # keep going until we run out of trap nodes to find parents of
    while len(prev_trap_nodes) != 0:
        # parent nodes of trap_nodes[i]
        parent_i_nodes = set()
        for node in possible_nodes:
            # parent_i_nodes are any nodes who have at least one child in trap_nodes[i]
            if len(prev_trap_nodes & linked_list[node]) != 0 and node not in total_parent_nodes:
                parent_i_nodes.add(node)
        total_parent_nodes |= parent_i_nodes

        # Nodes 2i+2-away from win node
        trap_i1_nodes = set()
        for node in possible_nodes:
            if node not in total_trap_nodes:
                # nodes whose children are all parent nodes
                overlap = len(total_parent_nodes & linked_list[node])
                if overlap == len(linked_list[node]) and overlap != 0:
                    trap_i1_nodes.add(node)
        total_trap_nodes |= trap_i1_nodes
        prev_trap_nodes = trap_i1_nodes.copy()

        if log > 2:
            print("Parent " + str(i) + ": " + str(len(parent_i_nodes)) + " " + str(parent_i_nodes))
            print("Trap " + str(i + 1) + ": " + str(len(trap_i1_nodes)) + " " + str(trap_i1_nodes))
        if starting_node in total_parent_nodes:
            if log:
                print("The first player wins at "+str(i))
        if starting_node in total_trap_nodes:
            if log:
                print("The second player wins at "+str(i))
        i += 1

    unclassified_nodes = possible_nodes - (total_parent_nodes | total_trap_nodes)
    if log:
        if log == 1:
            print()
            print("Total Parent: " + str(len(total_parent_nodes)))
            print("Total Trap: " + str(len(total_trap_nodes)))
            print("Remaining Nodes: " + str(len(unclassified_nodes)))
        elif log == 2:
            print()
            print("Total Parent: " + str(len(total_parent_nodes)) + " " + str(total_parent_nodes))
            print("Total Trap: " + str(len(total_trap_nodes)) + " " + str(total_trap_nodes))
            print("Remaining Nodes: " + str(len(unclassified_nodes)) + " " + str(unclassified_nodes))
        elif log > 2:
            overlap = total_parent_nodes & total_trap_nodes
            print("Parent/Trap Overlap: " + str(len(overlap)) + " " + str(overlap))

    return total_trap_nodes, total_parent_nodes, unclassified_nodes

# trap_nodes, parent_nodes, unclassified = classify_nodes(start_node, log=1)

# find_trap_nodes(start_node, log=1)

list_nodes_and_sort(start_node)

# print()
# node_children_classification = {}
# for unknown_node in unclassified:
#     node_children_classification[unknown_node] = {}
#     for un_child in linked_list[unknown_node]:
#         if un_child in unclassified:
#             node_children_classification[unknown_node][un_child] = "Unclassified"
#         if un_child in parent_nodes:
#             node_children_classification[unknown_node][un_child] = "Parent"
#         if un_child in trap_nodes:
#             node_children_classification[unknown_node][un_child] = "Trap"
#     print(repr(unknown_node)+": "+str(node_children_classification[unknown_node]))


""" Impossible States (w/o Stalling)(Turn: 0):
(0, 0), (0, 0)
(1, 0), (0, 0)
(1, 1), (0, 0)
(1, 1), (4, 3)
(1, 1), (4, 4)
(2, 0), (0, 0)
(2, 1), (0, 0)
(2, 1), (4, 3)
(2, 1), (4, 4)
(2, 2), (0, 0)
(2, 2), (4, 3)
(2, 2), (4, 4)
(3, 0), (0, 0)
(3, 1), (0, 0)
(3, 1), (4, 3)
(3, 1), (4, 4)
(3, 2), (0, 0)
(3, 2), (4, 3)
(3, 2), (4, 4)
(3, 3), (0, 0)
(3, 3), (4, 3)
(3, 3), (4, 4)
(4, 0), (0, 0)
(4, 1), (0, 0)
(4, 1), (4, 4)
(4, 2), (0, 0)
(4, 2), (4, 4)
(4, 3), (0, 0)
(4, 3), (4, 0)
(4, 3), (4, 4)
(4, 4), (0, 0)
(4, 4), (4, 0)
(4, 4), (4, 4)
"""
""" Impossible States (w/ Stalling)(Turn: 0):
(0, 0), (0, 0)
(1, 0), (0, 0)
(1, 1), (0, 0)
(1, 1), (4, 3)
(1, 1), (4, 4)
(2, 0), (0, 0)
(2, 1), (0, 0)
(2, 1), (4, 3)
(2, 1), (4, 4)
(2, 2), (0, 0)
(2, 2), (4, 3)
(2, 2), (4, 4)
(3, 0), (0, 0)
(3, 1), (0, 0)
(3, 1), (4, 3)
(3, 1), (4, 4)
(3, 2), (0, 0)
(3, 2), (4, 3)
(3, 2), (4, 4)
(3, 3), (0, 0)
(3, 3), (4, 3)
(3, 3), (4, 4)
(4, 0), (0, 0)
(4, 1), (0, 0)
(4, 1), (4, 4)
(4, 2), (0, 0)
(4, 2), (4, 4)
(4, 3), (0, 0)
(4, 3), (4, 4)
(4, 4), (0, 0)
(4, 4), (4, 4)
"""
""" States added by stalling (Turn: 0):
(4, 3), (4, 0)
(4, 4), (4, 0)
"""
