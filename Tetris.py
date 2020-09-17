import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c

from Board import Board

def key_press_handler(event):
    sys.stdout.flush()
    if event.key in 'adeqs':
        board.controls(event.key, shift=False, control=False)
        fig.canvas.draw()
    elif event.key in 'ADSEQ':
        board.controls(event.key.lower(), shift=True, control=False)
        fig.canvas.draw()
    elif 'ctrl+' in event.key and event.key.split('+')[1] in 'wasdWASD':
        board.controls(event.key.lower()[-1], shift=False, control=True)
        fig.canvas.draw()

plt.rcParams['figure.figsize'] = (2.7, 8)
plt.rcParams['keymap.save'].remove('s')
plt.rcParams['keymap.save'].remove('ctrl+s')
plt.rcParams['keymap.quit'].remove('q')
plt.rcParams['keymap.quit'].remove('ctrl+w')

plt.ion()
fig = plt.figure()
plt.gca().invert_yaxis()
plt.axis('off')
ax = fig.add_subplot(111)
ax.set_title('Tetris')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
score_card = ax.text(0.65, 1.1, 'Score: 0', transform=ax.transAxes, verticalalignment='top', bbox=props)

board = Board()
board.start_round()
data = ax.pcolormesh(board.grid, edgecolor='k', linewidth=0.2)
fig.canvas.mpl_connect('key_press_event', key_press_handler)

while board.tetrimino is not None:
    board.tick()
    data.set_array(board.grid)
    data.set_clim(vmax=len(board.registry))
    data.set_cmap(c.ListedColormap(board.registry))
    score_card.set_text(f'Score: {board.score}')
    fig.canvas.draw()
    time.sleep(.2)
    fig.canvas.flush_events()