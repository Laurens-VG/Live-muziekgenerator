"""File that contains all the musical structures like verse, chorus, bridge, solo, intro, outro.
File that contains the creation of the band for each structure and lets this band play with FoxDot.
"""
# Author: Laurens Van Goethem, UGent

from music_building import *
from music_parameter import get_parameters, get_csv_line
from FoxDot import *
import numpy as np

# Global variables for the chorus and verse_progression. Chorus keeps the same vars throughout the song
global verse_progression, c_band_melody, c_band_bass, c_band_accomp, c_band_beat, c_band_drum, c_chords, c_phrase_notes
global c_phrase_rhythm, c_bassline_notes, c_bassline_rhythm, c_beat, c_drum, c_length
global line

###################################################################################################
# Structures


# Sets the length that each structure plays
def get_length_structure(structure):
    length = [16, 32, 48, 64]
    if structure == "intro":
        p = [0.8, 0.2, 0, 0]
    if structure == "verse":
        p = [0.2, 0.8, 0, 0]
    if structure == "chorus":
        p = [0.1, 0.9, 0, 0]
    if structure == "bridge":
        p = [0.2, 0.8, 0, 0]
    if structure == "solo":
        p = [0.5, 0.5, 0, 0]
    res = np.random.choice(length, p=p)
    print("structure length is", res)
    return res


# Chooses a next structure to be played after the currently played structure
def get_next_structure(structure):
    global line
    structures = [verse, chorus, bridge, solo, outro]
    if structure == "intro":
        p = [0.5, 0.5, 0, 0, 0]
    if structure == "verse":
        p = [0.3, 0.4, 0.15, 0.15, 0]
    if structure == "chorus":
        p = [0.4, 0.05, 0.35, 0.2, 0]
    if structure == "bridge":
        p = [0.4, 0.4, 0, 0.2, 0]
    if structure == "solo":
        p = [0.3, 0.5, 0.2, 0, 0]
    res = np.random.choice(structures, p=p)
    newline = get_csv_line()
    if newline != line:
        line = newline
        res = intro
    return res


# Sets a random speed for a structure. Needs to be implemented with markov chain
def set_speed(tempo):
    Clock.bpm = tempo


# Starts the music and is the first function to always be called
def intro():
    print("----------intro----------")
    global verse_progression, line
    line = get_csv_line()
    tempo, instruments, root, scale = get_parameters()
    set_speed(tempo)
    length = get_length_structure("intro")
    print("intro progression:")
    progression = get_progression(root, scale, "I", 3)
    print("verse progression:")
    verse_progression = get_progression(root, scale, "I", 3)
    init_chorus()
    print("intro band:")
    int_chosen = get_number_of_instruments("intro")
    print(int_chosen)
    play_band("intro", progression, int_chosen)
    struct = get_next_structure("intro")
    Clock.future(length, struct)


# Plays the verse
def verse():
    print("----------verse----------")
    length = get_length_structure("verse")
    tempo, instruments, root, scale = get_parameters()
    print("verse band:")
    int_chosen = get_number_of_instruments("verse")
    print(int_chosen)
    play_band("verse", verse_progression, int_chosen)
    time.sleep(length / (tempo / 60) - 1)
    struct = get_next_structure("verse")
    Clock.future(1, struct)


# Plays the chorus
def chorus():
    global c_length
    print("----------chorus----------")
    tempo, instruments, root, scale = get_parameters()
    play_chorus()
    time.sleep(c_length / (tempo / 60) - 1)
    struct = get_next_structure("chorus")
    Clock.future(1, struct)


# Plays the bridge
def bridge():
    print("----------bridge----------")
    tempo, instruments, root, scale = get_parameters()
    length = get_length_structure("bridge")
    progression = get_progression(root, scale, "I", 3)
    print("bridge band:")
    int_chosen = get_number_of_instruments("bridge")
    print(int_chosen)
    play_band("bridge", progression, int_chosen)
    time.sleep(length / (tempo / 60) - 1)
    struct = get_next_structure("bridge")
    Clock.future(1, struct)


# Plays the solo
def solo():
    print("----------solo----------")
    tempo, instruments, root, scale = get_parameters()
    length = get_length_structure("solo")
    progression = get_progression(root, scale, "I", 3)
    print("solo band:")
    int_chosen = get_number_of_instruments("solo")
    print(int_chosen)
    play_band("solo", progression, int_chosen)
    time.sleep(length / (tempo / 60) - 1)
    struct = get_next_structure("solo")
    Clock.future(1, struct)


# Plays the outro which is a final chord, which is I
def outro():
    print("----------outro----------")
    stop_band()
    m1 >> play("c", sample=[(0, 2, 4)], dur=4)
    Clock.future(4, stop)


# Stops the band
def stop():
    Clock.clear()
    m1.stop()
    m2.stop()
    m3.stop()
    m4.stop()
    m5.stop()
    b1.stop()
    b2.stop()
    b3.stop()
    c1.stop()
    c2.stop()
    c3.stop()
    c4.stop()
    c5.stop()
    d1.stop()
    d2.stop()


###################################################################################################
# Band actions


# Gets all the possible instruments and puts it in a respective melody, bass, chords or beat
def create_band(structure, number_of_instr):
    tempo, instruments, root, scale = get_parameters()
    instr_melody = ["piano_h", "keys", "guitar_a", "guitar_j", "sax"]
    instr_bass = ["bass_j", "bass_t", "piano_l", "sax"]
    instr_accomp = ["piano_h", "keys", "guitar_a", "guitar_j", "strings"]
    band_melody = []
    band_bass = []
    band_accomp = []
    band_beat = False
    band_drum = False
    instruments = random.sample(instruments, k=number_of_instr)
    for i in range(len(instruments)):
        if instruments[i] in instr_melody and len(band_melody) == 0:
            band_melody.append(instruments[i])
        elif instruments[i] in instr_accomp and len(band_accomp) == 0:
            band_accomp.append(instruments[i])
        elif instruments[i] in instr_melody and instr_accomp:
            p = [0.5, 0.5]
            choice = np.random.choice(["melody", "accomp"], p=p)
            if choice == "melody":
                band_melody.append(instruments[i])
            else:
                band_accomp.append(instruments[i])
        elif instruments[i] in instr_melody:
            band_melody.append(instruments[i])
        elif instruments[i] in instr_accomp:
            band_accomp.append(instruments[i])
        elif instruments[i] in instr_bass:
            band_bass.append(instruments[i])
        elif instruments[i] == "beat":
            band_beat = True
        elif instruments[i] == "drum":
            band_drum = True
    print(band_melody)
    print(band_bass)
    print(band_accomp)
    print(band_beat, band_drum)
    return band_melody, band_bass, band_accomp, band_beat, band_drum


# Plays the band with the chosen instruments from create_band
def play_band(structure, progression, number_of_instr):
    chords = init_chords(progression)
    band_melody, band_bass, band_accomp, band_beat, band_drum = create_band(structure, number_of_instr)
    if "piano_h" in band_melody:
        phrase_notes, phrase_rhythm = get_phrase(chords)
        m1 >> play("a", sample=phrase_notes, dur=phrase_rhythm, amp=0.7)
    else:
        m1.stop()
    if "keys" in band_melody:
        phrase_notes, phrase_rhythm = get_phrase(chords)
        m2 >> play("d", sample=phrase_notes, dur=phrase_rhythm)
    else:
        m2.stop()
    if "guitar_a" in band_melody:
        phrase_notes, phrase_rhythm = get_phrase(chords)
        m3 >> play("C", sample=phrase_notes, dur=phrase_rhythm)
    else:
        m3.stop()
    if "guitar_j" in band_melody:
        phrase_notes, phrase_rhythm = get_phrase(chords)
        m4 >> play("c", sample=phrase_notes, dur=phrase_rhythm)
    else:
        m4.stop()
    if "bass_j" in band_bass:
        bassline_notes, bassline_rhythm = get_bassline(chords)
        b1 >> play("b", sample=[bassline_notes], dur=[bassline_rhythm], amp=1.2)
    else:
        b1.stop()
    if "bass_t" in band_bass:
        bassline_notes, bassline_rhythm = get_bassline(chords)
        b2 >> play("B", sample=[bassline_notes], dur=[bassline_rhythm], amp=0.8)
    else:
        b2.stop()
    if "piano_l" in band_bass:
        bassline_notes, bassline_rhythm = get_bassline(chords)
        b3 >> play("A", sample=[bassline_notes], dur=[bassline_rhythm], amp=0.5)
    else:
        b3.stop()
    if "piano_h" in band_accomp:
        c1 >> play("a", sample=P[chords], dur=4, amp=0.50)
    else:
        c1.stop()
    if "keys" in band_accomp:
        c2 >> play("d", sample=P[chords], dur=4, amp=0.50)
    else:
        c2.stop()
    if "guitar_a" in band_accomp:
        c3 >> play("C", sample=P[chords], dur=4, amp=0.50)
    else:
        c3.stop()
    if "guitar_j" in band_accomp:
        c4 >> play("c", sample=P[chords], dur=4, amp=0.50)
    else:
        c4.stop()
    if "strings" in band_accomp:
        c5 >> play("e", sample=P[chords], dur=4, amp=0.50)
    else:
        c5.stop()
    if band_beat:
        beat = get_beat_pattern()
        d1 >> play(beat, amp=0.50)
    else:
        d1.stop()
    if band_drum:
        drum = get_drum_pattern()
        d2 >> play("g", sample=drum, amp=0.30)
    else:
        d2.stop()


# Initializes the chorus to be used throughout the song
def init_chorus():
    global c_band_melody, c_band_bass, c_band_accomp, c_band_beat, c_band_drum, c_chords, c_phrase_notes, c_phrase_rhythm
    global c_bassline_notes, c_bassline_rhythm, c_beat, c_drum, c_length
    tempo, instruments, root, scale = get_parameters()
    c_length = get_length_structure("chorus")
    print("chorus progression:")
    progression = get_progression(root, scale, "I", 3)
    c_chords = init_chords(progression)
    print("chorus band:")
    int_chosen = get_number_of_instruments("chorus")
    print(int_chosen)
    c_band_melody, c_band_bass, c_band_accomp, c_band_beat, c_band_drum = create_band("chorus", int_chosen)
    c_phrase_notes, c_phrase_rhythm = get_phrase(c_chords)
    c_bassline_notes, c_bassline_rhythm = get_bassline(c_chords)
    c_beat = get_beat_pattern()
    c_drum = get_drum_pattern()


# Plays the chorus when it is called
def play_chorus():
    global c_band_melody, c_band_bass, c_band_accomp, c_band_beat, c_band_drum, c_chords, c_phrase_notes, c_phrase_rhythm
    global c_bassline_notes, c_bassline_rhythm, c_beat, c_drum
    print("chorus band:")
    print(c_band_melody)
    print(c_band_bass)
    print(c_band_accomp)
    print(c_band_beat, c_band_drum)
    if "piano_h" in c_band_melody:
        c_phrase_notes, c_phrase_rhythm = get_phrase(c_chords)
        m1 >> play("a", sample=c_phrase_notes, dur=c_phrase_rhythm, amp=0.7)
    else:
        m1.stop()
    if "keys" in c_band_melody:
        c_phrase_notes, c_phrase_rhythm = get_phrase(c_chords)
        m2 >> play("d", sample=c_phrase_notes, dur=c_phrase_rhythm)
    else:
        m2.stop()
    if "guitar_a" in c_band_melody:
        c_phrase_notes, c_phrase_rhythm = get_phrase(c_chords)
        m3 >> play("C", sample=c_phrase_notes, dur=c_phrase_rhythm)
    else:
        m3.stop()
    if "guitar_j" in c_band_melody:
        c_phrase_notes, c_phrase_rhythm = get_phrase(c_chords)
        m4 >> play("c", sample=c_phrase_notes, dur=c_phrase_rhythm)
    else:
        m4.stop()
    if "bass_j" in c_band_bass:
        c_bassline_notes, c_bassline_rhythm = get_bassline(c_chords)
        b1 >> play("b", sample=[c_bassline_notes], dur=[c_bassline_rhythm], amp=1.2)
    else:
        b1.stop()
    if "bass_t" in c_band_bass:
        c_bassline_notes, c_bassline_rhythm = get_bassline(c_chords)
        b2 >> play("B", sample=[c_bassline_notes], dur=[c_bassline_rhythm], amp=0.8)
    else:
        b2.stop()
    if "piano_l" in c_band_bass:
        c_bassline_notes, c_bassline_rhythm = get_bassline(c_chords)
        b3 >> play("A", sample=[c_bassline_notes], dur=[c_bassline_rhythm], amp=0.5)
    else:
        b3.stop()
    if "piano_h" in c_band_accomp:
        c1 >> play("a", sample=P[c_chords], dur=4, amp=0.50)
    else:
        c1.stop()
    if "keys" in c_band_accomp:
        c2 >> play("d", sample=P[c_chords], dur=4, amp=0.50)
    else:
        c2.stop()
    if "guitar_a" in c_band_accomp:
        c3 >> play("C", sample=P[c_chords], dur=4, amp=0.50)
    else:
        c3.stop()
    if "guitar_j" in c_band_accomp:
        c4 >> play("c", sample=P[c_chords], dur=4, amp=0.50)
    else:
        c4.stop()
    if "strings" in c_band_accomp:
        c5 >> play("e", sample=P[c_chords], dur=4, amp=0.50)
    else:
        c5.stop()
    if c_band_beat:
        d1 >> play(c_beat, amp=0.50)
    else:
        d1.stop()
    if c_band_drum:
        d2 >> play("g", sample=c_drum, amp=0.30)
    else:
        d2.stop()


# Returns a random number of instruments that are possible according to the structure given.
def get_number_of_instruments(structure):
    tempo, instruments, root, scale = get_parameters()
    total_instr = len(instruments)
    number_of_instr = [2, 3, 4, 5]
    if total_instr == 1 or structure == "intro" or structure == "solo":
        int_chosen = 1
    elif total_instr == 2:
        int_chosen = 2
    elif total_instr == 3:
        if structure == "verse":
            p = [0.3, 0.7, 0, 0]
        if structure == "chorus":
            p = [0.2, 0.8, 0, 0]
        if structure == "bridge":
            p = [0.3, 0.7, 0, 0]
        int_chosen = np.random.choice(number_of_instr, p=p)
    elif total_instr == 4:
        if structure == "verse":
            p = [0.1, 0.2, 0.7, 0]
        if structure == "chorus":
            p = [0.1, 0.1, 0.8, 0]
        if structure == "bridge":
            p = [0.1, 0.2, 0.7, 0]
        int_chosen = np.random.choice(number_of_instr, p=p)
    elif total_instr == 5:
        if structure == "verse":
            p = [0.1, 0.1, 0.3, 0.5]
        if structure == "chorus":
            p = [0.05, 0.05, 0.3, 0.6]
        if structure == "bridge":
            p = [0.1, 0.1, 0.3, 0.5]
        int_chosen = np.random.choice(number_of_instr, p=p)
    return int_chosen


# Gets the instruments from previous structure to markov chain use them in the next structure. Need to implement
def get_random_instruments(structure):
    tempo, instruments, root, scale = get_parameters()
    numbers = []
    for i in range(1, len(instruments)):
        numbers.append(i)
    if structure == "intro":
        p = [0.5, 0.5, 0, 0, 0]
    if structure == "verse":
        p = [0.3, 0.4, 0.15, 0.1, 0.05]
    if structure == "chorus":
        p = [0.4, 0.3, 0.15, 0.1, 0.05]
    if structure == "bridge":
        p = [0.4, 0.4, 0, 0.2, 0]
    if structure == "solo":
        p = [0.3, 0.5, 0.15, 0, 0.05]
    res = np.random.choice(numbers, p=p)
    return res
