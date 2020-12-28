"""
Created on May 22, 2020

@author: Tavis
"""

import pygame
from pygame import Rect, Surface
from root.nested.chopsticks.tree import generate_tree, Tree, Node
"""
Attempt to analyze the game of chopsticks
Analysis will include:
    Drawing a tree with all the possible states and their relationship to one another
    Determining a winning/not losing strategy
    Determining a strategy that loops the game for ever
    Determining the quickest way to win/lose

Analysis could include:
    Drawing a reverse tree (starting at a certain state and seeing all the possible ways to get to that state)
    Analysis of other starting states (besides the standard [[1,1],[1,1]])
    
    
Next Steps: 
    Additional move options
    Divide the tree into multiple images and only display the two that are needed at a time (if there are too many moves to display)
    Decide how to display the looped relationship between repeated hands and circular moves
    
"""
#initialize pygame
pygame.init()

#Set up and draw the screen and background
env_size = (4000, 1500)
screen_size = (2000, 750)
screen = pygame.display.set_mode(screen_size)
original_background = Surface(env_size)
pygame.draw.rect(original_background, (255,255,255), Rect((0,0), env_size))
screen.blit(original_background, Rect(0,0,0,0))

#Create the font
font = pygame.font.SysFont("Calibri", 11)

#Generate the tree and all of its levels
levels = 10
tree = generate_tree(Tree(Node(((1,1),(1,1)))), levels, turn=0, max_depth=levels, env_size=env_size)

#Draw the tree
tree.draw(original_background, font, env_size)

background_dimensions = Rect((0,0), env_size)
screen.blit(original_background, background_dimensions)

pygame.display.update()
scale = 1
prev_scale = 1
running = True
while running:
    redraw = False
    normalize = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            redraw = True
            if event.key == pygame.K_UP:
                background_dimensions.move_ip(0, 100)
            elif event.key == pygame.K_DOWN:
                background_dimensions.move_ip(0, -100)
            elif event.key == pygame.K_LEFT:
                background_dimensions.move_ip(100, 0)
            elif event.key == pygame.K_RIGHT:
                background_dimensions.move_ip(-100, 0)
            elif event.key == pygame.K_SPACE:
                normalize = True
            else:
                redraw = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            redraw = True
            if event.button == 4:
                scale *= 1.1
            elif event.button == 5:
                scale /= 1.1
            else:
                redraw = False
        
    if redraw:
        if scale < screen_size[0]/env_size[0]:
            scale = screen_size[0]/env_size[0]
        if scale > 16000/env_size[0]:
            scale = 16000/env_size[0]
        size = (int(env_size[0]*scale), int(env_size[1]*scale))
        background = Surface(size)
        pygame.draw.rect(background, (255,255,255), Rect((0,0), size))
        tree.draw(background, pygame.font.SysFont("Calibri", int(11*scale)), size, scale)
        
        mouse_pose = pygame.mouse.get_pos()
        background_mouse_pose = (mouse_pose[0]-background_dimensions.left, mouse_pose[1]-background_dimensions.top)
        current_scale = scale/prev_scale
        background_dimensions.move_ip(int(-background_mouse_pose[0]*(current_scale-1)), int(-background_mouse_pose[1]*(current_scale-1)))
        background_dimensions.size = size
        
        x = background_dimensions.width-2000
        y = background_dimensions.height-750
        background_dimensions.clamp_ip(Rect(-x, -y, 2000+2*x, 750+2*y))
        
        screen.blit(background, background_dimensions)
        pygame.display.update()
        prev_scale = scale
        
pygame.quit()

