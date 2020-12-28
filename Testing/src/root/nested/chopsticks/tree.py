"""
Created on May 22, 2020

@author: Tavis
"""
from pygame import Rect
import pygame.gfxdraw

def generate_tree(tree, depth, turn, max_depth, env_size):
    if depth == 1:
        return tree
    else:
        next_level = tree.generate_next_level(turn, max_depth-depth-1)
        tree.add(next_level, depth==2, env_size)
        return generate_tree(tree, depth-1, int(not turn), max_depth, env_size)


def generate_circle(all_nodes, allow_stall=False):
    return {node: node.generate_children(not node.turn, allow_stall=allow_stall) for node in all_nodes}


class Node:
    def __init__(self, state, parent=None, turn=0, level=0):
        #State contains the state of the game, namely the number of fingers on each hand
        #This in the form [[hand11, hand12],[hand21, hand22]]
        self.state = Node.wrap(state)
        #Who was the parent of this node
        self.parent = parent
        #Who will play next
        self.turn = turn
        #Is this node a duplicate in the tree (the first node will not be marked as a duplicate, only the subsequent nodes)
        self.is_duplicate = False
        #Is this node a duplicate in this level of the tree?
        self.is_level_duplicate = False
        #Is this the end of a branch? (i.e. the game is now over)
        self.is_end = self.state[0] == (0,0) or self.state[1] == (0,0)
        #The level of the tree this node is on
        self.level = level
        
    @classmethod
    def wrap(cls, state):
        new_state = [sorted(state[0], reverse=True), sorted(state[1], reverse=True)]
        for i in range(0, 2):
            for j in range(0, 2):
                if new_state[i][j] >= 5:
                    new_state[i][j] = 0
        return tuple(new_state[0]), tuple(new_state[1])
    
    def generate_children(self, turn, all_nodes=None, level=None, allow_stall=False):
        if self.is_duplicate:
            return []
        
        log = False
        
        # Look at all possible move options

        # We have no move options if one player is out of fingers
        if self.state[0][0] == 0 or self.state[1][0] == 0:
            if log:
                print("Dead "+repr(self))
            return []
        states = []
        if not turn:
            # Hand 1's Move
            # Normal Moves
            states.append(((self.state[0][0]+self.state[1][0], self.state[0][1]), self.state[1]))
            states.append(((self.state[0][0]+self.state[1][1], self.state[0][1]), self.state[1]))
            if self.state[0][1] != 0:
                # Normal Moves
                states.append(((self.state[0][0], self.state[0][1]+self.state[1][0]), self.state[1]))
                states.append(((self.state[0][0], self.state[0][1]+self.state[1][1]), self.state[1]))
            # Transferring Fingers/Reviving
            for i in range(1, self.state[1][0] + 1):
                states.append((self.state[0], (self.state[1][0] - i, self.state[1][1] + i)))
        else:
            # Hand 0's Move
            # Normal Moves
            states.append((self.state[0], (self.state[1][0] + self.state[0][0], self.state[1][1])))
            states.append((self.state[0], (self.state[1][0] + self.state[0][1], self.state[1][1])))
            if self.state[1][1] != 0:
                # Normal Moves
                states.append((self.state[0], (self.state[1][0], self.state[1][1]+self.state[0][0])))
                states.append((self.state[0], (self.state[1][0], self.state[1][1]+self.state[0][1])))
            # Transferring Fingers/Reviving
            for i in range(1, self.state[0][0] + 1):
                states.append(((self.state[0][0] - i, self.state[0][1] + i), self.state[1]))
        #Sort the players' hands, so that the hand with the most fingers appears first
        ordered_states = [Node.wrap(state) for state in states]
        if log:
            print(ordered_states)
        #Remove any state that is the same as its parent state
        if not allow_stall or self.state[not turn][1] != 0:
            ordered_states = [state for state in ordered_states if state != self.state]
        if log:
            print(ordered_states)
        #Remove duplicates
        unique_states = tuple(set(ordered_states))
        if log:
            print(unique_states)
        
        nodes = [Node(state, self, turn, level) for state in unique_states]
        
        if log:
            print("State: "+str(self.state))
        for node in nodes:
            if log:
                print(node)
                print(all_nodes)
            if all_nodes is not None and level is not None:
                if node in all_nodes[level]:
                    node.is_level_duplicate = True
                    node.is_duplicate = True
                else:
                    for node_level in all_nodes:
                        if node in node_level:
                            node.is_duplicate = True
                    if not node.is_duplicate:
                        all_nodes[level].append(node)
        if log:
            print()
        
        return nodes
    
    def get_color(self):
        """Node Color Guide
        Black: Normal
        Red: Duplicate
        Blue: Level Duplicate
        Green: End
        Yellow: Duplicate End
        Light Blue: Level Duplicate End 
        """
        color = (0,0,0)
        if self.is_level_duplicate:
            color = (0,0,255)
            if self.is_end:
                color = (0,200,255)
        elif self.is_duplicate:
            color = (255,0,0)
            if self.is_end:
                color = (255,200,0)
        elif self.is_end:
            color = (0,150,0)
        return color

    def winner(self):
        if self.state[0][0] == 0:
            return 1
        elif self.state[1][0] == 0:
            return 0
        else:
            return None
    
    def __eq__(self, other):
        if self.turn == other.turn:
            return self.state == other.state
        else:
            return self.state == tuple(reversed(other.state))
    def __hash__(self):
        state = self.state if self.turn == 0 else tuple(reversed(self.state))
        return hash(state)

    def __lt__(self, other):
        if self.turn == other.turn:
            return self.state < other.state
        else:
            return self.state < tuple(reversed(other.state))
    
    def __str__(self):
        if self.turn == 0:
            return str(self.state[0][0])+","+str(self.state[0][1])+"  "+str(self.state[1][0])+","+str(self.state[1][1])
        else:
            return str(self.state[1][0])+","+str(self.state[1][1])+"  "+str(self.state[0][0])+","+str(self.state[0][1])
    def __repr__(self):
        # TODO: This seems to be having problems?
        if self.turn == 0:
            return "Node("+str(self.state)+")"
        else:
            return "Node("+str(tuple(reversed(self.state)))+")"
        
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
    def generate_next_level(self, turn, level):
        current_level = self.levels[-1]
        
        self.nodes.append([])
        new_level = {node : node.generate_children(turn, self.nodes, level) for node_list in current_level.values() for node in node_list if not node.is_level_duplicate}
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
                        screen.blit(text, Rect(x-self.node_offset*scale, level*self.height*scale, 0, 0))
                        
                        if level != 0:
                            pygame.gfxdraw.line(screen, int(parent_x), int((level-1)*self.height*scale+15*scale), int(x), int(level*self.height*scale), (0,0,0))
                        
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
            screen.blit(text, Rect(child_x-self.node_offset*scale, level*self.height*scale, 0,0))
            
            pygame.gfxdraw.line(screen, parent_x, int((level-1)*self.height*scale+15*scale), child_x, int(level*self.height*scale), (0,0,0))
            
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
                    




    
