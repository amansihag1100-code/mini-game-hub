import pygame as pg
import numpy as np
from fungame import FunGame

class Connect4(FunGame):

    def __init__(self):
        super().__init__("Connect 4", space=1000, dim=7, bg_color="#1d1a30")
        self.win_len = 4
        self.ptr = int(self.dim / 2)
        self.height = np.zeros(self.dim)
        self.thickness = 17
        
        try:
            self.x_surf = pg.transform.smoothscale(pg.image.load("assets/Red_disk.png").convert_alpha(), (self.disk_size, self.disk_size))
            self.o_surf = pg.transform.smoothscale(pg.image.load("assets/Yellow_disk.png").convert_alpha(), (self.disk_size, self.disk_size))
        except FileNotFoundError:

            self.x_surf = self.pgfont.render("R", False, "Red")
            self.o_surf = self.pgfont.render("Y", False, "Yellow")
            
        self.symbol = {0: "Yellow", 1: "Red"}

    def reset(self):
        self.board.fill(-1)
        self.height.fill(0)
        self.ptr = int(self.dim / 2)
        self.turn = 1
        self.winner = -1
        self.game_active = True

    def check_winner(self):
        for [dx, dy] in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            for x in range(self.dim):
                for y in range(self.dim):
                    if (0 <= (x + (dx * (self.win_len - 1))) < self.dim and 0 <= (y + (dy * (self.win_len - 1))) < self.dim):
                        if self.examine(self.win_len, x, y, dx, dy) != -1:
                            return self.examine(self.win_len, x, y, dx, dy)
        if -1 not in self.board: return 2
        return -1

    def attempt_drop(self, col):
        if self.game_active and 0 <= col < self.dim:
            if self.height[col] < self.dim:
                row = int(self.dim - self.height[col] - 1)
                self.board[row][col] = self.turn
                self.height[col] += 1
                
                # Particles at the drop location
                px = self.box_len * (col + 1) + self.box_len / 2
                py = self.box_len * (row + 1) + self.box_len / 2
                color = "Red" if self.turn == 1 else "Yellow"
                self.add_particles(px, py, color, 40)
                
                self.toggle_turn()
                self.winner = self.check_winner()
                if self.winner != -1:
                    self.game_active = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: self.running = False
            elif event.type == pg.MOUSEMOTION:
                col, _ = self.mouse_to_grid(event.pos[0], event.pos[1])
                if 0 <= col < self.dim: self.ptr = col

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.game_active: self.reset()
                    else: self.attempt_drop(self.ptr)
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_RETURN, pg.K_SPACE]:
                    if not self.game_active: self.reset()
                    else: self.attempt_drop(self.ptr)
                elif event.key == pg.K_q: self.running = False
                elif event.key == pg.K_r: self.reset()
                elif event.key in [pg.K_LEFT, pg.K_a]: self.ptr = max(0, self.ptr - 1)
                elif event.key in [pg.K_RIGHT, pg.K_d]: self.ptr = min(self.dim - 1, self.ptr + 1)

    def render_board(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.board[(y, x)] != -1:
                    surf = self.x_surf if self.board[(y, x)] == 1 else self.o_surf
                    rect = surf.get_rect(center=(self.box_len*(x+1) + self.box_len//2, self.box_len*(y+1) + self.box_len//2))
                    self.screen.blit(surf, rect)

    def draw_ui(self):
        if self.game_active:
            # Highlight column

            col_rect = pg.Rect(self.box_len * (self.ptr + 1), self.box_len, self.box_len, self.dim * self.box_len)
            hover_surf = pg.Surface((col_rect.w, col_rect.h), pg.SRCALPHA)
            hover_surf.fill((255, 255, 255, 20))
            self.screen.blit(hover_surf, col_rect.topleft)


            cursor = pg.Rect(self.box_len * (self.ptr + 1), self.box_len - self.thickness, self.box_len, self.thickness)
            pg.draw.rect(self.screen, "Red" if self.turn == 1 else "Yellow", cursor, 0)
            
            menu_surf = self.pgfont.render(f"{self.symbol[self.turn]}'s turn", False, "White")
        else:
            txt = "TIE" if self.winner == 2 else f"{self.symbol[self.winner]} won!"
            menu_surf = self.pgfont.render(txt, False, "White")

        self.screen.blit(menu_surf, menu_surf.get_rect(center=(self.space / 2, self.box_len / 2)))

if __name__ == "__main__":
    Connect4().run()
