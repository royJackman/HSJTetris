from operator import itemgetter
from Tetrimino import DEFAULTS, Tetrimino
import numpy as np
import random
import sys
import time

np.set_printoptions(threshold=sys.maxsize)
start_location = [4, 5]

class Board:
    def __init__(self):
        self.grid = np.zeros((24, 10))
        self.coral = []
        self.rowsums = np.zeros((24,))
        self.tetrimino = None
        self.focus = None
        self.epoch = None
        self.timer = None
        self.registry = [(0.95, 0.95, 0.95)]
        self.score = 0
        self.round = 0
    
    def __str__(self):
        return str(self.grid)
    
    def controls(self, inp, shift=False, control=False):
        delta = 2 if shift else 1
        if control:
            if inp == 'w':
                self.jump(np.array([-1, 0]))
            elif inp == 'a':
                self.jump(np.array([0,-1]))
            elif inp == 's':
                self.jump(np.array([1, 0]))
            elif inp == 'd':
                self.jump(np.array([0,1]))
        elif inp == 'a':
            if not self.stop_check(rng=delta, direction=np.array([0,-1])):
                self.move_tetrimino(np.array([0, -delta]))
        elif inp == 'd':
            if not self.stop_check(rng=delta, direction=np.array([0,1])):
                self.move_tetrimino(np.array([0, delta]))
        elif inp == 'e':
            rotated = self.tetrimino.rotate(clockwise=True)
            if shift: rotated = Tetrimino(rotated).rotate(clockwise=True)
            if len(list(filter(lambda x: x[1] + self.focus[1] in [-1, 10], rotated))) == 0:
                self.draw_tetrimino(clean=True)
                self.tetrimino.squares = rotated
                self.draw_tetrimino()
        elif inp == 'q':
            rotated = self.tetrimino.rotate(clockwise=False)
            if shift: rotated = Tetrimino(rotated).rotate(clockwise=False)
            if len(list(filter(lambda x: x[1] + self.focus[1] in [-1, 10], rotated))) == 0:
                self.draw_tetrimino(clean=True)
                self.tetrimino.squares = rotated
                self.draw_tetrimino()
        elif inp == 's':
            self.jump(np.array([1,0]))

    def delete_row(self, row):
        self.grid[row, :] = np.zeros((10,))
        self.coral = list(filter(lambda x: x[0] != row, self.coral))
        for i in sorted(list(filter(lambda x: x[0] < row, self.coral)), key=itemgetter(0), reverse=True):
            self.coral.remove(i)
            self.coral.append([i[0] + 1, i[1]])
        self.grid = np.insert(np.delete(self.grid, row, 0), 0, 0, axis=0)
        self.rowsums = np.insert(np.delete(self.rowsums, row, 0), 0, 0, axis=0)

    def draw_tetrimino(self, clean=False):
        if self.tetrimino is None: return
        val = 0 if clean else self.registry.index(self.tetrimino.color)
        for i in self.tetrimino.squares:
            x, y = self.focus + np.array(i)
            self.grid[x, y] = val

    def game_over_check(self):
        return len(list(filter(lambda x: x[0] < 4, self.coral))) > 0

    def gravity(self):
        self.move_tetrimino(np.array([1, 0]))
    
    def jump(self, vector):
        i = 0
        while not self.stop_check(rng=i+1, direction=vector):
            i += 1
        self.move_tetrimino(i * vector)

    def move_tetrimino(self, vector):
        self.draw_tetrimino(clean=True)
        self.focus += vector
        self.draw_tetrimino()

    def row_check(self):
        idx = np.where(self.rowsums == 10)
        lines = len(idx[0])
        if lines > 0:
            self.score += [40, 100, 300, 1200][lines - 1] * (self.round + 1)
            offset = 0
            for i in range(lines):
                self.delete_row(idx[0][-i - 1] + offset)
                offset += 1

    def set_tetrimino(self, t, refocus=True):
        if not t.color in self.registry:
            self.registry.append(t.color)
        if refocus:
            self.focus = np.array([2, 4])
        self.tetrimino = t
        self.draw_tetrimino()
        self.timer = time.time()
    
    def solidify_tetrimino(self):
        for i in self.tetrimino.squares:
            x, y = self.focus + np.array(i)
            self.coral.append([x, y])
            self.rowsums[x] += 1
        self.tetrimino = None

    def start_round(self):
        self.epoch = self.timer = time.time()
        self.set_tetrimino(random.choice(DEFAULTS)())
    
    def stop_check(self, rng=1, direction=np.array([1,0])):
        for i in self.tetrimino.squares:
            x, y = self.focus + np.array(i) + rng * direction
            if x < 0 or x > 23 or y < 0 or y > 9 or [x, y] in self.coral:
                return True
        return False

    def tick(self):
        stop = self.stop_check()
        if stop:
            self.solidify_tetrimino()
            if self.game_over_check(): sys.exit(f'Game Over!\n\nFinal Score: {self.score}')
            self.row_check()
            r = random.choice(DEFAULTS)
            self.set_tetrimino(r())
        else:
            self.gravity()

    def time(self): return time.time() - self.timer

    def round_time(self): return time.time() - self.epoch