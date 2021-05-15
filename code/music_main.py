"""File that controls the overall working of FoxDot. Start, options select, speed and the showing of the annotation
plot"""
# Author: Laurens Van Goethem, UGent

from FoxDot import *
from music_structure import *
from music_parameter import *
from matplotlib import pyplot as plt
from mir_main import plot_anno_csv, get_anno_csv
from datamodel import graph_real_and_predicted
import csv
import numpy as np
import pandas as pd
global coords


###################################################################################################
# Music instructions


# Starts FoxDot music generations
def start():
    print("First line?")
    y = input()
    set_csv_line(int(y))
    tempo, instruments, root, scale = get_parameters()
    Clock.bpm = tempo
    while True:
        print("Type/select 'options' or 'start'")
        print("options: bpm, speed_up, speed_down, stop, line")
        x = input()
        if x == "bpm":
            print("give different tempo (bpm)")
            y = input()
            Clock.bpm = int(y)
        if x == 'start':
            intro()
        if x == 'stop':
            stop()
        if x == 'speed_up':
            speed_up()
        if x == 'speed_down':
            speed_down()
        if x == 'line':
            print("Give number:")
            y = input()
            set_csv_line(int(y))
        show_plot_predict()
    Go()


# Makes the music speed up
def speed_up():
    print("speed up")
    Clock.bpm = Clock.bpm + 20


# Makes the music speed down
def speed_down():
    print("speed down")
    Clock.bpm = Clock.bpm - 20


# When called prints all available info from specific number in the supercollider database
def get_musical_info(number):
    info = get_csv_line('supercollider_info.csv', number)
    data = get_csv_line('features_data/data_mapped_supercollider.csv', number)
    anno = get_csv_line('features_data/anno_mapped_supercollider.csv', number)
    print("Number:")
    print(number)
    print("Info:")
    print(info)
    print("Data:")
    print(data)
    print("Annotation:")
    print(anno)


# returns a specific line from a csv file
def get_csv_line(filename, number):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for i in range(number):
            next(reader)
        row = next(reader)
    return row


###################################################################################################
# Showing the plot


# Shows the annotations plot to click on and choose emotions
def show_plot_mapped():
    global coords, fig, pts
    mapped_path = "features_data/anno_mapped_supercollider.csv"
    fig = plot_anno_csv(mapped_path)
    valence, arousal = get_anno_csv(mapped_path)
    pts = []
    for i in range(len(valence)):
        pts.append([valence[i], arousal[i]])
    coords = []
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()


# Shows the annotations plot to click on and choose emotions
def show_plot_predict():
    global coords, fig, pts
    anno_path = "model_data/anno_pred_supercollider.csv"
    df = pd.read_csv(anno_path)
    valence = df['valence']
    arousal = df['arousal']
    fig = graph_real_and_predicted([0], valence, arousal)
    pts = []
    for i in range(len(valence)):
        pts.append([valence[i], arousal[i]])
    coords = []
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()


# Function to perform on plot click
def onclick(event):
    print("---------------")
    global ix, iy
    ix, iy = event.xdata, event.ydata
    global coords, fig, pts
    if len(coords) != 0:
        plt.plot(coords[0], coords[1], c='C0', marker='*')
    coords = [ix, iy]
    print(coords)
    coords, index = closest_node(coords, pts)
    print(coords)
    # plt.annotate('', xy=(node[0], node[1]), color='green')
    plt.plot(coords[0], coords[1], 'g*')
    set_csv_line(index)
    plt.show()


# Returns the distance between two points
def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)


# Returns the smallest point found in a radius around clicked point on plot
def closest_node(node, nodes):
    pt = []
    dist = 9999999
    index = 0
    for i in range(len(nodes)):
        if distance(node, nodes[i]) <= dist:
            dist = distance(node, nodes[i])
            pt = nodes[i]
            index = i
    return pt, index


if __name__ == '__main__':
    show_plot_predict()
