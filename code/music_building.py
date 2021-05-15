"""File that makes the different melodies, beats, progression, chords, motifs for FoxDot """
# Author: Laurens Van Goethem, UGent

from music_parameter import get_parameters
import numpy as np


# Gets a progression
def get_progression(root, scale, first_chord, length):
    current_state = first_chord
    sequence = ['I']
    prog = ["I", "ii", "iii", "IV", "V", "vi", "vii"]
    for i in range(length):
        if current_state == "I":
            p = [0, 0.1, 0.1, 0.4, 0.2, 0.1, 0.1]
        if current_state == "ii":
            p = [0.05, 0, 0.05, 0.15, 0.4, 0.05, 0.3]
        if current_state == "iii":
            p = [0.1, 0.1, 0, 0.1, 0.1, 0.5, 0.1]
        if current_state == "IV":
            p = [0.1, 0.2, 0.05, 0, 0.5, 0.05, 0.1]
        if current_state == "V":
            p = [0.7, 0.05, 0.05, 0.05, 0, 0.05, 0.1]
        if current_state == "vi":
            p = [0.05, 0.4, 0.05, 0.4, 0.05, 0, 0.05]
        if current_state == "vii":
            p = [0.05, 0.05, 0.7, 0.05, 0.1, 0.05, 0]
        choice = np.random.choice(prog, p=p)
        sequence.append(choice)
        current_state = choice
    for i in sequence:
        i.replace("\"", "")
    print(sequence)
    return sequence


# Initializes the chord so FoxDot knows which samples/notes to take to form a chord
def init_chords(progression):
    tempo, instruments, root, scale = get_parameters()
    i = transpose(root)
    chords = []
    if scale == "major":
        I = (0 + i, 4 + i, 7 + i)
        ii = (2 + i, 5 + i, 9 + i)
        iii = (4 + i, 7 + i, 11 + i)
        IV = (5 + i, 9 + i, 12 + i)
        V = (7 + i, 11 + i, 14 + i)
        vi = (9 + i, 12 + i, 16 + i)
        vii = (11 + i, 14 + i, 17 + i)
    if scale == "minor_m":
        I = (0 + i, 3 + i, 7 + i)
        I7 = (0 + i, 3 + i, 7 + i, 10 + i)
        ii = (2 + i, 5 + i, 8 + i)
        ii7 = (2 + i, 5 + i, 8 + i, 12 + i)
        iii = (3 + i, 7 + i, 10 + i)
        iii7 = (3 + i, 7 + i, 10 + i, 14 + i)
        IV = (5 + i, 8 + i, 12 + i)
        iv7 = (5 + i, 8 + i, 12 + i, 15 + i)
        V = (7 + i, 10 + i, 14 + i)
        v7 = (7 + i, 10 + i, 14 + i, 17 + i)
        vi = (8 + i, 12 + i, 15 + i)
        vii = (10 + i, 14 + i, 17 + i)
    for chord in progression:
        if chord == "I":
            chords.append(I)
        if chord == "ii":
            chords.append(ii)
        if chord == "iii":
            chords.append(iii)
        if chord == "IV":
            chords.append(IV)
        if chord == "V":
            chords.append(V)
        if chord == "vi":
            chords.append(vi)
        if chord == "vii":
            chords.append(vii)
    return chords


# Transpose to different key
def transpose(root):
    if root == "C":
        i = 0
    if root == "C#":
        i = 1
    if root == "D":
        i = 2
    if root == "D#":
        i = 3
    if root == "E":
        i = 4
    if root == "F":
        i = 5
    if root == "F#":
        i = 6
    if root == "G":
        i = 7
    if root == "G#":
        i = 8
    if root == "A":
        i = 9
    if root == "A#":
        i = 10
    if root == "B":
        i = 11
    return i


# Gets a motif (notes and rhythm) to be used in the melody. This is a single bar.
def get_motif(chord, first_note, first_rhythm):
    tempo, instruments, root, scale = get_parameters()
    i = transpose(root)
    if scale == "major":
        notes = [0 + i, 2 + i, 4 + i, 5 + i, 7 + i, 9 + i, 11 + i, 12 + i, 14 + i, 16 + i, 17 + i, 19 + i, 21 + i]
    if scale == "minor_m":
        notes = [0 + i, 2 + i, 3 + i, 5 + i, 7 + i, 8 + i, 10 + i, 12 + i, 14 + i, 15 + i, 17 + i, 19 + i, 20 + i]
    rhythm = [1 / 4, 1 / 2, 1, 3 / 2, 2]
    current_rhythm = first_rhythm
    bar_rhythm = []
    while sum(bar_rhythm) < 4.0:
        if current_rhythm == 1 / 4:
            p = [0.0, 0.7, 0.15, 0.1, 0.05]
        if current_rhythm == 1 / 2:
            p = [0.05, 0.5, 0.2, 0.1, 0.15]
        if current_rhythm == 1:
            p = [0.05, 0.2, 0.5, 0.1, 0.15]
        if current_rhythm == 3 / 2:
            p = [0.05, 0.1, 0.15, 0.5, 0.2]
        if current_rhythm == 2:
            p = [0.05, 0.1, 0.15, 0.2, 0.5]
        choice = np.random.choice(rhythm, p=p)
        while sum(bar_rhythm) + choice > 4:
            choice = np.random.choice(rhythm, p=p)
        bar_rhythm.append(choice)
    beat = 0
    bar_notes = []
    current_note = first_note
    for j in range(len(bar_rhythm)):
        beat += bar_rhythm[j]
        if beat >= 1:
            chord_notes = [chord[0], chord[1], chord[2]]
            p = [0.34, 0.33, 0.33]
            choice = np.random.choice(chord_notes, p=p)
            beat = 0
        else:
            if current_note == 0 + i:
                p = [0.2, 0.2, 0.2, 0.1, 0.2, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125]
            if current_note == 2 + i:
                p = [0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125]
            if current_note == 3 + i or 4 + i:
                p = [0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125]
            if current_note == 5 + i:
                p = [0.0125, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125]
            if current_note == 7 + i:
                p = [0.0125, 0.0125, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125, 0.0125, 0.0125, 0.0125]
            if current_note == 8 + i or 9 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125, 0.0125, 0.0125]
            if current_note == 10 + i or 11 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125, 0.0125]
            if current_note == 12 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15, 0.0125]
            if current_note == 14 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125, 0.15]
            if current_note == 15 + i or 16 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.15, 0.0125, 0.2, 0.2, 0.2, 0.15, 0.0125]
            if current_note == 17 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.15, 0.0125, 0.2, 0.2, 0.2, 0.15]
            if current_note == 19 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.15, 0.0125, 0.15, 0.0125, 0.2, 0.2, 0.2]
            if current_note == 20 + i or 21 + i:
                p = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.05, 0.0125, 0.2, 0.05, 0.3, 0.3]
            choice = np.random.choice(notes, p=p)
        bar_notes.append(choice)
        current_note = choice
    return bar_notes, bar_rhythm


# Gets multiple bars and forms a phrase for the melody
def get_phrase(chords):
    phrase_notes = []
    phrase_rhythm = []
    for i in range(len(chords)):
        if len(phrase_notes) == 0:
            chord_notes = [chords[i][0], chords[i][1], chords[i][2]]
            p = [0.34, 0.33, 0.33]
            first_note = np.random.choice(chord_notes, p=p)
            p = [0.1, 0.2, 0.3, 0.2, 0.2]
            rhythm = [1 / 4, 1 / 2, 1, 3 / 2, 2]
            first_rhythm = np.random.choice(rhythm, p=p)
        else:
            first_note = phrase_notes[len(phrase_notes) - 1]
            first_rhythm = phrase_rhythm[len(phrase_rhythm) - 1]
        bar_notes, bar_rhythm = get_motif(chords[i], first_note, first_rhythm)
        for j in range(len(bar_rhythm)):
            phrase_notes.append(bar_notes[j])
            phrase_rhythm.append(bar_rhythm[j])
    return phrase_notes, phrase_rhythm


# Gets a motif for the bass
def get_bassmotif(chord):
    bass_notes = []
    bass_rhythm = []
    while sum(bass_rhythm) < 4:
        rhythm = [1 / 4, 1 / 2, 1, 3 / 2, 2]
        p = [0.05, 0.1, 0.2, 0.05, 0.6]
        choice = np.random.choice(rhythm, p=p)
        while sum(bass_rhythm) + choice > 4:
            choice = np.random.choice(rhythm, p=p)
        bass_rhythm.append(choice)
    for j in range(len(bass_rhythm)):
        notes = [chord[0], chord[1], chord[2]]
        p = [0.34, 0.33, 0.33]
        bass_note = np.random.choice(notes, p=p)
        bass_notes.append(bass_note)
    return bass_notes, bass_rhythm


# Creates a bassline for the bass
def get_bassline(chords):
    bassline_notes = []
    bassline_rhythm = []
    for i in range(len(chords)):
        bass_notes, bass_rhythm = get_bassmotif(chords[i])
        for j in range(len(bass_rhythm)):
            bassline_notes.append(bass_notes[j])
            bassline_rhythm.append(bass_rhythm[j])
    return bassline_notes, bassline_rhythm


# Gets a pattern for the beat
def get_beat_pattern():
    beat = []
    beats = ["x", "-", "X", "o", "u", "*", " "]
    p = ["0.16", "0.14", "0.14", "0.14", "0.14", "0.14", "0.14"]
    current_rhythm = np.random.choice(beats, p=p)
    length_beats = [4, 8]
    p = ["0.60", "0.40"]
    length_beat = np.random.choice(length_beats, p=p)
    for i in range(length_beat):
        beat.append(current_rhythm)
        if current_rhythm == "x":
            p = ["0.20", "0.20", "0.10", "0.10", "0.10", "0.10", "0.20"]
        if current_rhythm == "-":
            p = ["0.20", "0.10", "0.20", "0.20", "0.10", "0.10", "0.10"]
        if current_rhythm == "X":
            p = ["0.10", "0.20", "0.20", "0.10", "0.10", "0.10", "0.20"]
        if current_rhythm == "o":
            p = ["0.20", "0.20", "0.10", "0.10", "0.10", "0.10", "0.20"]
        if current_rhythm == "u":
            p = ["0.20", "0.20", "0.10", "0.10", "0.10", "0.10", "0.20"]
        if current_rhythm == "*":
            p = ["0.10", "0.20", "0.10", "0.10", "0.10", "0.20", "0.20"]
        if current_rhythm == " ":
            p = ["0.16", "0.14", "0.14", "0.14", "0.14", "0.14", "0.14"]
        current_rhythm = np.random.choice(beats, p=p)
    return beat


# Makes a pattern for drum
def get_drum_pattern():
    drum = []
    sample = [0, 1, 2, 3, 4, 5]
    p = ["0.10", "0.15", "0.15", "0.20", "0.20", "0.20"]
    current_rhythm = np.random.choice(sample, p=p)
    length_beats = [4, 8]
    p = ["0.60", "0.40"]
    length_beat = np.random.choice(length_beats, p=p)
    for i in range(length_beat):
        drum.append(current_rhythm)
        p = ["0.05", "0.05", "0.225", "0.225", "0.225", "0.225"]
        current_rhythm = np.random.choice(sample, p=p)
    return drum


if __name__ == '__main__':
    # Test
    progression = get_progression("key", "major", "I", 3)
    chords = init_chords(progression)
    get_bassline(chords)
    beat = get_beat_pattern()
