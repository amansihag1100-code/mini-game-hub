import pygame as pg
import numpy as np
from sys import exit

"""
A Dictionary with indices from 0-7 and the correpsonding values are tthe dx and dy for eaach direction
"""
dict = {
    0: (0, 1),
    1: (0, -1),
    2: (1, 0),
    3: (-1, 0),
    4: (1, 1),
    5: (-1, -1),
    6: (1, -1),
    7: (-1, 1),
}

# pygame
pg.init()
clock = pg.time.Clock()
space = 1000
screen_height = space
screen_width = space
screen = pg.display.set_mode((screen_width, screen_height))

# general
len = 8
dim = 8
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
enemy = 1 - turn

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


def out_of_bound(x):
    if x < 0 or x >= 8:
        return True


def valid_path(x, y, dx, dy):  # this checks if a path is valid or not
    """
    I am on an empty square now
    -1 => no valid move
    n =>(x,y) + n times (dx,dy) is the position of the other black piece
    """
    global turn, enemy
    while True:
        x += dx
        y += dy
        if out_of_bound(x) or out_of_bound(y):
            return False
        elif board[y][x] == -1:
            return False
        elif board[y][x] == turn:
            return True


def valid_move(x, y):
    # returns an arrray of dim 8 with the coords of next black and (-1,-1) if no move is valid
    arr = np.empty(8)
    for i in range(8):
        (dx, dy) = dict[i]
        arr[i] = valid_path(x, y, dx, dy)
    return arr


def play_move(x, y, array):  # finalises a move
    for i in range(8):
        if array[i] == -1:
            pass
        else:
            switch_pieces(x, y, i, array[i])


def switch_pieces(
    x, y, dr, pos
):  # x,y which are coords direction and index of final pos
    (dx, dy) = dict[dr]
    for i in range(1, pos - 1):
        board[y + i * dy][x + i * dx] = 1 - board[y + i * dy][x + i * dx]


def check_winner():
    """
    -1 -> continue
    0 -> 0 wins
    1 -> x wins
    2 -> tie

    I need to see if a player can make a move or not
    keep looping on emppty squares on the board while checking for valid move
    whenver i find a non nil array no winner : continue
    if there is no valid move
    count the number of pieces and declare the winner
    """
    if game_over():
        xcount = 0
        ocount = 0
        for i in board:
            if i == 0:
                ocount += 1
            elif i == 1:
                xcount += 1
        if xcount > ocount:
            return 1
        elif ocount > xcount:
            return 0
        else:
            return 2
    else:
        return -1


def game_over() -> bool:
    for x in range(dim):
        for y in range(dim):
            if board[y][x] == -1:
                if (valid_move(x, y) != np.full(8, -1)).all():
                    return False
    return True


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
            if event.key == pg.K_RETURN or event.key == pg.K_e or event.key == pg.K_i:
                if not game_active:
                    reset()
                elif game_active and valid_move:
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
            elif event.key == pg.K_UP or event.key == pg.K_w or event.key == pg.K_k:
                exp[1] -= 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
            elif event.key == pg.K_DOWN or event.key == pg.K_s or event.key == pg.K_j:
                exp[1] += 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
            elif event.key == pg.K_LEFT or event.key == pg.K_a or event.key == pg.K_h:
                exp[0] -= 1
                if check_exp():
                    ptr = exp.copy()
                else:
                    exp = ptr.copy()
            elif event.key == pg.K_RIGHT or event.key == pg.K_d or event.key == pg.K_l:
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
    """
    I need to loop in each direction
    and not looping dimension times but 8 times always as there are 8 possible directions only here
    If it is emmpty then check the folloeing conditions
    there must be a white in nearby square
    If you find an empty square next stop. -> invalid
    If you again find white, keep moving
    If you find black stop
    There are 8 possible directions.
    global enemy, turn
    as soon as validity becomes false I want to return
    for each value of (x,y), I have 8 possible values of validity
    I need to return an array of 8 elements indicating validity in each direction
    For each position I need to check if a path is vlaid or not
    Here I enter a loop where I just need to search for black
    If I get out of bound or find an empty square: game over
    else we found it
    I have chance
    If I find turn from now It is a valid move
    If not invlaid
    If I find any -1 return false
    """
