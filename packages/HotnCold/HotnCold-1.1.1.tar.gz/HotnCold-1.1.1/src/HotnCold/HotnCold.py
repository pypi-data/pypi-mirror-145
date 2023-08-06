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
event_loop = False

def onclick(event):
    global distance, fig, text, found, credit
    credit.set_visible(False)

    if event.xdata == None or event.ydata == None:
        status.set_text('Outside clickable area!')
        fig.canvas.draw()
        return

    if event.xdata < -9.5 and event.ydata > 10.5:
        restart()
        return

    if event.xdata > 10.5 and event.ydata > 10.5:
        credit.set_visible(True)
        fig.canvas.draw()
        return

    if not found:
        new_distance = math.sqrt((event.xdata-rand_x)**2 + (event.ydata-rand_y)**2)
        if new_distance < 0.5:
            status.set_text('You found me!')
            ax.plot(rand_x, rand_y, color='green', marker='o', markersize=14)
            found = True
        else:
            if new_distance > distance:
                status.set_text('Colder')
                ax.plot(event.xdata, event.ydata, color='blue', marker='o', markersize=12)
            elif new_distance < distance:
                status.set_text('Warmer')
                ax.plot(event.xdata, event.ydata, color='red', marker='o', markersize=12)
            distance = new_distance
        fig.canvas.draw()


def restart():
    global fig
    fig.clf()
    main()
    fig.canvas.draw()


def main():
    global rand_x, rand_y, distance, fig, ax, status, event_loop, found, credit
    rand_x, rand_y = random.randint(-9, 9), random.randint(-9, 9)
    distance = 100
    found = False

    plt.rcParams['figure.figsize'] = [8, 8]
    plt.rcParams['figure.autolayout'] = False
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(num="Hot'n'Cold Game")
    #ax.axis('off')
    plt.xticks([])
    plt.yticks([])
    ax.plot(range(-10, 11), range(-10, 11), color='white')
    plt.tight_layout()
    plt.autoscale(False)

    status = ax.text(-0.8, -10.9, 'Click!')
    restart = ax.text(-10.9, 10.6, 'Restart?')
    help = ax.text(10.6, 10.6, '?')
    credit_text = """
Hot'n'Cold is a simple "Hot and Cold" game.\n
A green goal point is hidden and you need to find it by clicking on it.
You'll get hints based on your distance to the goal.
In comparison to your last selected point,
if you're getting closer to the goal, the point you clicked on will be red (getting warmer),
if you're getting away from the goal, the point you clicked on will be blue (getting colder).
The game is finished when you find the green goal point.
You can restart the game at any time by clicking on the "Restart?" button.
\nMade by Samic (samic.org) on April 2, 2022.
    """
    credit = ax.text(-9, 0, credit_text)
    credit.set_visible(False)

    connection = fig.canvas.mpl_connect('button_press_event', onclick)

    if not event_loop:
        event_loop = True
        plt.show()


if __name__ == '__main__':
    main()
