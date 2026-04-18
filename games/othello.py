import pygame as pg
import numpy as np
from sys import exit

"""
A Dictionary with indices from 0-7 and the correpsonding values are the dx and dy for eaach direction
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
# x stands for black and o for white
len = 8
dim = 8
box_len = space / (dim + 2)
disk_size = box_len*0.95
pgfont = pg.font.Font("PixelifySans-VariableFont_wght.ttf", int(box_len))
x_surf = pg.image.load("blackpiece.png").convert_alpha()
x_surf = pg.transform.smoothscale(x_surf,(disk_size,disk_size))
x_rect = x_surf.get_rect()
o_surf = pg.image.load("whitepiece.png").convert_alpha()
o_surf = pg.transform.smoothscale(o_surf,(disk_size,disk_size))
o_rect = o_surf.get_rect()
board = np.full((dim, dim), -1)
board[dim // 2, dim // 2] = 1
board[dim // 2 - 1, dim // 2] = 0
board[dim // 2 - 1, dim // 2 - 1] = 1
board[dim // 2, dim // 2 - 1] = 0
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


def valid_path(x, y, dx, dy):
    # returns 0 if path is not valid
    # else retruns the index of postion relative
    global turn, ptr
    i = 0
    if out_of_bound(x + dx) or out_of_bound(y + dy):
        return 0
    if board[y + dy][x + dx] == turn:
        return 0
    while True:
        x += dx
        y += dy
        i += 1
        if out_of_bound(x) or out_of_bound(y):
            return 0
        elif board[y][x] == -1:
            return 0
        elif board[y][x] == turn:
            return i


def move_array(x, y):
    arr = np.ones(8)
    for i in range(8):
        (dx, dy) = dict[i]
        arr[i] = valid_path(x, y, dx, dy)
    return arr


def valid_move(x, y):
    if board[y][x] == 0 or board[y][x] == 1:
        return False
    if (move_array(x, y) == np.zeros(8)).all():
        return False
    return True


def play_move(x, y):  # finalises a move
    array = move_array(x, y)
    for i in range(8):
        if array[i] == 0:
            pass
        else:
            switch_pieces(x, y, i, array[i])
    return


def switch_pieces(x, y, dr, pos):
    # print("switch activated")
    (dx, dy) = dict[dr]
    for i in range(1, int(pos)):
        board[y + i * dy][x + i * dx] = 1 - board[y + i * dy][x + i * dx]


def check_winner():
    if game_over():
        ocount = np.sum(board == 0)
        xcount = np.sum(board == 1)
        print("x : ", xcount)
        print("o : ", ocount)
        if xcount > ocount:
            return 1
        elif ocount > xcount:
            return 0
        else:
            return 2
    return -1


def game_over() -> bool:
    for x in range(dim):
        for y in range(dim):
            if board[y][x] == -1:
                if (move_array(x, y) != np.full(8, -1)).all():
                    return False
    return True


# game loop
while True:
    # screen
    screen.fill("#006400")
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
                elif game_active and valid_move(ptr[0], ptr[1]):
                    play_move(ptr[0], ptr[1])
                    board[ptr[1]][ptr[0]] = turn
                    toggle_turn()
                    winner = check_winner()
                    # print("ptr :", ptr)
                    # print(board)
                    # print("check_winner: ", check_winner())
                    # print("move_array: ", move_array(ptr[0], ptr[1]))
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
    """
    when do i need to call each function?
    check_winner each timme move is made
    play_movve also each time when a move is made
    """
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
