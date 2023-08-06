#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0603,C0103
""" @author: Samic (samic.org) """


import math
import random
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
event_loop = False
distance, found, rand_x, rand_y, fig, counter = [None] * 6
event_loop, help_box, counter_text, status, ax = [None] * 5

def onclick(event):
    """ runs on each clicks and evaluates the event """
    global distance, found, counter

    if event.xdata is None or event.ydata is None:
        status.set_text('Outside clickable area!')
        fig.canvas.draw()
        return

    if event.xdata < -9.5 and event.ydata > 10.5:
        restart()
        return

    if event.xdata > 10.5 and event.ydata > 10.5:
        help_box.set_visible(not help_box.get_visible())
        fig.canvas.draw()
        return

    if not found:
        help_box.set_visible(False)
        new_distance = math.sqrt(
            (event.xdata-rand_x)**2 + (event.ydata-rand_y)**2)
        if new_distance < 0.5:
            status.set_text('You found me!')
            ax.plot(rand_x, rand_y, color='green', marker='o', markersize=14)
            found = True
        else:
            if new_distance > distance:
                status.set_text('Colder')
                ax.plot(event.xdata, event.ydata, color='blue',
                        marker='o', markersize=12)
            elif new_distance < distance:
                status.set_text('Warmer')
                ax.plot(event.xdata, event.ydata, color='red',
                        marker='o', markersize=12)
            distance = new_distance
        counter += 1
        counter_text.set_text(str(counter))
        fig.canvas.draw()


def restart():
    """ restart the game """
    global fig
    fig.clf()
    main()
    fig.canvas.draw()


def main():
    """ initialization """
    global rand_x, rand_y, distance, fig, ax, status, event_loop
    global found, help_box, counter, counter_text
    rand_x, rand_y = random.randint(-9, 9), random.randint(-9, 9)
    distance = 100
    found = False
    counter = 0

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
    ax.text(-10.9, 10.6, 'Restart?')
    counter_text = ax.text(-10.8, -10.8, '0')
    ax.text(10.6, 10.6, '?')
    help_text = """
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
    help_box = ax.text(-9, 0, help_text)
    help_box.set_visible(False)

    fig.canvas.mpl_connect('button_press_event', onclick)

    if not event_loop:
        event_loop = True
        plt.show()


if __name__ == '__main__':
    main()
