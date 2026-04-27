import pygame as pg
import numpy as np
from fungame import FunGame

class Othello(FunGame):
    def __init__(self):

        super().__init__("Othello", space=900, dim=8, bg_color="#006400")
        self.dirs = {0: (0, 1), 1: (0, -1), 2: (1, 0), 3: (-1, 0), 4: (1, 1), 5: (-1, -1), 6: (1, -1), 7: (-1, 1)}
        self.ptr = [int(self.dim / 2), int(self.dim / 2)]
        
        try:
            self.x_surf = pg.transform.smoothscale(pg.image.load("assets/blackpiece.png").convert_alpha(), (self.disk_size, self.disk_size))
            self.o_surf = pg.transform.smoothscale(pg.image.load("assets/whitepiece.png").convert_alpha(), (self.disk_size, self.disk_size))
        except FileNotFoundError:

            self.x_surf = self.pgfont.render("B", False, "Black")
            self.o_surf = self.pgfont.render("W", False, "White")

        self.symbol = {0: "White", 1: "Black", 2: "Tie"}
        self.init_board()

    def init_board(self):
        d2 = self.dim // 2
        self.board[d2, d2] = 1
        self.board[d2 - 1, d2] = 0
        self.board[d2 - 1, d2 - 1] = 1
        self.board[d2, d2 - 1] = 0

    def reset(self):
        self.board.fill(-1)
        self.init_board()
        self.ptr = [int(self.dim / 2), int(self.dim / 2)]
        self.turn = 1
        self.winner = -1
        self.game_active = True

    def out_of_bound(self, x):
        return x < 0 or x >= self.dim

    def valid_path(self, x, y, dx, dy):
        i = 0
        if self.out_of_bound(x + dx) or self.out_of_bound(y + dy) or self.board[y + dy][x + dx] == self.turn: return 0
        while True:
            x += dx; y += dy; i += 1
            if self.out_of_bound(x) or self.out_of_bound(y) or self.board[y][x] == -1: return 0
            elif self.board[y][x] == self.turn: return i

    def move_array(self, x, y):
        return np.array([self.valid_path(x, y, dx, dy) for i, (dx, dy) in self.dirs.items()])

    def valid_move(self, x, y):
        if self.board[y][x] in [0, 1]: return False
        return (self.move_array(x, y) != 0).any()

    def play_move(self, col, row):
        if self.game_active and 0 <= col < self.dim and 0 <= row < self.dim and self.valid_move(col, row):
            array = self.move_array(col, row)
            self.board[row][col] = self.turn
            
            # Particles for placement
            color = "Black" if self.turn == 1 else "White"

            self.add_particles(self.box_len*(col+1.5), self.box_len*(row+1.5), color, 20)

            for i in range(8):
                if array[i] != 0:
                    (dx, dy) = self.dirs[i]
                    for step in range(1, int(array[i])):
                        fy, fx = row + step * dy, col + step * dx
                        self.board[fy][fx] = 1 - self.board[fy][fx]
                        # Particles for flipping
                        self.add_particles(self.box_len*(fx+1.5), self.box_len*(fy+1.5), color, 10)
                        
            self.toggle_turn()
            if self.game_over():
                ocount = np.sum(self.board == 0); xcount = np.sum(self.board == 1)
                if xcount > ocount: self.winner = 1
                elif ocount > xcount: self.winner = 0
                else: self.winner = 2
                self.game_active = False

    def game_over(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[y][x] == -1 and (self.move_array(x, y) != 0).any(): return False
        return True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: self.running = False
            elif event.type == pg.MOUSEMOTION:
                col, row = self.mouse_to_grid(event.pos[0], event.pos[1])
                if 0 <= col < self.dim and 0 <= row < self.dim: self.ptr = [col, row]
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.game_active: self.reset()
                    else:
                        col, row = self.mouse_to_grid(event.pos[0], event.pos[1])
                        self.play_move(col, row)
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_RETURN, pg.K_SPACE]:
                    if not self.game_active: self.reset()
                    else: self.play_move(self.ptr[0], self.ptr[1])
                elif event.key == pg.K_q: self.running = False
                elif event.key == pg.K_r: self.reset()
                elif event.key == pg.K_UP: self.ptr[1] = max(0, self.ptr[1] - 1)
                elif event.key == pg.K_DOWN: self.ptr[1] = min(self.dim - 1, self.ptr[1] + 1)
                elif event.key == pg.K_LEFT: self.ptr[0] = max(0, self.ptr[0] - 1)
                elif event.key == pg.K_RIGHT: self.ptr[0] = min(self.dim - 1, self.ptr[0] + 1)

    def render_board(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[(y, x)] != -1:
                    surf = self.x_surf if self.board[(y, x)] == 1 else self.o_surf
                    rect = surf.get_rect(center=(self.box_len*(x+1) + self.box_len//2, self.box_len*(y+1) + self.box_len//2))
                    self.screen.blit(surf, rect)

    def draw_ui(self):
        cursor = pg.Rect(self.box_len * (self.ptr[0] + 1), self.box_len * (self.ptr[1] + 1), self.box_len, self.box_len)

        
        if self.game_active:
            # Show transparent piece of current turn if valid move
            if self.valid_move(self.ptr[0], self.ptr[1]):
                hover_surf = pg.Surface((self.box_len, self.box_len), pg.SRCALPHA)
                hover_surf.fill((255, 255, 255, 50))
                self.screen.blit(hover_surf, cursor.topleft)
                pg.draw.rect(self.screen, "Lime", cursor, 3)
            else:
                pg.draw.rect(self.screen, "Red", cursor, 3) # Invalid move indicator
                

            menu_surf = self.pgfont.render(f"{self.symbol[self.turn]}'s turn", False, "White")
        else:
            txt = "TIE" if self.winner == 2 else f"{self.symbol[self.winner]} won!"
            menu_surf = self.pgfont.render(txt, False, "Yellow")

        self.screen.blit(menu_surf, menu_surf.get_rect(center=(self.space / 2, self.box_len / 2)))

if __name__ == "__main__":
    Othello().run()
