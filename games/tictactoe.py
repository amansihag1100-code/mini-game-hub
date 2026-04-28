import pygame as pg
import numpy as np
from fungame import FunGame

class TicTacToe(FunGame):
    def __init__(self):
        super().__init__("Tic Tac Toe", space=1000, dim=10, bg_color="#222222")
        self.win_len = 5
        self.ptr = [int(self.dim / 2), int(self.dim / 2)]

        self.x_surf = self.pgfont.render("X", False, "Lime")
        self.o_surf = self.pgfont.render("O", False, "Pink")
        self.symbol = {0: "O", 1: "X", 2: "Tie"}

    def reset(self):
        self.board.fill(-1)
        self.ptr = [int(self.dim / 2), int(self.dim / 2)]
        self.turn = 1
        self.winner = -1
        self.game_active = True


    def attempt_move(self, col, row):
        if self.game_active and 0 <= col < self.dim and 0 <= row < self.dim:
            if self.board[row][col] == -1:
                self.board[row][col] = self.turn
                
                # Flashy Particles!
                px = self.box_len * (col + 1) + self.box_len / 2
                py = self.box_len * (row + 1) + self.box_len / 2
                color = "Lime" if self.turn == 1 else "Pink"
                self.add_particles(px, py, color, 30)

                self.toggle_turn()
                self.winner = self.check_winner()
                if self.winner != -1:
                    self.game_active = False

    def check_winner(self):
        for [dx, dy] in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            for x in range(self.dim):
                for y in range(self.dim):
                    if (0 <= (x + (dx * (self.win_len - 1))) < self.dim and 
                        0 <= (y + (dy * (self.win_len - 1))) < self.dim):
                        if self.examine(self.win_len, x, y, dx, dy) != -1:
                            return self.examine(self.win_len, x, y, dx, dy)
        if -1 not in self.board: return 2
        return -1


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEMOTION:
                self.mouse_pos = event.pos
                col, row = self.mouse_to_grid(event.pos[0], event.pos[1])
                if 0 <= col < self.dim and 0 <= row < self.dim:
                    self.ptr = [col, row] # Move cursor to mouse
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    col, row = self.mouse_to_grid(event.pos[0], event.pos[1])
                    if not self.game_active:
                        self.reset()
                    else:
                        self.attempt_move(col, row)
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_RETURN, pg.K_SPACE]:
                    if not self.game_active: self.reset()
                    else: self.attempt_move(self.ptr[0], self.ptr[1])
                elif event.key == pg.K_q: self.running = False
                elif event.key == pg.K_r: self.reset()
                # Arrow keys
                elif event.key == pg.K_UP: self.ptr[1] = max(0, self.ptr[1] - 1)
                elif event.key == pg.K_DOWN: self.ptr[1] = min(self.dim - 1, self.ptr[1] + 1)

                elif event.key == pg.K_LEFT: self.ptr[0] = max(0, self.ptr[0] - 1)
                elif event.key == pg.K_RIGHT: self.ptr[0] = min(self.dim - 1, self.ptr[0] + 1)

    def render_board(self):
        for x in range(self.dim):
            for y in range(self.dim):
                x_pos = self.box_len * (x + 1)

                y_pos = self.box_len * (y + 1)
                rect = self.o_surf.get_rect(center=(x_pos + self.box_len//2, y_pos + self.box_len//2))
                if self.board[(y, x)] == 0: self.screen.blit(self.o_surf, rect)
                elif self.board[(y, x)] == 1: self.screen.blit(self.x_surf, rect)

    def draw_ui(self):
        cursor = pg.Rect(self.box_len * (self.ptr[0] + 1), self.box_len * (self.ptr[1] + 1), self.box_len, self.box_len)
        
        if self.game_active:
            # Subtle hover effect
            hover_surf = pg.Surface((self.box_len, self.box_len), pg.SRCALPHA)
            hover_surf.fill((255, 255, 255, 50)) # Transparent white
            self.screen.blit(hover_surf, cursor.topleft)
            pg.draw.rect(self.screen, "yellow", cursor, 3)

            
            menu_surf = self.pgfont.render(f"{self.symbol[self.turn]}'s turn", False, "White")
        else:
            txt = "TIE" if self.winner == 2 else f"{self.symbol[self.winner]} won!"
            menu_surf = self.pgfont.render(txt, False, "Yellow")

        menu_rect = menu_surf.get_rect(center=(self.space / 2, self.box_len / 2))
        self.screen.blit(menu_surf, menu_rect)

if __name__ == "__main__":
    TicTacToe().run()
