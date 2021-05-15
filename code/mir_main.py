"""File that manipulates data for MIR extraction. Makes the lookup model for supercollider annotations"""
# Author: Laurens Van Goethem, UGent

import librosa as lr
import glob
import csv
import numpy as np
import pandas as pd
import statistics
from matplotlib import pyplot as plt
from mir_features import *
from matplotlib.pyplot import axvline, axhline


###################################################################################################
# Main extraction


# Reads the whole directory to extract mir features
def mir(dir_name, kind, sr):
    print("Reading " + dir_name + "...")  # Print name of file directory
    audio_files = glob.glob('audiofiles/' + dir_name + '/*.' + kind)

    # start csv
    file = open('features_data/data_' + dir_name + '.csv', 'w', newline='')
    header = 'filename tempo chromagram zero_crossing_rate spectral_rolloff spectral_centroid spectral_bandwidth rmse'
    header = header.split()
    with file:
        writer = csv.writer(file)
        writer.writerow(header)

    # read all files in directory
    dir_features = []
    for i in range(0, len(audio_files), 1):
        name_file = audio_files[i][11:]
        print(name_file)
        audio, sr = lr.load(audio_files[i], sr=sr)
        # Extract features from audio and write to csv
        features = all_features(audio, sr)
        # Other features come from essentia
        dir_features.append(features)
        write_csv(features, dir_name, name_file)

    # Reads the data from final csv file and exports to excel
    data = pd.read_csv('features_data/data_' + dir_name + '.csv')
    data.to_excel(r'features_data/data_' + dir_name + '.xlsx', header=True)
    print(data)


# Writes data to csv file
def write_csv(features, dir_name, name_file):
    to_append = f'{name_file} {features[0]} {features[1]} {features[2]}' \
                f' {features[3]} {features[4]} {features[5]} {features[6]}'
    file = open('features_data/data_' + dir_name + '.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(to_append.split())


###################################################################################################
# Plotting of CSV files


# Plots the data of two csv files
def plot_csv(csv01_name, csv02_name):
    columns = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    counter = 0
    units = ['bpm', 'dimensieloos', '%', '%', 'Hz', 'Hz', 'Hz', '%', 'dimensieloos', 'Hz', 'Hz', 'dB']
    for i in columns:
        data01 = []
        with open(csv01_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                if lines[i] == "major":
                    lines[i] = 0
                elif lines[i] == "minor":
                    lines[i] = 1
                data01.append(lines[i])
        data02 = []
        with open(csv02_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                if lines[i] == "major":
                    lines[i] = 0
                elif lines[i] == "minor":
                    lines[i] = 1
                data02.append(lines[i])
        plot_a_feature(data01, data02, "deam", "supercollider", units[counter])
        counter += 1


# Plots one feature from two csv files
def plot_a_feature(data01, data02, csv01_name, csv02_name, y_label):
    title = data01[0]
    data01.remove(data01[0])
    data02.remove(data02[0])
    labels = [csv01_name, csv02_name]
    colors = ["crimson", "limegreen"]
    width = 0.5
    fig, ax = plt.subplots()
    data01 = list(map(float, data01))
    data02 = list(map(float, data02))
    data = data01
    for i in range(2):
        x = np.ones(len(data)) * i
        ax.scatter(x, data, color=colors[i], s=25)
        mean = statistics.mean(data)
        ax.plot([i - width / 2., i + width / 2.], [mean, mean], color="k")
        data = data02
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    plt.title(title)
    plt.ylabel(y_label)
    plt.show()


# Segments audio. Optional
def segment_audio(audio, sr):
    frame_sz = int(0.100 * sr)
    onset_samples = get_onset_samples(audio, sr)
    segments = np.array([audio[i:i + frame_sz] for i in onset_samples])
    return segments


# Concatenates the segments. Optional
def concatenate_segments(segments, sr=22050, pad_time=0.300):
    padded_segments = [np.concatenate([segment, np.zeros(int(pad_time * sr))]) for segment in segments]
    return np.concatenate(padded_segments)


# Plots all the emotional annotation obtained from two csv files
def plot_anno_csv(filename):
    valence, arousal = get_anno_csv(filename)
    index = filename.find("/") + 1
    index_2 = filename.find(".")
    figure = zplane(valence, arousal, filename[index:index_2])
    return figure


# Gets the emotional annotations from a file and return them in lists
def get_anno_csv(filename):
    valence = []
    arousal = []
    # Distinguish supercollider and deam anno dataset
    if filename.find("supercollider") != -1:
        index = 2
    else:
        index = 3
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        for lines in csv_reader:
            valence.append(lines[1])
            arousal.append(lines[index])
    valence = list(map(float, valence))
    arousal = list(map(float, arousal))
    return valence, arousal


# Plots a zplane figure to show valence and arousal
def zplane(x, y, name):
    fig, ax = plt.subplots()
    axvline(5, color='0.7')
    axhline(5, color='0.7')
    plt.scatter(x, y)
    ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.axis('image')
    plt.tight_layout()
    plt.title("Emotional annotations " + name)
    plt.xlabel("Valence")
    plt.ylabel("Arousal")
    plt.show()
    return fig


# Gets the tempo column from a CSV datafile
def get_tempo_data(filename):
    tempo = []
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        for lines in csv_reader:
            tempo.append(lines[2])
    tempo = list(map(float, tempo))
    return tempo


# Plots the tempo heatmap from a hardcoded dataset
def plot_heatmap(filename):
    # anno_name = "features_data/anno_" + filename
    # data_name = "features_data/data_" + filename
    anno_name = "features_data/anno_mapped_supercollider.csv"
    data_name = "features_data/data_mapped_supercollider.csv"
    x, y = get_anno_csv(anno_name)
    tempo = get_tempo_data(data_name)
    index = filename.find("/") + 1
    index_2 = filename.find(".")
    name = filename[index:index_2]
    fig, ax = plt.subplots()
    axvline(5, color='0.7')
    axhline(5, color='0.7')
    plt.scatter(x, y, c=tempo, s=500)
    ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.axis('image')
    plt.tight_layout()
    plt.title("Emotional annotations " + name)
    plt.xlabel("Valence")
    plt.ylabel("Arousal")
    plt.show()
    return fig


###################################################################################################
# Creates the lookup model


# Rearrange the csv file to use the data
def put_seperate_lists(filename):
    name = []
    tempo = []
    root = []
    scale = []
    chroma = []
    zcr = []
    roll = []
    centroid = []
    bandwidth = []
    rmse = []
    dance = []
    per10 = []
    per90 = []
    dyn = []
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        for lines in csv_reader:
            name.append(lines[1])
            tempo.append(lines[2])
            root.append(lines[3])
            if lines[4] == "major":
                scale.append(0)
            else:
                scale.append(1)
            chroma.append(lines[5])
            zcr.append(lines[6])
            roll.append(lines[7])
            centroid.append(lines[8])
            bandwidth.append(lines[9])
            rmse.append(lines[10])
            dance.append(lines[11])
            per10.append(lines[12])
            per90.append(lines[13])
            dyn.append(lines[14])
    set = [tempo, scale, chroma, zcr, roll, centroid, bandwidth, rmse, dance, per10, per90, dyn]
    return set, name


# Function to transform/map the supercollider data according to the deam dataset
# into a new csv file called: 'data_mapped_supercollider' and plots them too and saves the images.
def get_mapped_features():
    filename_1 = "features_data/data_deam.csv"
    filename_2 = "features_data/data_supercollider.csv"

    # Get all features from the 2 files in separate lists. Set one is from deam,
    # set two is from supercollider, set three is the new mapped file
    set_1, name_1 = put_seperate_lists(filename_1)
    set_2, name_2 = put_seperate_lists(filename_2)
    set_3 = []

    print("--------------------")
    print(set_1)
    print(set_2)
    print("--------------------")

    # For every feature from the sets, map all values
    header = ['tempo', 'scale', 'chromagram', 'zero_crossing_rate', 'spectral_rolloff', 'spectral_centroid',
              'spectral_bandwidth', 'rmse', 'danceability', 'percentile_10', 'percentile_90', 'dynamic_comp']
    for i in range(len(set_1)):
        features_1 = set_1[i]
        features_2 = set_2[i]
        features_1 = list(map(float, features_1))
        features_2 = list(map(float, features_2))
        mapped_set = []
        min_1, max_1 = get_min_max(features_1)
        min_2, max_2 = get_min_max(features_2)
        for j in features_2:
            mapped_value = translate(j, min_1, max_1, min_2, max_2)
            mapped_set.append(mapped_value)
        set_3.append(mapped_set)
        plot_a_mapped_feature(features_1, mapped_set, "deam", "mapped_supercollider", header[i])
    set_3.insert(0, name_2)
    write_mapped_csv(set_3)


# Writes the new csv file for the mapped supercollider dataset.
def write_mapped_csv(mapped_set):
    file = open('features_data/data_mapped_supercollider.csv', 'w', newline='')
    header = 'number filename tempo scale chromagram zero_crossing_rate spectral_rolloff spectral_centroid' \
             ' spectral_bandwidth rmse dance percentile_10 percentile_90 dynamic_comp'
    header = header.split()
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    for i in range(len(mapped_set[0])):
        to_append = f'{i} {mapped_set[0][i]} {mapped_set[1][i]} {mapped_set[2][i]} {mapped_set[3][i]} {mapped_set[4][i]}' \
                    f' {mapped_set[5][i]} {mapped_set[6][i]} {mapped_set[7][i]} {mapped_set[8][i]} {mapped_set[9][i]}' \
                    f' {mapped_set[10][i]} {mapped_set[11][i]} {mapped_set[12][i]}'
        file = open('features_data/data_mapped_supercollider.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())


# Plots the features from data_deam and data_mapped_supercollider next to each other.
def plot_a_mapped_feature(data01, data02, csv01_name, csv02_name, title):
    labels = [csv01_name, csv02_name]
    colors = ["crimson", "limegreen"]
    width = 0.4
    fig, ax = plt.subplots()
    data01 = list(map(float, data01))
    data02 = list(map(float, data02))
    data = data01
    for i in range(2):
        x = np.ones(len(data)) * i
        ax.scatter(x, data, color=colors[i], s=25)
        mean = statistics.mean(data)
        ax.plot([i - width / 2., i + width / 2.], [mean, mean], color="k")
        data = data02
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    plt.title(title)
    plt.show()
    fig.savefig('features_data/plots/mapped_' + title + '.png')


# Gets the min max according to 1 and 99 percentiles from a set of features.
def get_min_max(feature_set):
    min = np.percentile(feature_set, 1)
    max = np.percentile(feature_set, 99)
    return min, max


# Gets the width of each range and converts a value corresponding to the right range.
def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - right_min) / float(right_span)
    return left_min + (value_scaled * left_span)


# Checks the mapped_supercollider and deam dataset features and compares them.
# The one song number from the deam dataset that has the least difference in features returns its valence and arousal
# so it can be copied to the mapped_supercollider song.
def get_closest_value(number):
    with open('features_data/data_mapped_supercollider.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        for line in csv_reader:
            if number == int(line[0]):
                features = [line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10],
                            line[11], line[12], line[13]]
                features_super = list(map(float, features))
    print("------------------------------")
    print("song number chosen:", number)
    print(features_super)
    deam_number = 2
    features_deam, valence, arousal = read_anno_deam(deam_number)
    del features_deam[0]
    del features_deam[1]
    if features_deam[1] == "major":
        features_deam.insert(1, "0")
    else:
        features_deam.insert(1, "1")
    del features_deam[2]
    features_deam = list(map(float, features_deam))
    diff = compare_features(features_super, features_deam)
    diff_min = diff
    index_min = 2
    for i in range(3, 1801):
        try:
            features_deam, valence, arousal = read_anno_deam(i)
            del features_deam[0]
            del features_deam[1]
            if features_deam[1] == "major":
                features_deam.insert(1, "0")
            else:
                features_deam.insert(1, "1")
            del features_deam[2]
            features_deam = list(map(float, features_deam))
            diff = compare_features(features_super, features_deam)
            if diff < diff_min:
                diff_min = diff
                index_min = i
        except:
            print("ERROR: probably no song number", i, " in deam dataset")
            pass
    print("closest related song:", index_min)
    print("difference:", diff_min)
    features_min, valence_min, arousal_min = read_anno_deam(index_min)
    print("filename:", features_min[0])
    print("valence:", valence_min)
    print("arousal", arousal_min)
    return valence_min, arousal_min


# Reads the deam data file and gets the features and annotations for one particular song number in the deam dataset.
def read_anno_deam(song_number):
    data = "features_data/data_deam.csv"
    anno = "features_data/anno_deam.csv"
    with open(anno, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        valence = None
        arousal = None
        for line in csv_reader:
            if int(line[0]) == song_number:
                valence = line[1]
                arousal = line[3]
    with open(data, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        for line in csv_reader:
            index_1 = line[1].find("/") + 1
            index_2 = line[1].find(".mp")
            number = int(line[1][index_1:index_2])
            if number == song_number:
                features = [line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10],
                            line[11],
                            line[12], line[13], line[14]]
    return features, valence, arousal


# Math to compare two feature sets in percentage.
def compare_features(features_1, features_2):
    differences = []
    for index in range(len(features_1)):
        diff = abs(features_1[index] - features_2[index])
        div = (features_1[index] + features_2[index]) / 2
        if diff == 0 and div == 0:
            frac = 0.01
        else:
            frac = diff / div
        percent = frac * 100
        differences.append(percent)
    return sum(differences)


# Writes the obtained number valence and arousal to the anno_mapped_supercollider dataset.
def write_to_anno_csv(number, valence, arousal):
    to_append = f'{number} {valence} {arousal}'
    file = open('features_data/anno_mapped_supercollider.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(to_append.split())


# Gets all annotation data for the mapped_supercollider_dataset and writes it to a csv file.
def get_anno_for_supercollider():
    file = open('features_data/anno_mapped_supercollider.csv', 'w', newline='')
    header = 'song_number valence arousal'
    header = header.split()
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    for i in range(236):
        valence, arousal = get_closest_value(i)
        write_to_anno_csv(i, valence, arousal)


if __name__ == '__main__':
    # get_mapped_features()
    # get_anno_for_supercollider()
    # plot_anno_csv("features_data/anno_mapped_supercollider.csv")
    # plot_anno_csv("features_data/anno_deam.csv")
    # get_closest_value(122)
    # plot_csv("features_data/data_deam.csv", "features_data/data_supercollider.csv")
    # plot_heatmap(".csv")
    plot_anno_csv("model_data/anno_pred_supercollider.csv")
