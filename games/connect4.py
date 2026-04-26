#new added 
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg
import numpy as np
from sys import exit
#new added
import sys

player1 = sys.argv[1]
player2 = sys.argv[2]

# pygame
pg.init()
clock = pg.time.Clock()
space = 700
screen_height = space
screen_width = space
screen = pg.display.set_mode((screen_width, screen_height))

# general
dim = 7
len = 4
ptr = int(dim / 2)
board = np.full((dim, dim), -1)
height = np.zeros(dim)
turn = 1
winner = -1
game_active = True
thickness = 17
box_len = space / (dim + 2)
disk_size = box_len*0.95
pgfont = pg.font.Font("assets/PixelifySans-VariableFont_wght.ttf", int(box_len))
x_surf = pg.image.load("assets/Red_disk.png").convert_alpha()
x_surf = pg.transform.smoothscale(x_surf,(disk_size,disk_size))
x_rect = x_surf.get_rect()
o_surf = pg.image.load("assets/Yellow_disk.png").convert_alpha()
o_surf = pg.transform.smoothscale(o_surf,(disk_size,disk_size))
o_rect = o_surf.get_rect()

# assets
symbol = {0: "Yellow", 1: "Red"}
skeleton = pg.Rect(box_len, box_len, dim * box_len, dim * box_len)


# functions
def toggle_turn():
    global turn
    turn = 1 - turn


def reset():
    board.fill(-1)
    height.fill(0)
    global ptr
    ptr = int(dim / 2)
    global turn
    turn = 1
    global winner
    winner = -1
    global game_active
    game_active = True


def examine(len, x, y, dx, dy) -> int:
    val = board[y][x]
    for i in range(len):
        if board[y + (i * dy)][x + (i * dx)] == val:
            continue
        else:
            return -1
    return int(val)


def check_winner():
    global winner
    for [dx, dy] in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        for x in range(dim):
            for y in range(dim):
                if (
                    0 <= (x + (dx * (len - 1))) < dim
                    and 0 <= (y + (dy * (len - 1))) < dim
                ):
                    if examine(len, x, y, dx, dy) != -1:
                        return examine(len, x, y, dx, dy)

    for i in board:
        for j in i:
            if j == -1:
                return -1

    return 2


# game loop
while True:
    # screen
    screen.fill("#1d1a30")
    pg.draw.rect(screen, "white", skeleton, 1)
    for x in range(dim - 1):
        pg.draw.line(
            screen,
            "White",
            (box_len * (2 + x), box_len),
            (box_len * (2 + x), box_len * (dim + 1)),
            width=1,
        )
    for y in range(dim - 1):
        pg.draw.line(
            screen,
            "White",
            (box_len, box_len * (2 + y)),
            (box_len * (dim + 1), box_len * (2 + y)),
            width=1,
        )

    # Drawing X and O
    for x in range(dim):
        for y in range(dim):
            x_pos = box_len*( x+1 )
            y_pos = box_len*( y+1 )
            if board[(y, x)] == 0:
                o_rect.center = (x_pos + box_len//2, y_pos+ box_len//2)
                screen.blit(o_surf,o_rect)
            if board[(y, x)] == 1:
                x_rect.center = (x_pos+ box_len//2, y_pos+ box_len//2)
                screen.blit(x_surf,x_rect)

    # event loop
    for event in pg.event.get():
        # Quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # Keyboard input
        elif event.type == pg.KEYDOWN:
            # Filling board and checking winner
            if event.key == pg.K_RETURN or event.key == pg.K_e or event.key == pg.K_i:
                if not game_active:
                    reset()
                elif game_active and height[ptr] < dim:
                    board[int(dim - height[ptr] - 1)][ptr] = turn
                    height[ptr] += 1
                    toggle_turn()
                    winner = check_winner()
                    if winner == -1:
                        continue
                    else: #neww added
                        if winner == 0:
                            print(player1)
                        elif winner == 1:
                            print(player2)
                        elif winner == 2:
                            print("DRAW")

                        pg.quit()
                        exit()
                        
            # Quit using q
            elif event.key == pg.K_q:
                pg.quit()
                exit()
            # Reset using r
            elif event.key == pg.K_r:
                reset()
            # Movement Keys
            elif event.key == pg.K_LEFT or event.key == pg.K_a or event.key == pg.K_h:
                ptr = max(0, ptr - 1)
            elif event.key == pg.K_RIGHT or event.key == pg.K_d or event.key == pg.K_l:
                ptr = min(dim - 1, ptr + 1)

    if game_active:
        menu_surf = pgfont.render(f"{symbol[turn]}'s turn", False, f"{symbol[turn]}")
        cursor = pg.Rect(box_len * (ptr + 1), box_len - thickness, box_len, thickness)
        pg.draw.rect(screen, "White", cursor, 0)

    else:
        if winner == 2:
            menu_surf = pgfont.render("TIE", False, "White")
        else:
            menu_surf = pgfont.render(f"{symbol[winner]} won", False, "White")

    menu_rect = menu_surf.get_rect(center=(space / 2, box_len / 2))
    screen.blit(menu_surf, menu_rect)

    # End
    pg.display.update()
    clock.tick(16)
