
from itertools import combinations
from math import floor, log, ceil
from timeit import default_timer as time

# import pygame.gfxdraw
# from pygame import Rect

# TODO: Redo the without stalling chart using the new depth metric
"""
Winner, Max Moves (by the winner)
0 is no forced winner
UC is uncomputable
UCT is uncomputable time (most likely, full time is obviously unknown)
UCM is uncomputable due to lack of memory (i.e. we ran into a memory error while running the program)[1 for listing, 2 for testing]
PP stands for Provable Pattern (i.e. there a simple pattern that I could easily proves holds for all n)
TTn stands for Test To n (i.e. We have tested it up to n and the pattern holds for those)
Without Stalling
Hands -->   1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19    20
Fingers  2  1,1  1,2  1,3  1,4  1,5  1,6  1,7  1,8  1,9  1,10 1,11 PP
|        3  2,1  0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    TT27
v        4  1,2  1,9  0    1,15 1,18 1,22 1,26 1,30 1,33 1,37 1,41 1,44 1,49 1,53 1,57 1    1    1    1    
         5  1,2  2,14 0    0    0    0    0    0    0
         6  2,2  0    0    0    0    0    0    UCM
         7  2,2  0    0    0    0    UCM
         8  2,2  0    0    0    0    
         9  1,3  0    0    0    UCM
         10 1,3  0    0    0
         11 PP   0    0
"""
"""Without stalling, with carry-over
Hands -->   1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19
Fingers  2  1,1  1,3  1,5  1,7  1,7  1,9  1,9  1,11 1,11 1,13 1,13 MPP
|        3  2,2  0,4  0,6  0,6  0,8  0,8  0,8  0,10 0,12 0,12 0,12 0,12 0,14 0,14 0,16 0,16
v        4  2,4  1,9  0,6  1,17 1,21 1,21 1,23 1,23 1,27
         5  1,3  0,8  0,8  0,8  0,10 0,10 0,12
         6
         7
         8
"""
"""
With Stalling (w/ or w/o carry over is very similar [no winner for any of the reasonable non-degenerate cases])
Hands -->   1    2    3    4    5    6    7    8
Fingers  2  1,1  1,2  1,3  1,4  1,5  1,6  1,7  1,8
|        3  2,1  0    0    0    0    0    0    UC
v        4  1,2  0    0    0    UC   UC   UC
         5  1,2  0    0    UC
         6  2,2  0    UC  
         7  2,2  0    UC
         8  2,2  0    UC
         9  1,3  UC
"""
# More hands increases the time of the first part (discovering nodes) faster
# Gives more move options per state
hands = 9
# More fingers increases the time of the second part (sorting the nodes) faster
# Gives more states and deeper graphs
fingers = 4
# Allow moves which do nothing (e.g. Swapping which hand the fingers are on;  (3,0),(4,1) -> (0,3),(4,1) or (2,1),(4,1) -> (1,2),(4,1))
allow_stall = False
# When a hand goes over the finger limit, the finger count on that hand wraps back around
carry_over = False
# TODO: when extending the Node class for more fingers and hands, we made many changes which broke compatibility with the event_loop
# program.  We may want to make this program work again.

def generate_tree(tree, depth, turn, max_depth, env_size):
    if depth == 1:
        return tree
    else:
        next_level = tree.generate_next_level(turn, max_depth-depth-1, allow_stall)
        tree.add(next_level, depth==2, env_size)
        return generate_tree(tree, depth-1, int(not turn), max_depth, env_size)


def generate_circle(all_nodes):
    return {node: node.generate_children() for node in all_nodes}

def get_tt1():
    global tt1
    return tt1
def get_tt2():
    global tt2
    return tt2
def get_tt3():
    global tt3
    return tt3
def get_tt4():
    global tt4
    return tt4
def get_tt5():
    global tt5
    return tt5

tt1 = 0
tt2 = 0
tt3 = 0
tt4 = 0
tt5 = 0

class Node:
    # def __init__(self, state, parent=None, turn=0, level=0):
    #     #State contains the state of the game, namely the number of fingers on each hand
    #     #This in the form [[hand11, hand12],[hand21, hand22]]
    #     # self.state = Node.wrap(state)
    #     self.state = state
    #     # #Who was the parent of this node
    #     # self.parent = parent
    #     #Who will play next
    #     self.turn = turn
    #     # #Is this node a duplicate in the tree (the first node will not be marked as a duplicate, only the subsequent nodes)
    #     # self.is_duplicate = False
    #     # #Is this node a duplicate in this level of the tree?
    #     # self.is_level_duplicate = False
    #     # #The level of the tree this node is on
    #     # self.level = level

    @classmethod
    def wrap_both(cls, state):
        state[0].sort(reverse=True)
        state[1].sort(reverse=True)
        if state[0][0] >= fingers:
            state[0][0] = 0 if not carry_over else state[0][0]%fingers
        if state[1][0] >= fingers:
            state[1][0] = 0 if not carry_over else state[1][0]%fingers
        state[0].sort(reverse=True)
        state[1].sort(reverse=True)
        return tuple(state[0]), tuple(state[1])

    # @classmethod
    # def wrap(cls, state):
    #     state.sort(reverse=True)
    #     if state[0] >= fingers:
    #         state[0] = 0 if not carry_over else state[0]%fingers
    #     state.sort(reverse=True)
    #     return tuple(state)

    @classmethod
    def generate_children(cls, parent_state):
        # if self.is_duplicate:
        #     return set()
        
        # log = False
        
        # Look at all possible move options
        # We have no move options if one player is out of fingers
        # if self.state[0][0] == 0 or self.state[1][0] == 0:
        #     # if log:
        #     #     print("Dead "+repr(self))
        #     return set()

        # states[0] are the states that changed state[0]
        # likewise, states[1] are the states that changed state[1]
        states = set()
        # We might encounter hands that have the same number of fingers, so to reduce the number of options to check
        # we remove duplicates from the attacking hands
        attack_hand_set = {num_fingers for num_fingers in parent_state[0]}
        attack_hand_set.difference_update({0})
        attack_hand_set = list(attack_hand_set)
        attack_hand_set.sort()
        starting_hand_set = {0}
        # Normal Moves
        # hand is the hand which is "attacking"
        for hand in attack_hand_set:
            defend_hand_set = starting_hand_set.copy()
            # j is the hand which is being "attacked"
            for j in range(hands-1, -1, -1):
                if parent_state[1][j] not in defend_hand_set:
                    defend_hand_set.add(parent_state[1][j])
                    mod_state = list(parent_state[1])
                    mod_state[j] += hand
                    if mod_state[j] >= fingers:
                        if not carry_over:
                            mod_state[j] = 0
                            starting_hand_set.add(parent_state[1][j])
                        else:
                            mod_state[j] = mod_state[j]-fingers
                    mod_state.sort(reverse=True)
                    mod_state = tuple(mod_state)
                    if mod_state == dead_state:
                        return {(mod_state, parent_state[0])}, True
                    states.add((mod_state, parent_state[0]))
        # Transferring Fingers/Reviving
        # get all possible two-hand combinations
        done_perms = set()
        for perm in perms:
            fingers_tuple = (parent_state[0][perm[0]], parent_state[0][perm[1]])
            if fingers_tuple not in done_perms:
                done_perms.add(fingers_tuple)
                # I have max=fingers_tuple[0]+fingers_tuple[1] fingers that I distribute over two hands
                # WLOG give the first one i and the second one max-i.  Now i only needs to go up to floor(max/2)
                # Ex 7: 0,7 1,6 2,5 3,4
                # Ex 6: 0,6 1,5 2,4 3,3
                # However, we should exclude the cases of i=fingers_tuple[0] and i=fingers_tuple[1]
                limit = fingers_tuple[0]+fingers_tuple[1]
                for i in range(floor(limit/2)+1):
                    if (i != fingers_tuple[0] and i != fingers_tuple[1]) or allow_stall:
                        mod_state = list(parent_state[0])
                        mod_state[perm[0]] = i
                        mod_state[perm[1]] = limit-i
                        if mod_state[perm[1]] >= fingers:
                            if carry_over:
                                mod_state[perm[1]] = mod_state[perm[1]]-fingers
                            else:
                                mod_state[perm[1]] = 0
                        mod_state.sort(reverse=True)
                        states.add((parent_state[1], tuple(mod_state)))
        # Sort the players' hands, so that the hand with the most fingers appears first
        # Also remove duplicates by placing them in a set
        # ordered_states = {Node.wrap(state, 0) for state in states[0]} | {Node.wrap(state, 1) for state in states[1]}
        # Remove the parent state if it exists
        # Don't allow a move that kills off all our hands
        states.discard((parent_state[1], dead_state))
        # tt1 += 1
        # try:
        #     assert len(ordered_states) == len(states)
        # except AssertionError as e:
        #     print(tt1)
        #     print(len(ordered_states))
        #     print(len(states))
        #     print()
        #     print(sorted(ordered_states))
        #     print(sorted(states))
        #     raise e
        # if log:
        #     print(ordered_states)
        # Remove any state that is the same as its parent state
        # TODO: we changed this because we could not determine the function of the second, if we rediscover it we should
        # WRITE it down, so we don't forget again
        # if not (allow_stall and self.state[not turn][1] == 0):
        # start_time = time()
        # if not allow_stall:
        #     ordered_states = {state for state in ordered_states if state != self.state}
        # end_time = time()
        # tt2 += (end_time - start_time)
        # # We don't allow a move that kills off all our hands
        # start_time = time()
        # unique_states = {state for state in ordered_states if state[not turn][0] != 0}
        # end_time = time()
        # tt3 += (end_time - start_time)
        # if log:
        #     print(unique_states)
        
        # nodes = {Node(state, self, turn, level) for state in unique_states}
        # nodes = {Node(state, turn=turn) for state in ordered_states}
        # if log:
        #     print("State: "+str(self.state))
        # for node in nodes:
        #     if log:
        #         print(node)
        #         print(all_nodes)
        #     if all_nodes is not None and level is not None:
        #         if node in all_nodes[level]:
        #             node.is_level_duplicate = True
        #             node.is_duplicate = True
        #         else:
        #             for node_level in all_nodes:
        #                 if node in node_level:
        #                     node.is_duplicate = True
        #             if not node.is_duplicate:
        #                 all_nodes[level].append(node)
        # if log:
        #     print()
        return states, False

    @classmethod
    def winner(cls, state):
        if state[0][0] == 0:
            return 1
        elif state[1][0] == 0:
            return 0
        else:
            return None
    # def get_color(self):
    #     """Node Color Guide
    #     Black: Normal
    #     Red: Duplicate
    #     Blue: Level Duplicate
    #     Green: End
    #     Yellow: Duplicate End
    #     Light Blue: Level Duplicate End
    #     """
    #     color = (0,0,0)
    #     if self.is_level_duplicate:
    #         color = (0,0,255)
    #         if self.winner() is not None:
    #             color = (0,200,255)
    #     elif self.is_duplicate:
    #         color = (255,0,0)
    #         if self.winner() is not None:
    #             color = (255,200,0)
    #     elif self.winner() is not None:
    #         color = (0,150,0)
    #     return color
    #
    #
    # def __eq__(self, other):
    #     if self.turn == other.turn:
    #         return self.state == other.state
    #     else:
    #         return self.state == other.state[::-1]
    # def __hash__(self):
    #     state = self.state if self.turn == 0 else self.state[::-1]
    #     return hash(state)
    #
    # def __lt__(self, other):
    #     if self.turn == other.turn:
    #         return self.state < other.state
    #     else:
    #         return self.state < other.state[::-1]
    #
    # def __str__(self):
    #     """Nodes are displayed so that the player whose turn it is is listed first"""
    #     if self.turn == 0:
    #         string = ""
    #         for i in range(0, 2):
    #             for j in range(0, hands):
    #                 string += str(self.state[i][j])+","
    #             string = string[:-1]
    #             string += " "
    #         string = string[:-1]
    #         return string
    #     else:
    #         string = ""
    #         for i in range(1, -1, -1):
    #             for j in range(0, hands):
    #                 string += str(self.state[i][j]) + ","
    #             string = string[:-1]
    #             string += " "
    #         string = string[:-1]
    #         return string
    # def __repr__(self):
    #     """Nodes are displayed so that the player whose turn it is is listed first"""
    #     if self.turn == 0:
    #         return "Node("+str(self.state)+")"
    #     else:
    #         return "Node("+str(self.state[::-1])+")"

start_node = Node.wrap_both([[1]*hands, [1]*hands])
perms = tuple(combinations(range(0, hands), 2))
dead_state = (0,)*hands
        
class Tree:
    height = 100
    node_offset = 18
    min_node_space = node_offset*2.5
    def __init__(self, starting_node):
        #This is a multi-dimensional array that stores the nodes of the tree
        #The first dimension is the level of the tree (i.e. how many moves have been played)
        #The second dimension is a dictionary that maps parent nodes to a list of child nodes
        self.levels = [{None: [starting_node]}]
        self.starting_node = starting_node
        self.nodes = [[]]
        self.space = [{None: 1.0}]
        self.largest_level = 0
        self.total_values = []
    
    def generate_node_list(self):    
        all_nodes = []
        for level in self.levels:
            for node_list in level.values():
                all_nodes += node_list
        return all_nodes
    def generate_next_level(self, turn, level, allow_stall=False):
        current_level = self.levels[-1]
        
        self.nodes.append([])
        new_level = {node : node.generate_children(turn, self.nodes, level, allow_stall) for node_list in current_level.values() for node in node_list if not node.is_level_duplicate}
        return new_level
    def add(self, new_level, last_level, env_size):
        self.levels.append(new_level)
        if last_level:
            self.calculate_space(env_size)
    
    def get_num_of_descendants(self, node, node_level, descendant_level, log=False):
        if node_level >= descendant_level or node_level >= len(self.levels):
            return 1 #They are considered their own descendant for this purpose
        elif node.is_level_duplicate:
            return 0
        else:
            descendants = 0
            for child in self.levels[node_level+1][node]:
                descendants += self.get_num_of_descendants(child, node_level+1, descendant_level, log)
            return descendants
        
    def calculate_space(self, env_size):
        nodes_in_levels = [sum([len(node_list) for node_list in level.values()]) for level in self.levels]
        max_nodes = max(nodes_in_levels)
        print(nodes_in_levels)
        #The index of the level where the most number of nodes are children (since the last level of nodes are never parents)
        largest_level = nodes_in_levels.index(max_nodes)
        self.largest_level = largest_level
        
        for level in range(0, len(self.levels)):
            level_dict = {}
            total_value = 0
            for children in self.levels[level].values():
                for child in children:
                    descendants = self.get_num_of_descendants(child, level, self.largest_level)
                    if not child.is_level_duplicate:
                        space = max(descendants/max_nodes, self.min_node_space/env_size[0])
                        level_dict[child] = space
                    elif level == self.largest_level:
                        space = descendants/max_nodes
                    else:
                        space = self.min_node_space/env_size[0]
                    total_value += space
            
            for key, value in level_dict.items():
                level_dict[key] = value/total_value
            self.space.append(level_dict)
            self.total_values.append(total_value)
    
    def draw(self, screen, font, env_size, scale=1):
        for level in range(1, self.largest_level+1):
            total_percent_used = 0
            total_parent_percent_used = 0
            for potential_parents in self.levels[level-1].values():
                for potential_parent in potential_parents:
                    if potential_parent.is_duplicate:
                        total_parent_percent_used += self.min_node_space/env_size[0]*scale/self.total_values[level-1]
                        continue
                    else:
                        parent = potential_parent
                    parent_percent = self.space[level][parent]
                    parent_x = (total_parent_percent_used+parent_percent/2)*env_size[0]
                    for child in self.levels[level][parent]:
                        
                        color = child.get_color()
                        text = font.render(str(child), True, color)
                        
                        
                        if not child.is_level_duplicate or level == self.largest_level:
                            percent_of_level = self.space[level+1][child]
                        else:
                            percent_of_level = self.min_node_space/env_size[0]*scale/self.total_values[level]
                        
                        x = (total_percent_used+percent_of_level/2)*env_size[0]
                        # screen.blit(text, Rect(x-self.node_offset*scale, level*self.height*scale, 0, 0))
                        
                        # if level != 0:
                        #     pygame.gfxdraw.line(screen, int(parent_x), int((level-1)*self.height*scale+15*scale), int(x), int(level*self.height*scale), (0,0,0))
                        
                        total_percent_used += percent_of_level
                    total_parent_percent_used += parent_percent
            
            
        total_parent_percent_used = 0
        if self.largest_level < len(self.levels)-1:
            for parent_parent in self.levels[self.largest_level].keys():
                for child_parent in self.levels[self.largest_level][parent_parent]:
                    child_parent_percent = self.space[self.largest_level+1][child_parent]
                    if not child_parent.is_duplicate:
                        parent_x = int((total_parent_percent_used+child_parent_percent/2)*env_size[0])
                        parent_width = int(parent_percent*env_size[0])
                        self.draw_children(screen, font, scale, child_parent, self.largest_level+1, parent_x, parent_width)
                    total_parent_percent_used += child_parent_percent
    
    def draw_children(self, screen, font, scale, parent, level, parent_x, parent_width):
        if level == len(self.levels):
            return
        try:
            children = self.levels[level][parent]
        except KeyError as e:
            print(e)
            print(level)
            print(parent)
            raise e
        
        start = parent_x-parent_width/2
        partitions = len(children)
        
        for i in range(0, len(children)):
            color = children[i].get_color()
            text = font.render(str(children[i]), True, color)
            child_x = int(start+parent_width/partitions*(i+0.5))
            # screen.blit(text, Rect(child_x-self.node_offset*scale, level*self.height*scale, 0,0))
            
            # pygame.gfxdraw.line(screen, parent_x, int((level-1)*self.height*scale+15*scale), child_x, int(level*self.height*scale), (0,0,0))
            
            child_width = parent_width/len(children)
            self.draw_children(screen, font, scale, children[i], level+1, child_x, child_width)
            
    def __str__(self):
        string = ""
        for level in self.levels:
            string += "{\n"
            for parent, children in level.items():
                if parent is None:
                    string += str(parent)+": "
                else:
                    string += str(parent.state)+": "
                for child in children:
                    string += str(child.state)+", "
                string += "\n"
            string += "}\n\n"
        return string
                    




    
