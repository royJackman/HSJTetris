import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c

from Board import Board

def controls(event):
    sys.stdout.flush()
    if event.key in 'adeqs':
        board.controls(event.key)
        fig.canvas.draw()

plt.rcParams['figure.figsize'] = (2.7, 8)
plt.rcParams['keymap.save'].remove('s')
plt.rcParams['keymap.quit'].remove('q')

plt.ion()
fig = plt.figure()
plt.gca().invert_yaxis()
plt.axis('off')
ax = fig.add_subplot(111)
ax.set_title('Tetris')

board = Board()
board.start_round()
data = ax.pcolormesh(board.grid, edgecolor='k', linewidth=0.2)
fig.canvas.mpl_connect('key_press_event', controls)

while board.tetrimino is not None:
    board.tick()
    data.set_array(board.grid)
    data.set_clim(vmax=len(board.registry))
    data.set_cmap(c.ListedColormap(board.registry))
    fig.canvas.draw()
    time.sleep(.2)
    fig.canvas.flush_events()