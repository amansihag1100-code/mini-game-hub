import pygame as pg
import numpy as np
from sys import exit

# pygame
pg.init()
clock = pg.time.Clock()
space = 1000
screen_height = space
screen_width = space
screen = pg.display.set_mode((screen_width, screen_height))

# general
len = 3
dim = 3
box_len = space / (dim + 2)
pgfont = pg.font.Font(None, int(box_len))
x_surf = pgfont.render("X", False, "Lime")
x_rect = x_surf.get_rect
o_surf = pgfont.render("O", False, "Pink")
board = np.full((dim, dim), -1)
ptr = [int(dim / 2), int(dim / 2)]
exp = ptr.copy()
turn = 1
winner = -1
game_active = True

# assets
symbol = {0: "O", 1: "X", 2: "Tie"}
skeleton = pg.Rect(box_len, box_len, dim * box_len, dim * box_len)
cursor = pg.Rect(
    1.1 * box_len + ptr[0] * box_len,
    1.1 * box_len + ptr[1] * box_len,
    0.8 * box_len,
    0.8 * box_len,
)


# functions
def swap_ptr(ptr):
    return (ptr[1], ptr[0])


def toggle_turn():
    global turn
    turn = 1 - turn


def reset():
    board.fill(-1)
    global ptr
    ptr = [int(dim / 2), int(dim / 2)]
    global exp
    exp = ptr.copy()
    global turn
    turn = 1
    global winner
    winner = -1
    global game_active
    game_active = True


def check_exp():
    global exp
    return not (exp[0] < 0 or exp[0] >= dim or exp[1] < 0 or exp[1] >= dim)


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
    screen.fill("black")
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
            if board[(y, x)] == 0:
                screen.blit(o_surf, (box_len * (1.27 + x), box_len * (1.2 + y)))
            if board[(y, x)] == 1:
                screen.blit(x_surf, (box_len * (1.27 + x), box_len * (1.2 + y)))

    # event loop
    for event in pg.event.get():
        # Quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # Keyboard input
        elif event.type == pg.KEYDOWN:
            # Filling board and checking winner
            if event.key == pg.K_RETURN or event.key == pg.K_e:
                if game_active == False:
                    reset()
                elif game_active == True and board[swap_ptr(ptr)] == -1:
                    board[swap_ptr(ptr)] = turn
                    toggle_turn()
                    winner = check_winner()
                    if winner == -1:
                        pass
                    else:
                        print("winner: ", winner)
                        game_active = False
            # Quit using q
            elif event.key == pg.K_q:
                pg.quit()
                exit()
            # Reset using r
            elif event.key == pg.K_r:
                reset()
            # Movement Keys
            elif event.key == pg.K_UP or event.key == pg.K_w:
                exp[1] -= 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                exp[1] += 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                exp[0] -= 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                exp[0] += 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
        # Moving box
        cursor = pg.Rect(
            1.1 * box_len + ptr[0] * box_len,
            1.1 * box_len + ptr[1] * box_len,
            0.8 * box_len,
            0.8 * box_len,
        )

    if game_active:
        menu_surf = pgfont.render(f"{symbol[turn]}'s turn", False, "White")
        pg.draw.rect(screen, "yellow", cursor, 3)

    else:
        if winner == 2:
            menu_surf = pgfont.render("TIE", False, "Yellow")
        else:
            menu_surf = pgfont.render(f"{symbol[winner]} won", False, "Yellow")

    menu_rect = menu_surf.get_rect(center=(space / 2, box_len / 2))
    screen.blit(menu_surf, menu_rect)

    # End
    pg.display.update()
    clock.tick(16)
