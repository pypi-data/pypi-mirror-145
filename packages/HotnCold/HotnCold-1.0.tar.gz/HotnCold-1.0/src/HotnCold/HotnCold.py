#!/usr/bin/env python3
""" @author: Samic (samic.org) """

import os
import sys
import math
import random
import warnings
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = [8, 8]
plt.rcParams['figure.autolayout'] = True
plt.rcParams['toolbar'] = 'None'
rand_x, rand_y = random.randint(-9, 9), random.randint(-9, 9)
distance = 100

def onclick(event):
    global distance
    new_distance = math.sqrt((event.xdata-rand_x)**2 + (event.ydata-rand_y)**2)
    if new_distance < 0.5:
        text.set_text('You found me!')
        ax.plot(rand_x, rand_y, color='green', marker='o', markersize=14)
        fig.canvas.mpl_disconnect(connection)
    else:
        if new_distance > distance:
            text.set_text('Colder')
            ax.plot(event.xdata, event.ydata, color='blue', marker='o', markersize=12)
        elif new_distance < distance:
            text.set_text('Warmer')
            ax.plot(event.xdata, event.ydata, color='red', marker='o', markersize=12)
        distance = new_distance
    fig.canvas.draw()

def restart(event):
    os.execv(__file__, sys.argv)  # file needs to be executable

fig, ax = plt.subplots(num="Hot'n'Cold Game")
ax.axis('off')
ax.plot(range(-10, 11), range(-10, 11), color='white')
text = ax.text(-0.8, -11.2, 'Click!')
connection = fig.canvas.mpl_connect('button_press_event', onclick)
ax_restart = plt.axes([0, 0.98, 0.07, 0.02])
bn_restart = Button(ax_restart, 'Restart')
bn_restart.on_clicked(restart)
plt.show()
