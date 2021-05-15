"""File that contains the initial parameters and makes changes to them to change the way the music is created."""
# Author: Laurens Van Goethem, UGent

import csv
global row


# Changes the chosen csv line
def set_csv_line(number):
    global row
    with open("supercollider_info.csv", "r") as file:
        r = csv.reader(file)
        header = next(r)
        for i in range(number):
            next(r)
        row = next(r)
        print(row)


# Returns the csv line currently played
def get_csv_line():
    global row
    return row


# Init parameters that will be used throughout the music. You can change the parameters here.
def get_parameters():
    global row
    tempo = int(row[2])
    root = row[3]
    if row[4] == '0':
        scale = "major"
    else:
        scale = "minor_m"
    instruments = []
    if row[5] == '1':
        instruments.append("piano_h")
    if row[6] == '1':
        instruments.append("guitar_a")
    if row[7] == '1':
        instruments.append("guitar_j")
    if row[8] == '1':
        instruments.append("keys")
    if row[9] == '1':
        instruments.append("bass_j")
    if row[10] == '1':
        instruments.append("bass_t")
    if row[11] == '1':
        instruments.append("piano_l")
    if row[12] == '1':
        instruments.append("strings")
    if row[13] == '1':
        instruments.append("beat")
    if row[14] == '1':
        instruments.append("drum")
    return tempo, instruments, root, scale
