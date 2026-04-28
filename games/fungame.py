import pygame as pg
import numpy as np
import sys
import random

class FunGame:

    def __init__(self, title="Game", space=1000, dim=8, bg_color="#222222"):
        pg.init()
        self.space = space
        self.dim = dim
        self.bg_color = bg_color
        self.screen_width = self.space

        self.screen_height = self.space
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()

        self.box_len = self.space / (self.dim + 2)
        self.disk_size = self.box_len * 0.95
        
        try:
            self.pgfont = pg.font.Font("assets/PixelifySans-VariableFont_wght.ttf", int(self.box_len * 0.8))
        except FileNotFoundError:
            self.pgfont = pg.font.SysFont(None, int(self.box_len * 0.8))

        self.board = np.full((self.dim, self.dim), -1)
        self.skeleton = pg.Rect(self.box_len, self.box_len, self.dim * self.box_len, self.dim * self.box_len)


        self.turn = 1
        self.winner = -1
        self.game_active = True
        self.running = True

        # Mouse & Flashy state
        self.mouse_pos = (0, 0)
        self.particles = []

    def toggle_turn(self):

        self.turn = 1 - self.turn

    def mouse_to_grid(self, mx, my):
        """Converts raw mouse pixel coords to grid indices"""
        col = int((mx - self.box_len) // self.box_len)
        row = int((my - self.box_len) // self.box_len)

        return col, row

    def add_particles(self, x, y, color, count=15):
        """Spawns particles at a pixel location"""
        for _ in range(count):

            self.particles.append({

                'x': x, 'y': y,
                'dx': random.uniform(-4, 4),
                'dy': random.uniform(-4, 4),

                'life': random.uniform(0.5, 1.0),
                'color': color,
                'size': random.randint(3, 8)
            })

    def update_and_draw_particles(self):
        """Updates physics and draws particles"""
        dt = self.clock.get_time() / 1000.0
        for p in self.particles[:]:
            p['x'] += p['dx']

            p['y'] += p['dy']
            p['life'] -= dt * 2
            p['size'] -= dt * 5
            if p['life'] <= 0 or p['size'] <= 0:
                self.particles.remove(p)
            else:
                pg.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), int(p['size']))

    def examine(self, win_len, x, y, dx, dy):
        val = self.board[y][x]
        for i in range(win_len):
            if self.board[y + (i * dy)][x + (i * dx)] == val:
                continue
            else:
                return -1
        return int(val)

    def draw_grid(self):
        self.screen.fill(self.bg_color)
        pg.draw.rect(self.screen, "white", self.skeleton, 1)
        for i in range(self.dim - 1):
            pos = self.box_len * (2 + i)
            pg.draw.line(self.screen, "white", (pos, self.box_len), (pos, self.box_len * (self.dim + 1)), width=1)
            pg.draw.line(self.screen, "white", (self.box_len, pos), (self.box_len * (self.dim + 1), pos), width=1)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_grid()
            self.render_board()
            self.update_and_draw_particles()
            self.draw_ui()
            pg.display.update()
            self.clock.tick(60) # Bumped FPS for smooth particles!
        pg.quit()
        return
    def handle_events(self): pass
    def render_board(self): pass
    def draw_ui(self): pass
