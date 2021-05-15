"""Main file. Starting point. Asks input from user and selects what to do."""
# Author: Laurens Van Goethem, UGent

from music_main import start
from mir_main import mir, plot_csv, plot_anno_csv
import pandas as pd


print("Main:")
print("Type what you want to do:")
print("- Get MIR features of a directory: get")
print("- Plot MIR features from deam and SuperCollider: plot")
print("- Play FoxDot music: play")
print("- Convert supercollider data to csv: convert")
x = input()

# Get the MIR features of a directory of audio files.
if x == "get":
    print("Choose directory")
    print("- deam")
    print("- supercollider")
    y = input()
    print("Choose kind")
    print("- mp3")
    print("- aiff")
    z = input()
    mir(dir_name=y, kind=z, sr=44100)

# Plot the MIR features of two directory
elif x == "plot":
    print("Data of the two dataset will be plotted...")
    plot_csv('features_data/data_deam.csv', 'features_data/data_supercollider.csv')
    plot_anno_csv("features_data/anno_deam.csv")
    plot_anno_csv("features_data/anno_mapped_supercollider.csv")

# Play FoxDot music
elif x == "play":
    start()

# Convert an excel file to an csv
elif x == "convert":
    print("Give name of file without format tag")
    y = input()
    print("Choose excel to csv or csv to excel")
    print("- 1: excel to csv")
    print("- 2: csv to excel")
    z = input()
    if int(z) == 1:
        print("converting...")
        data = pd.read_excel(y + ".xlsx")
        data.to_csv(y + ".csv", header=True)
    if int(z) == 2:
        print("converting...")
        data = pd.read_csv(y + ".csv")
        data.to_excel(r'' + y + '.xlsx', header=True)
else:
    print("Wrong input")
